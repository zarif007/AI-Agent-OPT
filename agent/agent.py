from .llm import call_llm
from . import tools

def answer(q: str):
    plan = call_llm(q)
    print(plan)
    results = []
    if plan and isinstance(plan, list):
        for step in plan:
            if isinstance(step, dict) and "tool" in step:
                if step["tool"] == "calc":
                    results.append(tools.evaluate(step["args"]["expr"]))
                elif step["tool"] == "weather":
                    city = step["args"]["city"]
                    t = tools.temp(city)
                    results.append(f"{t} C")
                elif step["tool"] == "kb":
                    results.append(tools.kb_lookup(step["args"]["q"]))
    return results

    return str(plan)
