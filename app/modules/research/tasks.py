import os
from markdown import markdown
from weasyprint import HTML

from celery.utils.log import get_task_logger
from app.celery import celery
from app.modules.research.methods import extract_waste_info, generate_queries, search_web, extract_pricing_info, generate_report
from app.models.setorsampah import SetorSampah
from app.core.db import engine
from sqlmodel import Session

logger = get_task_logger(__name__)


def research(title: str):
    logger.info(f"Processing Setor Sampah: {title}")
    
    # 1 & 2. Validation & Extraction
    waste_info = extract_waste_info(title)
    
    # 3. Search Pricing
    queries = generate_queries(f"harga {waste_info.jenis_sampah} per {waste_info.satuan} di indonesia 2024")
    research_context = ""
    for query in queries.queries:
        search_result = search_web(query)
        research_context += f"Query: {query} \n\n Search Result: {search_result}\n\n\n"

    # Price Extraction
    pricing_info = extract_pricing_info(research_context, waste_info.jenis_sampah)
    
    # 4. Store to Transaction Table
    with Session(engine) as session:
        transaction = SetorSampah(
            jenis_sampah=waste_info.jenis_sampah,
            berat=waste_info.berat,
            harga=pricing_info.harga
        )
        session.add(transaction)
        session.commit()
    
    # 5. Generate Report
    research_result = generate_report(title=title, research_context=research_context)
    if not research_result:
        raise ValueError("No Research Result Generated")

    # Generate markdown and PDF report
    result = markdown(text=research_result, output_format="html")
    os.makedirs("./reports", exist_ok=True)
    filename = f"./reports/{title.replace(' ', '_')}.pdf"
    HTML(string=result).write_pdf(filename)
    logger.info(f"Report generated: {filename}")


@celery.task
def research_task(title: str):
    logger.info(f"Research Task")
    research(title)