import json
import logging


from app.utils.openapi import open_ai_client
from app.utils.tavily import tavily_client

from .prompt import REPORT_SYSTEM_PROMPT
from .schema import QueriesSchema

logger = logging.getLogger(__name__)

def generate_queries(topic: str) -> QueriesSchema:
    response = open_ai_client.chat.completions.parse(
        model="google/gemini-3-flash-preview",
        messages=[
            {"role": "system", "content": "Generate 5 queries to search into the web based on user topic"},
            {"role": "user", "content": f"Topic: {topic}"},
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

    print(f"Results: {results}")

    response = open_ai_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": "Summarize this into informative content, please include data, numbers and url/sources"},
            {"role": "user", "content": f"Search Result: {json.dumps(results)}"},
        ],
        extra_body={"reasoning": {"enabled": True}},
    )


    return response.choices[0].message.content


def generate_report(topic: str, research_context: str):
    response = open_ai_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": REPORT_SYSTEM_PROMPT.format(research_context=research_context)},
            {"role": "user", "content": f"Topic: {topic}"},
        ],
        extra_body={"reasoning": {"enabled": True}},
    )

    return response.choices[0].message.content
