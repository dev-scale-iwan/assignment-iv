from pydantic import BaseModel, Field


class ResearchInput(BaseModel):
    topic: str


class QueriesSchema(BaseModel):
    queries: list[str] = Field(description="List of queries to be searched")