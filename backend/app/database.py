from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models.wallet import Wallet
from app.models.user import User
from app.models.transaction import Transaction
from app.models.category import Category
from app.models.subscription import Subscription

import os
from dotenv import load_dotenv

load_dotenv()

async def init_db():
    # Puxa a URL do .env ou usa o padrão local
    # No Docker, o padrão é mongodb://localhost:27017/nome_do_banco
    DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017/moneasy")
    
    client = AsyncIOMotorClient(DATABASE_URL)
    
    # Inicializa o Beanie com a lista de modelos
    await init_beanie(
        database=client.get_default_database(), 
        document_models=[User, Wallet, Transaction, Category, Subscription]
    )
    print("✅ Conectado ao MongoDB: Moneasy Mode On")