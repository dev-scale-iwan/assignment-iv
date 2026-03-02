import uuid
from sqlmodel import SQLModel, Field

class SetorSampah(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    tabungan_id: uuid.UUID = Field(default=None)
    jenis_sampah: str = Field(default=None)
    berat: float = Field(default=0.0)
    harga: float = Field(default=0.0)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)