from fastapi import APIRouter, Depends, HTTPException, status
from app.models.subscription import Subscription
from app.models.wallet import Wallet
from app.models.transaction import Transaction
from app.models.category import Category
from app.models.user import User
from app.core.security import get_current_user
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/subscriptions", tags=["Assinaturas & Fixos"])

class SubscriptionCreate(BaseModel):
    name: str
    amount: float
    due_day: int
    category_id: str

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_subscription(sub_in: SubscriptionCreate, current_user: User = Depends(get_current_user)):
    category = await Category.get(sub_in.category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    
    sub_data = sub_in.model_dump(exclude={"category_id"})
    
    new_sub = Subscription(
        **sub_data,             
        owner_id=current_user,
        category_id=category 
    )
    await new_sub.insert()
    return new_sub

@router.get("/", response_model=List[Subscription])
async def list_subscriptions(current_user: User = Depends(get_current_user)):
    subs = await Subscription.find(Subscription.owner_id.id == current_user.id).to_list()
    
    for s in subs:
        if s.category_id:
            s.category_id = await Category.get(s.category_id.ref.id)
            
    return subs

@router.post("/{sub_id}/pay")
async def pay_subscription(sub_id: str, wallet_id: str, current_user: User = Depends(get_current_user)):
    """O botão 'Pagar': Abate do saldo e gera uma transação."""
    sub = await Subscription.get(sub_id)
    wallet = await Wallet.get(wallet_id)
    
    if not sub or sub.owner_id.ref.id != current_user.id:
        raise HTTPException(status_code=404, detail="Assinatura não encontrada")
    if not wallet or wallet.owner_id.ref.id != current_user.id:
        raise HTTPException(status_code=404, detail="Carteira não encontrada")

    wallet.balance -= sub.amount
    await wallet.save()

    new_expense = Transaction(
        description=f"Pagamento: {sub.name}",
        amount=sub.amount,
        wallet_id=wallet,
        owner_id=current_user,
        category_id=sub.category_id,
        type="expense"
    )
    await new_expense.insert()
    
    sub.is_paid = True
    await sub.save()

    return {"message": f"{sub.name} pago com sucesso!", "new_balance": wallet.balance}

@router.delete("/{sub_id}", status_code=204)
async def delete_subscription(sub_id: str, current_user: User = Depends(get_current_user)):
    sub = await Subscription.get(sub_id)
    if not sub or sub.owner_id.ref.id != current_user.id:
        raise HTTPException(status_code=404, detail="Assinatura não encontrada")
    await sub.delete()
    return None

@router.put("/{sub_id}", response_model=Subscription)
async def update_subscription(
    sub_id: str, 
    sub_in: SubscriptionCreate, 
    current_user: User = Depends(get_current_user)
):
    """Atualiza os dados da assinatura para os próximos pagamentos."""
    sub = await Subscription.get(sub_id)
    
    if not sub or sub.owner_id.ref.id != current_user.id:
        raise HTTPException(status_code=404, detail="Assinatura não encontrada")
    
    category = await Category.get(sub_in.category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")

    sub.name = sub_in.name
    sub.amount = sub_in.amount
    sub.due_day = sub_in.due_day
    sub.category_id = category
    
    await sub.save()
    return sub