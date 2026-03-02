import uuid
from sqlmodel import SQLModel, Field
from datetime import datetime

class Tabungan(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    nama: str = Field(default=None)
    saldo: float = Field(default=0.0)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)