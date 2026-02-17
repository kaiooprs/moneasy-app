from beanie import Document, Link
from app.models.user import User

class Category(Document):
    name: str          
    icon: str = "💰"    
    color: str = "#4CAF50"
    owner_id: Link[User] 

    class Settings:
        name = "categories"