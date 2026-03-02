from pydantic import BaseModel, Field


class ResearchInput(BaseModel):
    input: str


class QueriesSchema(BaseModel):
    queries: list[str] = Field(description="List of queries to be searched")


class WasteExtraction(BaseModel):
    jenis_sampah: str = Field(description="Type of waste")
    berat: float = Field(description="Weight of waste")
    satuan: str = Field(description="Unit of measurement")

class PriceExtraction(BaseModel):
    harga: float = Field(description="Price per unit")
    satuan: str = Field(description="Unit of price")