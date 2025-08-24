import json
import re
from constants import OP_MAP, TEMPS, WEATHER
from logger.info_logger import info_logger
from typing import Any, Dict, List, Optional

# Logger setup
logger = info_logger()

def normalize_expr(expr: str) -> str:
    expr = expr.lower()
    for k in sorted(OP_MAP.keys(), key=lambda x: -len(x)):
        expr = re.sub(rf'\b{k}\b', OP_MAP[k], expr)
    expr = re.sub(r'\band\b', '', expr)
    logger.info(f"normalize_expr: Normalized expression: {expr}")
    return expr

def tokenize(expr: str) -> List[str]:
    expr = expr.strip()
    tokens = re.findall(r'\d+\.?\d*|[+\-*/%A()]', expr)
    return tokens

def precedence(op: str) -> int:
    if op in ('+', '-', 'A'): return 1
    if op in ('*', '/', '%'): return 2
    return 0

def apply_operation(a: float, b: float, op: str) -> float:
    if op == '+': return a + b
    if op == '-': return a - b
    if op == '*': return a * b
    if op == '/': return a / b if b != 0 else (float("inf") if a >= 0 else float('-inf'))
    if op == '%': return (a / 100) * b
    if op == 'A': return (a + b) / 2
    raise ValueError(f"Unsupported operator {op}")

def replace_context(expr: str, context: Optional[Dict[str, Any]]) -> str:
    if not context:
        return expr
    for key, value in context.items():
        expr = expr.replace(key, str(value))
    return expr

def handle_unary_minus(values: List[float], ops: List[str]) -> bool:
    if len(values) == 1 and ops and ops[-1] == '-':
        values[-1] = -values[-1]
        ops.pop()
        return True
    return False

def evaluate(expr: str, context: Optional[Dict[str, Any]] = None) -> float:
    expr = replace_context(expr, context)
    expr = normalize_expr(expr)
    tokens: List[str] = tokenize(expr)
    values: List[float] = []
    ops: List[str] = []
    logger.info(f"evaluate: Evaluating expression: {expr}")
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if re.match(r'^\d+\.?\d*$', token):
            values.append(float(token))
        elif token == '(': 
            ops.append(token)
        elif token == ')':
            while ops and ops[-1] != '(': 
                if len(values) < 2:
                    if handle_unary_minus(values, ops):
                        continue
                    else:
                        break
                b = values.pop()
                a = values.pop()
                values.append(apply_operation(a, b, ops.pop()))
            ops.pop()
        else:
            while ops and ops[-1] not in '(' and precedence(ops[-1]) >= precedence(token):
                if len(values) < 2:
                    if handle_unary_minus(values, ops):
                        continue
                    else:
                        break
                b = values.pop()
                a = values.pop()
                values.append(apply_operation(a, b, ops.pop()))
            ops.append(token)
        i += 1
    
    while ops:
        if len(values) < 2:
            if handle_unary_minus(values, ops):
                continue
            else:
                break
        b = values.pop()
        a = values.pop()
        values.append(apply_operation(a, b, ops.pop()))
    
    ans: float = values[-1] if values else 0.0
    if context is not None:
        context[expr] = ans
    logger.info(f"evaluate: Result for '{expr}' is {ans}")
    return ans

def temp(city: str, keyword: str, context: Optional[Dict[str, Any]] = None) -> str:
    c: str = (city or "").strip().lower()
    k: str = (keyword or "").strip().lower()
    logger.info(f"temp: Query for city='{c}', keyword='{k}'")
    if k.strip().lower() in ["temperature", "temp", "humidity"]:
        ans = TEMPS.get(c, 20)   
    elif k.strip().lower() in ["weather", "condition"]:
        ans = WEATHER.get(c, "clear sky")  
    else:
        ans = TEMPS.get(c, 20)   
    if context is not None:
        context[c] = ans
    logger.info(f"temp: Result for city='{c}', keyword='{k}' is '{ans}'")
    return ans

def kb_lookup(q: str, context: Optional[Dict[str, Any]] = None) -> str:
    try:
        with open("data/kb.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        q_lower = q.lower()

        for item in data.get("entries", []):
            name = item.get("name", "")
            summary = item.get("summary", "")
            if q_lower in name.lower():
                ans = summary
                if context is not None:
                    context[q] = ans
                logger.info(f"kb_lookup: Found summary for '{q}' by name match")
                return ans
            summary_words = re.findall(r"\w+", summary.lower())
            if q_lower in summary_words:
                if context is not None:
                    context[q] = name
                logger.info(f"kb_lookup: Found entry '{name}' for summary word match '{q}'")
                return name

        logger.info(f"kb_lookup: No entry found for '{q}'")
        return "No entry found."

    except Exception as e:
        logger.error(f"kb_lookup: Error for '{q}': {e}")
        return f"KB error: {e}"

def job_search(args: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    role = args.get("role")
    location = args.get("location")
    date_posted = args.get("date_posted")
    company = args.get("company")

    logger.info(f"job_search: Searching jobs with args: {args}")
    date_patterns = {
        r"(24h|24 hours|today|recently)": "24h",
        r"(1 week|last week|7 days)": "1w",
        r"(1 month|last month|30 days)": "1m"
    }

    mapped_date: Optional[str] = None
    if date_posted:
        for pattern, mapped_value in date_patterns.items():
            if re.search(pattern, date_posted, re.IGNORECASE):
                mapped_date = mapped_value
                break

    try:
        with open("data/jobs.json", "r", encoding="utf-8") as f:
            jobs_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        logger.error("job_search: Error reading jobs.json")
        return []

    jobs = jobs_data.get("jobs", [])
    results: List[Dict[str, Any]] = []

    for job in jobs:
        if role and role.lower() != job.get("role", "").lower():
            continue
        if location and location.lower() != job.get("location", "").lower():
            continue
        if company and company.lower() != job.get("company", "").lower():
            continue
        if mapped_date and mapped_date.lower() != job.get("date_posted", "").lower():
            continue

        results.append(job)

    logger.info(f"job_search: Found {len(results)} jobs for args: {args}")
    return results

    