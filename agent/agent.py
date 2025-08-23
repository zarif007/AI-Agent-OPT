from .llm import call_llm
from . import tools

def answer(q: str):
    plan = call_llm(q)
    print(plan)
    results = []
    context = {}

    if plan and isinstance(plan, list):
        for step in plan:
            if isinstance(step, dict) and "tool" in step:
                if step["tool"] == "calc":
                    results.append(tools.evaluate(step["args"]["expr"], context))
                elif step["tool"] == "weather":
                    city = step["args"]["city"]
                    keyword = step["args"]["keyword"]
                    t = tools.temp(city, keyword, context)
                    results.append(t)
                elif step["tool"] == "kb":
                    results.append(tools.kb_lookup(step["args"]["q"], context))
                elif step["tool"] == "job_search":
                    results.append(tools.job_search(step["args"], context))

    res = results[-1] if results else "Sorry, I could not find an answer."
    return res
