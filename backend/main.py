from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db
from app.routes.wallets import router as wallet_router
from app.routes.users import router as user_router
from app.routes.transactions import router as transaction_router
from app.routes.categories import router as category_router
from app.routes.subscriptions import router as subscription_router
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.models.subscription import Subscription
from app.routes.analytics import router as analytics_router

async def reset_monthly_subscriptions():
    await Subscription.find(Subscription.is_paid).update({"$set": {"is_paid": False}})

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    
    scheduler = AsyncIOScheduler()
    scheduler.add_job(reset_monthly_subscriptions, 'cron', day=1, hour=0, minute=0)
    scheduler.start()
    
    yield
    
    scheduler.shutdown()

app = FastAPI(
    title="Moneasy API",
    description="Sistema de Gestão Financeira Pessoal",
    version="0.1.0",
    lifespan=lifespan
)

ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://moneasy-app-seven.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(wallet_router)
app.include_router(user_router)
app.include_router(transaction_router)
app.include_router(category_router)
app.include_router(subscription_router)
app.include_router(analytics_router)

@app.get("/")
async def root():
    return {
        "status": "online"
    }