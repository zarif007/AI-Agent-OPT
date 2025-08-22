from typing import List, Dict, Optional, Union

def extract_calc_tool(prompt: str) -> Optional[Dict[str, any]]:
    """Checks if the prompt involves a calculation and returns a calc tool call if applicable."""
    calc_keywords = ["%", "+", "-", "*", "/", "add", "average"]
    if any(keyword in prompt for keyword in calc_keywords):
        return {"tool": "calc", "args": {"expr": prompt}}
    return None

def extract_weather_tool(prompt: str) -> List[Dict[str, any]]:
    """
    Checks if the prompt involves weather or temperature and returns a list of weather tool calls
    for each mentioned city.
    """
    weather_keywords = ["weather", "temperature"]
    cities = ["paris", "london", "dhaka"]
    if not any(keyword in prompt for keyword in weather_keywords):
        return []
    
    mentioned_cities = [city for city in cities if city in prompt]
    if not mentioned_cities:
        mentioned_cities = ["paris"]
    
    return [{"tool": "weather", "args": {"city": city}} for city in mentioned_cities]

def extract_kb_tool(prompt: str) -> Optional[Dict[str, any]]:
    """Checks if the prompt is a 'who is' query and returns a kb tool call if applicable."""
    if "who is" not in prompt:
        return None
    try:
        name = prompt.split("who is", 1)[1].strip().rstrip("?")
        if name:
            return {"tool": "kb", "args": {"q": name}}
        return None
    except IndexError:
        return None

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

    TOOL_PRIORITY = {"weather": 1, "kb": 1, "calc": 2}
    tool_calls = sorted(tool_calls, key=lambda call: TOOL_PRIORITY.get(call["tool"], 99))

    if tool_calls:
        print(f"Selected tools (ordered): {[call['tool'] for call in tool_calls]}")
    else:
        print("Selected tools: none")
    
    return tool_calls
