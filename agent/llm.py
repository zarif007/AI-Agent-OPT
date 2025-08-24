import json
import re
import string
from typing import List, Dict, Optional, Union
from constants import OP_MAP, WEATHER, JOB_KEYWORDS, ROLE_KEYWORDS, LOCATION_KEYWORDS, DATE_KEYWORDS, COMPANY_KEYWORDS
from utils.info_logger import info_logger
from utils.llm_cost_logger import llm_cost_logger

# Logger setup
logger = info_logger()
cost_logger = llm_cost_logger()

def log_cost(prompt: str, tools_output: str = ""):
    # 812 tokens for system prompt
    # 1M tokens = $1, so cost = (tokens / 1_000_000)
    prompt_tokens = len(prompt.split())
    output_tokens = len(tools_output.split()) if tools_output else 0
    total_tokens = 812 + prompt_tokens + output_tokens
    cost = total_tokens / 1_000_000
    cost_logger.info(f"Prompt: {prompt} | Total Tokens: {total_tokens} | Cost: ${cost:.6f}")

def extract_calc_tool(prompt: str) -> Optional[Dict[str, any]]:
    """Checks if the prompt involves a calculation and returns a calc tool call if applicable."""
    calc_keywords = set(OP_MAP.keys()) | set(OP_MAP.values())
    if any(keyword in prompt for keyword in calc_keywords):
        logger.info(f"extract_calc_tool: Detected calculation in prompt: {prompt}")
        return {"tool": "calc", "args": {"expr": prompt}}
    return None

def extract_weather_tool(prompt: str) -> List[Dict[str, any]]:
    """
    Checks if the prompt involves weather or temperature and returns a list of weather tool calls
    for each mentioned city, including the matched keyword in args.
    """
    weather_keywords = ["weather", "temperature", "condition", "temp", "humidity"]
    cities = set(WEATHER.keys())
    
    matched_keyword = next((keyword for keyword in weather_keywords if keyword in prompt), None)
    if not matched_keyword:
        return []
    
    mentioned_cities = [city for city in cities if city in prompt]
    if not mentioned_cities:
        mentioned_cities = ["paris"]
    logger.info(f"extract_weather_tool: Detected weather query for cities {mentioned_cities} with keyword '{matched_keyword}' in prompt: {prompt}")
    return [{"tool": "weather", "args": {"city": city, "keyword": matched_keyword}} for city in mentioned_cities]

def extract_kb_tool(prompt: str) -> Optional[Dict[str, any]]:
    """Detect KB query if an entry name OR any exact (non-stopword) word from its summary exists in the prompt."""

    STOP_WORDS = {
        "a", "an", "and", "are", "as", "at", "be", "by",
        "for", "from", "has", "he", "in", "is", "it", "its", "'s", "s",
        "of", "on", "that", "the", "to", "was", "were", "will", "with"
    }

    def tokenize(text: str) -> list:
        text = text.lower()
        text = re.sub(f"[{re.escape(string.punctuation)}]", " ", text)
        return [w for w in text.split() if w]

    try:
        with open("data/kb.json", "r", encoding="utf-8") as f:
            kb = json.load(f)

        prompt_words = tokenize(prompt)

        for entry in kb.get("entries", []):
            name = entry["name"].lower()
            summary_words = set(tokenize(entry.get("summary", "")))

            if name in prompt.lower():
                logger.info(f"extract_kb_tool: Detected KB query for '{entry['name']}' (name match) in prompt: {prompt}")
                return {"tool": "kb", "args": {"q": entry["name"]}}

            for word in prompt_words:
                if word not in STOP_WORDS and word in summary_words:
                    logger.info(f"extract_kb_tool: Detected KB query for '{entry['name']}' (matched word '{word}') in prompt: {prompt}")
                    return {"tool": "kb", "args": {"q": word}}

        return None

    except Exception as e:
        logger.error(f"extract_kb_tool: Error reading or processing kb.json: {e}")
        return None


def extract_job_search_tool(prompt: str) -> Optional[Dict[str, any]]:
    """Checks if the prompt involves a job search and returns a job_search tool call if applicable."""
    prompt_lower = prompt.lower()

    has_job = any(keyword in prompt_lower for keyword in JOB_KEYWORDS)
    matched_role = next((role for role in ROLE_KEYWORDS if role in prompt_lower), None)
    matched_company = next((comp for comp in COMPANY_KEYWORDS if comp in prompt_lower), None)

    if not has_job and not matched_role:
        return None  

    args = {}

    if matched_role:
        args["role"] = matched_role  

    if matched_company:
        args["company"] = matched_company  

    for loc in LOCATION_KEYWORDS:
        if loc in prompt_lower:
            args["location"] = loc
            break  

    for date in DATE_KEYWORDS:
        if date in prompt_lower:
            args["date_posted"] = date
            break  

    logger.info(f"extract_job_search_tool: Detected job search with args {args} in prompt: {prompt}")
    return {"tool": "job_search", "args": args}

def call_llm(prompt: str) -> Union[List[Dict[str, any]], str, None]:
    """
    Parses the input prompt and returns an **ordered list** of tool calls or a direct response.
    """
    if not prompt or not isinstance(prompt, str):
        logger.warning("call_llm: Invalid prompt received.")
        return []

    prompt_clean = prompt.strip()
    prompt_lower = prompt.lower().strip()

    tool_calls: List[Dict[str, any]] = []
    
    calc_tool = extract_calc_tool(prompt_lower)
    if calc_tool:
        tool_calls.append(calc_tool)
    
    weather_tools = extract_weather_tool(prompt_lower)
    if weather_tools:
        tool_calls.extend(weather_tools)
    
    kb_tool = extract_kb_tool(prompt_lower)
    if kb_tool:
        tool_calls.append(kb_tool)

    job_search_tool = extract_job_search_tool(prompt_lower)
    if job_search_tool:
        tool_calls.append(job_search_tool)

    TOOL_PRIORITY = {"weather": 1, "kb": 1, "calc": 2, "job_search": 2}
    tool_calls = sorted(tool_calls, key=lambda call: TOOL_PRIORITY.get(call["tool"], 99))

    tools_output_str = "; ".join([
        f"{call['tool']}({', '.join(f'{k}={v}' for k, v in call.get('args', {}).items())})"
        for call in tool_calls
    ])

    log_cost(prompt_clean, tools_output_str)

    if tool_calls:
        logger.info(f"call_llm: Selected tools (ordered): {[call['tool'] for call in tool_calls]}")
    else:
        logger.info("call_llm: Selected tools: none")
    
    return tool_calls
