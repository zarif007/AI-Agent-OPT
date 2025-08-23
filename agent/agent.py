from .llm import call_llm
from . import tools

def answer(q: str):
    tasks = call_llm(q)
    results = []
    context = {}

    if tasks and isinstance(tasks, list):
        for sub_tasks in tasks:
            if isinstance(sub_tasks, dict) and "tool" in sub_tasks:
                if sub_tasks["tool"] == "calc":
                    results.append(tools.evaluate(sub_tasks["args"]["expr"], context))
                elif sub_tasks["tool"] == "weather":
                    city = sub_tasks["args"]["city"]
                    keyword = sub_tasks["args"]["keyword"]
                    t = tools.temp(city, keyword, context)
                    results.append(t)
                elif sub_tasks["tool"] == "kb":
                    results.append(tools.kb_lookup(sub_tasks["args"]["q"], context))
                elif sub_tasks["tool"] == "job_search":
                    results.append(tools.job_search(sub_tasks["args"], context))

    ans = results[-1] if results else "Sorry, I could not find an answer."
    return ans
