from pydantic import BaseModel, Field


class ResearchInput(BaseModel):
    input: str = Field(..., examples=["Selvi setor sampah plastik 2 kg"])


class QueriesSchema(BaseModel):
    queries: list[str] = Field(description="List of queries to be searched")


class WasteExtraction(BaseModel):
    nama: str = Field(description="Name of the user, set default to 'Umum' if not specified", default="Umum")
    jenis_sampah: str = Field(description="Type of waste")
    berat: float = Field(description="Weight of waste")
    satuan: str = Field(description="Unit of measurement")

class PriceExtraction(BaseModel):
    harga: float = Field(description="Price per unit")
    satuan: str = Field(description="Unit of price")