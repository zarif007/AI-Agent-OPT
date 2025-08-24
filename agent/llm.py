import json
from typing import List, Dict, Optional, Union
from constants import OP_MAP, WEATHER, JOB_KEYWORDS, ROLE_KEYWORDS, LOCATION_KEYWORDS, DATE_KEYWORDS, COMPANY_KEYWORDS

def extract_calc_tool(prompt: str) -> Optional[Dict[str, any]]:
    """Checks if the prompt involves a calculation and returns a calc tool call if applicable."""
    calc_keywords = set(OP_MAP.keys()) | set(OP_MAP.values())
    if any(keyword in prompt for keyword in calc_keywords):
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
    
    return [{"tool": "weather", "args": {"city": city, "keyword": matched_keyword}} for city in mentioned_cities]

def extract_kb_tool(prompt: str) -> Optional[Dict[str, any]]:
    """Checks if the prompt is a 'who is' query and returns a kb tool call 
    if any kb entry name exists in the prompt string (anywhere)."""

    try:
        with open("data/kb.json", "r", encoding="utf-8") as f:
            kb = json.load(f)

        prompt_lower = prompt.lower()
        for entry in kb.get("entries", []):
            if entry["name"].lower() in prompt_lower:
                return {"tool": "kb", "args": {"q": entry["name"]}}

        return None

    except (FileNotFoundError, json.JSONDecodeError):
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

    return {"tool": "job_search", "args": args}

def call_llm(prompt: str) -> Union[List[Dict[str, any]], str, None]:
    """
    Parses the input prompt and returns an **ordered list** of tool calls or a direct response.
    """
    if not prompt or not isinstance(prompt, str):
        print("Selected tools: none (invalid)")
        return []

    prompt = prompt.lower().strip()

    tool_calls: List[Dict[str, any]] = []
    
    calc_tool = extract_calc_tool(prompt)
    if calc_tool:
        tool_calls.append(calc_tool)
    
    weather_tools = extract_weather_tool(prompt)
    if weather_tools:
        tool_calls.extend(weather_tools)
    
    kb_tool = extract_kb_tool(prompt)
    if kb_tool:
        tool_calls.append(kb_tool)

    job_search_tool = extract_job_search_tool(prompt)
    if job_search_tool:
        tool_calls.append(job_search_tool)

    TOOL_PRIORITY = {"weather": 1, "kb": 1, "calc": 2, "job_search": 2}
    tool_calls = sorted(tool_calls, key=lambda call: TOOL_PRIORITY.get(call["tool"], 99))

    if tool_calls:
        print(f"Selected tools (ordered): {[call['tool'] for call in tool_calls]}")
    else:
        print("Selected tools: none")
    
    return tool_calls
