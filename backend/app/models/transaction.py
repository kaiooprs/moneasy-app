from beanie import Document, Link
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from app.models.user import User
from app.models.wallet import Wallet
from app.models.category import Category

class TransactionCreate(BaseModel):
    description: str
    amount: float
    wallet_id: str 
    category_id: str

class Transaction(Document):
    description: str
    amount: float
    wallet_id: Link[Wallet]
    owner_id: Link[User]
    category_id: Link[Category]
    date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "transactions"