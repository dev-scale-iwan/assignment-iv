import json
import logging


from app.utils.openapi import open_ai_client
from app.utils.tavily import tavily_client

from .prompt import REPORT_SYSTEM_PROMPT
from .schema import QueriesSchema, WasteExtraction, PriceExtraction

logger = logging.getLogger(__name__)

def extract_pricing_info(research_context: str, jenis_sampah: str) -> PriceExtraction:
    print(f"Extracting price for: {jenis_sampah}")
    response = open_ai_client.chat.completions.parse(
        model="google/gemini-3.1-pro-preview",
        messages=[
            {"role": "system", "content": "Extract the best current price for the given waste type from the context."},
            {"role": "user", "content": f"Waste Type: {jenis_sampah} \n\n Context: {research_context}"},
        ],
        response_format=PriceExtraction,
    )

    if not response:
        raise ValueError("No response from OpenAI for pricing extraction")
    
    parsed_data = response.choices[0].message.parsed.model_dump()
    logger.info(f"Extracted Price: {parsed_data}")
    
    return PriceExtraction(**parsed_data)

def extract_waste_info(user_input: str) -> WasteExtraction:
    print(f"Extracting waste info for: {user_input}")
    response = open_ai_client.chat.completions.parse(
        model="google/gemini-3-flash-preview",
        messages=[
            {"role": "system", "content": "Extract waste information (type, weight, and unit) from user input"},
            {"role": "user", "content": f"Input: {user_input}"},
        ],
        response_format=WasteExtraction,
    )

    if not response:
        raise ValueError("No response from OpenAI for extraction")
    
    parsed_data = response.choices[0].message.parsed.model_dump()
    logger.info(f"Extracted info: {parsed_data}")
    
    return WasteExtraction(**parsed_data)

def generate_queries(title: str) -> QueriesSchema:
    print(f"Generating queries for topic: {title}")
    response = open_ai_client.chat.completions.parse(
        model="google/gemini-3-flash-preview",
        messages=[
            {"role": "system", "content": "Generate 1 queries to search into the web based on user topic"},
            {"role": "user", "content": f"Topic: {title}"},
        ],
        response_format=QueriesSchema,
    )

    if not response:
        raise ValueError("No response from OpenAI")
    
    parsed_data = response.choices[0].message.parsed.model_dump()
    logger.info(f"Generated queries: {parsed_data}")
    
    return QueriesSchema(**parsed_data)

def search_web(query: str) -> str:
    results = tavily_client.search(query=query, search_depth="advanced", include_raw_content="markdown")

    print(f"Search Web : {results}")

    response = open_ai_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": "Summarize this into informative content, please include data, numbers and url/sources"},
            {"role": "user", "content": f"Search Result: {json.dumps(results)}"},
        ],
        extra_body={"reasoning": {"enabled": True}},
    )


    return response.choices[0].message.content


def generate_report(title: str, research_context: str):
    print(f"Generating report for topic: {title}")
    response = open_ai_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": REPORT_SYSTEM_PROMPT.format(research_context=research_context)},
            {"role": "user", "content": f"Topic: {title}"},
        ],
        extra_body={"reasoning": {"enabled": True}},
    )

    return response.choices[0].message.content
