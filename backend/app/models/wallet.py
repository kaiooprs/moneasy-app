from beanie import Document, Link
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from enum import Enum
from app.models.user import User

class WalletType(str, Enum):
    CORRENTE = "corrente"
    POUPANCA = "poupanca"

class WalletCreate(BaseModel):
    name: str
    balance: float = 0.0
    type: WalletType = WalletType.CORRENTE
    goal: float = 0.0
    color: str = "#EAB308"
    description: str | None = None

class Wallet(Document):
    name: str
    balance: float
    type: WalletType = WalletType.CORRENTE
    goal: float = 0.0                      
    color: str = "#EAB308"
    description: str = ""
    owner_id: Link[User]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "wallets"