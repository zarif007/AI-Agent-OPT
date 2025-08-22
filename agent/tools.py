import json
import re
from constants.operator_mapping import OP_MAP

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
    if op == '%': return a % b
    if op == 'A': return (a + b) / 2
    raise ValueError(f"Unsupported operator {op}")

def evaluate(expr: str):
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
    return values[-1]

_TEMPS = {
    "paris": "18",
    "london": 17.0,
    "dhaka": 31,
    "amsterdam": "19.5"
}

def temp(city: str):
    c = (city or "").strip()
    return _TEMPS.get(c, "20")


def kb_lookup(q: str) -> str:
    try:
        with open("data/kb.json","r") as f:
            data = json.load(f)
        for item in data.get("entries", []):
            if q in item.get("name",""):
                return item.get("summary","")
        return "No entry found."
    except Exception as e:
        return f"KB error: {e}"
