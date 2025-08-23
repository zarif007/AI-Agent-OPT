import json
import re
from constants import OP_MAP, TEMPS, WEATHER

def normalize_expr(expr: str) -> str:
    expr = expr.lower()
    for k in sorted(OP_MAP.keys(), key=lambda x: -len(x)):
        expr = re.sub(rf'\b{k}\b', OP_MAP[k], expr)
    expr = re.sub(r'\band\b', '', expr)
    return expr

def tokenize(expr: str):
    expr = expr.strip()
    tokens = re.findall(r'\d+\.?\d*|[+\-*/%A()]', expr)
    return tokens

def precedence(op):
    if op in ('+', '-', 'A'): return 1
    if op in ('*', '/', '%'): return 2
    return 0

def apply_operation(a, b, op):
    if op == '+': return a + b
    if op == '-': return a - b
    if op == '*': return a * b
    if op == '/': return a / b
    if op == '%': return (a / 100) * b
    if op == 'A': return (a + b) / 2
    raise ValueError(f"Unsupported operator {op}")

def replace_context(expr: str, context: dict) -> str:
    if not context:
        return expr
    for key, value in context.items():
        expr = expr.replace(key, str(value))
    return expr

def evaluate(expr: str, context: dict = None) -> float:
    expr = replace_context(expr, context)
    expr = normalize_expr(expr)
    tokens = tokenize(expr)
    values = []
    ops = []
    
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
                    break
                b = values.pop()
                a = values.pop()
                values.append(apply_operation(a, b, ops.pop()))
            ops.pop()
        else:
            while ops and ops[-1] not in '(' and precedence(ops[-1]) >= precedence(token):
                if len(values) < 2:
                    break
                b = values.pop()
                a = values.pop()
                values.append(apply_operation(a, b, ops.pop()))
            ops.append(token)
        i += 1

    while ops:
        if len(values) < 2:
            break
        b = values.pop()
        a = values.pop()
        values.append(apply_operation(a, b, ops.pop()))
    
    ans = values[-1] if values else None
    context[expr] = ans
    return ans

def temp(city: str, keyword: str, context: dict = None) -> str:
    c = (city or "").strip().lower()
    k = (keyword or "").strip().lower()
    
    if k.strip().lower() in ["temperature", "temp"]:
        ans = TEMPS.get(c, 20)   
    elif k.strip().lower() in ["weather", "condition"]:
        ans = WEATHER.get(c, "clear sky")  
    else:
        ans = TEMPS.get(c, 20)   
    
    context[c] = ans
    return ans

def kb_lookup(q: str, context: dict = None) -> str:
    try:
        with open("data/kb.json","r") as f:
            data = json.load(f)
        for item in data.get("entries", []):
            if q in item.get("name",""):
                ans = item.get("summary","")
                context[q] = ans
                return ans
        return "No entry found."
    except Exception as e:
        return f"KB error: {e}"

def job_search(args: dict, context: dict = None) -> list:
    role = args.get("role")
    location = args.get("location")
    date_posted = args.get("date_posted")
    company = args.get("company")

    date_patterns = {
        r"(24h|24 hours|today|recently)": "24h",
        r"(1 week|last week|7 days)": "1w",
        r"(1 month|last month|30 days)": "1m"
    }

    mapped_date = None
    if date_posted:
        for pattern, mapped_value in date_patterns.items():
            if re.search(pattern, date_posted, re.IGNORECASE):
                mapped_date = mapped_value
                break

    try:
        with open("data/jobs.json", "r", encoding="utf-8") as f:
            jobs_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    jobs = jobs_data.get("jobs", [])
    results = []

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

    return results

    