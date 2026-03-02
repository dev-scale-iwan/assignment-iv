import os
from markdown import markdown
from weasyprint import HTML

from celery.utils.log import get_task_logger
from app.celery import celery
from app.modules.research.methods import generate_queries, search_web, generate_report

logger = get_task_logger(__name__)


def research(topic: str):
    logger.info(f"Research Start By Topic {topic}")
    research_context = ""
    queries = generate_queries(topic)
    
    for query in queries.queries:
        search_result = search_web(query)
        research_context += f"Query: {query} \n\n Search Result: {search_result}\n\n\n"

    research_result = generate_report(topic=topic, research_context=research_context)
    if not research_result:
        raise ValueError("No Research Result Generated")

    # Generate markdown report
    result = markdown(text=research_result, output_format="html")
    os.makedirs("./reports", exist_ok=True)
    HTML(string=result).write_pdf(f"./reports/{topic.replace(" ", "_")}.pdf")


@celery.task
def research_task(topic: str):
    logger.info(f"Research Task")
    research(topic)