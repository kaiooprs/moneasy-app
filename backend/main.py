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
    print("🔄 Reiniciando ciclo de assinaturas para o novo mês...")
    await Subscription.find(Subscription.is_paid).update({"$set": {"is_paid": False}})
    print("✅ Todas as assinaturas foram marcadas como 'Não Pagas'.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Iniciando conexão com o MongoDB...")
    await init_db()
    
    print("📅 Iniciando agendador de tarefas (Scheduler)...")
    scheduler = AsyncIOScheduler()
    scheduler.add_job(reset_monthly_subscriptions, 'cron', day=1, hour=0, minute=0)
    scheduler.start()
    
    yield
    
    print("🛑 Encerrando agendador e conexões...")
    scheduler.shutdown()
    print("✅ Backend Moneasy desligado com segurança.")

app = FastAPI(
    title="Moneasy API",
    description="Sistema de Gestão Financeira Pessoal",
    version="0.1.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
        "status": "online",
        "app": "Moneasy",
        "owner": "Remi",
        "message": "Backend rodando perfeitamente!"
    }