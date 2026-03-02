from markdown import markdown
from weasyprint import HTML

from app.celery import celery
from app.modules.research.methods import generate_queries, search_web, generate_report


def research(topic: str):
    print(f"Reseacrh Start ....")
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
    HTML(string=result).write_pdf(f"./reports/{topic.replace(" ", "_")}.pdf")


@celery.task
def research_task(topic: str):
    research(topic)