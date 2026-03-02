from pydantic import BaseModel

class TabunganRequest(BaseModel):
    nama: str
    saldo: float | None = None

class TabunganResponse(BaseModel):
    id: str
    nama: str
    saldo: float | None = None