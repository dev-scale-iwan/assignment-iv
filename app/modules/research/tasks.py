import os
from markdown import markdown
from datetime import datetime
from weasyprint import HTML

from celery.utils.log import get_task_logger
from app.celery import celery
from app.modules.research.methods import extract_waste_info, generate_queries, search_web, extract_pricing_info, generate_report
from app.models.setorsampah import SetorSampah
from app.models.tabungan import Tabungan
from app.core.db import engine
from sqlmodel import Session, select

logger = get_task_logger(__name__)


def setorsampah(title: str):
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
    total_harga = waste_info.berat * pricing_info.harga
    
    # 4. Store to Transaction Tables
    with Session(engine) as session:
        # Find or create tabungan
        statement = select(Tabungan).where(Tabungan.nama == waste_info.nama)
        tabungan = session.exec(statement).first()
        
        if not tabungan:
            tabungan = Tabungan(nama=waste_info.nama, saldo=0.0)
            session.add(tabungan)
            session.commit()
            session.refresh(tabungan)
        
        # Update Tabungan balance
        tabungan.saldo += total_harga
        tabungan.updated_at = datetime.now()
        session.add(tabungan)

        # Create SetorSampah transaction
        transaction = SetorSampah(
            tabungan_id=tabungan.id,
            jenis_sampah=waste_info.jenis_sampah,
            berat=waste_info.berat,
            harga=pricing_info.harga
        )
        session.add(transaction)
        session.commit()
    
    # 5. Generate Report
    research_result = generate_report(
        title=title, 
        research_context=research_context, 
        current_date=str(datetime.now())
    )
    if not research_result:
        raise ValueError("No Research Result Generated")

    # Generate markdown and PDF report
    result = markdown(text=research_result, extensions=['tables'], output_format="html")
    os.makedirs("./reports", exist_ok=True)
    filename = f"./reports/{title.replace(' ', '_')}.pdf"
    HTML(string=result).write_pdf(filename)
    logger.info(f"Report generated: {filename}")


@celery.task
def setorsampah_task(title: str):
    logger.info(f"Setor Sampah Task")
    setorsampah(title)