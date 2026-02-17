from beanie import Document, Link
from app.models.user import User
from app.models.category import Category

class Subscription(Document):
    name: str
    amount: float
    due_day: int                # Dia do vencimento (1 a 31)
    is_paid: bool = False       # Para você marcar o que já pagou no mês
    category_id: Link[Category]
    owner_id: Link[User]

    class Settings:
        name = "subscriptions"