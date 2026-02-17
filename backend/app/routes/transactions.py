from fastapi import APIRouter, Depends, HTTPException, status
from app.models.transaction import Transaction, TransactionCreate
from app.models.wallet import Wallet
from app.models.category import Category
from app.models.user import User
from app.core.security import get_current_user
from typing import List

router = APIRouter(prefix="/transactions", tags=["Transações"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_expense(t_in: TransactionCreate, current_user: User = Depends(get_current_user)):
    """Registra um gasto e abate o valor do saldo da carteira."""
    wallet = await Wallet.get(t_in.wallet_id)
    category = await Category.get(t_in.category_id)
    
    if not wallet or wallet.owner_id.ref.id != current_user.id:
        raise HTTPException(status_code=404, detail="Carteira não encontrada")
    
    if not category or category.owner_id.ref.id != current_user.id:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")

    wallet.balance -= t_in.amount
    await wallet.save()

    new_transaction = Transaction(
        description=t_in.description,
        amount=t_in.amount,
        wallet_id=wallet,
        owner_id=current_user,
        category_id=category
    )
    await new_transaction.insert()
    return new_transaction

@router.get("/", response_model=List[Transaction])
async def list_expenses(current_user: User = Depends(get_current_user)):
    """
    Lista os gastos do usuário resolvendo os links manualmente.
    Essa versão evita o bug de cursor do Motor/Beanie no Python 3.13.
    """
    transactions = await Transaction.find(
        Transaction.owner_id.id == current_user.id
    ).sort("-date").to_list()
    
    for t in transactions:
        if t.wallet_id:
            t.wallet_id = await Wallet.find_one(Wallet.id == t.wallet_id.ref.id)
        
        if t.category_id:
            t.category_id = await Category.find_one(Category.id == t.category_id.ref.id)
            
    return transactions

@router.put("/{transaction_id}", response_model=Transaction)
async def update_expense(
    transaction_id: str, 
    t_in: TransactionCreate, 
    current_user: User = Depends(get_current_user)
):
    t = await Transaction.get(transaction_id)
    if not t or t.owner_id.ref.id != current_user.id:
        raise HTTPException(status_code=404, detail="Gasto não encontrado")

    old_amount = t.amount
    
    wallet = await Wallet.get(t.wallet_id.ref.id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Carteira original não encontrada")

    wallet.balance = (wallet.balance + old_amount) - t_in.amount
    
    if t.wallet_id.ref.id != t_in.wallet_id:
        pass 

    t.description = t_in.description
    t.amount = t_in.amount
    t.category_id = await Category.get(t_in.category_id)
    
    await wallet.save()
    await t.save()
    
    return t

@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(transaction_id: str, current_user: User = Depends(get_current_user)):
    """Exclui um gasto resolvendo a carteira manualmente para o estorno."""
    t = await Transaction.get(transaction_id)
    
    if not t or t.owner_id.ref.id != current_user.id:
        raise HTTPException(status_code=404, detail="Gasto não encontrado")

    wallet = await Wallet.get(t.wallet_id.ref.id)
    if wallet:
        wallet.balance += t.amount
        await wallet.save()
    
    await t.delete()
    return None