from fastapi import APIRouter, Depends, Query
from app.models.transaction import Transaction
from app.models.category import Category
from app.models.wallet import Wallet, WalletType
from app.models.user import User
from app.core.security import get_current_user
from datetime import datetime, timezone

router = APIRouter(prefix="/analytics", tags=["Inteligência Financeira"])

@router.get("/spending-by-category")
async def get_spending_by_category(
    month: int = Query(default=datetime.now().month),
    year: int = Query(default=datetime.now().year),
    current_user: User = Depends(get_current_user)
):
    """Retorna quanto foi gasto em cada categoria com correção de cursor para Python 3.13."""
    # 1. Datas em UTC para o MongoDB
    start_date = datetime(year, month, 1, tzinfo=timezone.utc)
    if month == 12:
        end_date = datetime(year + 1, 1, 1, tzinfo=timezone.utc)
    else:
        end_date = datetime(year, month + 1, 1, tzinfo=timezone.utc)

    # 2. Pipeline de agregação
    pipeline = [
        {
            "$match": {
                # Beanie armazena Links como DBRefs, então usamos .id ou .$id
                "owner_id.$id": current_user.id, 
                "date": {"$gte": start_date, "$lt": end_date}
            }
        },
        {
            "$group": {
                "_id": "$category_id.$id",
                "total": {"$sum": "$amount"},
                "count": {"$sum": 1}
            }
        },
        {"$sort": {"total": -1}}
    ]

    # 3. BYPASS: Usamos a coleção bruta do Motor para evitar o bug do Beanie
    collection = Transaction.get_pymongo_collection()
    cursor = collection.aggregate(pipeline) # Aqui não usamos await
    results = await cursor.to_list(length=None) # Aqui usamos await no cursor direto
    
    # 4. Resolução manual de categorias
    formatted = []
    for item in results:
        cat = await Category.get(item["_id"])
        formatted.append({
            "name": cat.name if cat else "Outros",
            "icon": cat.icon if cat else "❓",
            "color": cat.color if cat else "#ccc",
            "total": item["total"],
            "count": item["count"]
        })
    return formatted

@router.get("/monthly-overview")
async def get_monthly_overview(
    month: int = Query(default=datetime.now().month),
    year: int = Query(default=datetime.now().year),
    current_user: User = Depends(get_current_user)
):
    """Resumo geral: Saldo total disponível vs. Gasto total do mês."""
    wallets = await Wallet.find(Wallet.owner_id.id == current_user.id).to_list()
    total_disponivel = sum(w.balance for w in wallets if w.type == WalletType.CORRENTE)
    
    start_date = datetime(year, month, 1, tzinfo=timezone.utc)
    if month == 12:
        end_date = datetime(year + 1, 1, 1, tzinfo=timezone.utc)
    else:
        end_date = datetime(year, month + 1, 1, tzinfo=timezone.utc)

    gastos = await Transaction.find(
        Transaction.owner_id.id == current_user.id,
        Transaction.date >= start_date,
        Transaction.date < end_date
    ).to_list()
    
    total_gasto = sum(g.amount for g in gastos)

    return {
        "month": month,
        "year": year,
        "available_balance": total_disponivel,
        "total_spent": total_gasto,
        "transaction_count": len(gastos)
    }
    
    
@router.get("/emergency-reserve")
async def get_emergency_reserve_progress(current_user: User = Depends(get_current_user)):
    """
    Calcula o progresso da reserva de emergência (contas POUPANCA).
    """
    savings_wallets = await Wallet.find(
        Wallet.owner_id.id == current_user.id,
        Wallet.type == WalletType.POUPANCA
    ).to_list()

    total_saved = sum(w.balance for w in savings_wallets)
    total_goal = sum(w.goal for w in savings_wallets)
    
    progress_percentage = (total_saved / total_goal * 100) if total_goal > 0 else 0

    return {
        "total_saved": total_saved,
        "total_goal": total_goal,
        "progress_percentage": round(progress_percentage, 2),
        "wallets": [
            {
                "name": w.name,
                "balance": w.balance,
                "goal": w.goal,
                "color": w.color
            } for w in savings_wallets
        ]
    }