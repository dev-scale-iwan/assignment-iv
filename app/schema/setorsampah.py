from pydantic import BaseModel

class SetorSampahRequest(BaseModel):
    tabungan_id: str
    jenis_sampah: str
    berat: float
    harga: float | None = None

class SetorSampahResponse(BaseModel):
    id: str
    tabungan_id: str
    jenis_sampah: str
    berat: float
    harga: float | None = None