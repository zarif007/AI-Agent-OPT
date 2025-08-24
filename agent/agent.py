
from .llm import call_llm
from . import tools
from logger.info_logger import info_logger
from typing import Any, Dict, List, Union

# Logger setup
logger = info_logger()

def answer(q: str):
    logger.info(f"answer: Received question: {q}")
    tasks: Union[List[Dict[str, Any]], str, None] = call_llm(q)
    results: List[Any] = []
    context: Dict[str, Any] = {}

    if tasks and isinstance(tasks, list):
        for sub_tasks in tasks:
            if isinstance(sub_tasks, dict) and "tool" in sub_tasks:
                if sub_tasks["tool"] == "calc":
                    logger.info(f"answer: Calling evaluate with expr: {sub_tasks['args']['expr']}")
                    results.append(tools.evaluate(sub_tasks["args"]["expr"], context))
                elif sub_tasks["tool"] == "weather":
                    city: str = sub_tasks["args"]["city"]
                    keyword: str = sub_tasks["args"]["keyword"]
                    logger.info(f"answer: Calling temp for city: {city}, keyword: {keyword}")
                    t = tools.temp(city, keyword, context)
                    results.append(t)
                elif sub_tasks["tool"] == "kb":
                    logger.info(f"answer: Calling kb_lookup for q: {sub_tasks['args']['q']}")
                    results.append(tools.kb_lookup(sub_tasks["args"]["q"], context))
                elif sub_tasks["tool"] == "job_search":
                    logger.info(f"answer: Calling job_search with args: {sub_tasks['args']}")
                    results.append(tools.job_search(sub_tasks["args"], context))

    ans: str = results[-1] if results else "Sorry, I could not find an answer."
    logger.info(f"answer: Final answer: {ans}")
    return ans
