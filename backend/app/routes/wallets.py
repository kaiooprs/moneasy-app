from fastapi import APIRouter, Depends, HTTPException
from app.models.wallet import Wallet, WalletCreate, WalletType
from app.models.user import User
from app.core.security import get_current_user
from typing import List
from pydantic import BaseModel

router = APIRouter(prefix="/wallets", tags=["Carteiras"])

class BalanceUpdate(BaseModel):
    amount: float

@router.post("/", response_model=Wallet)
async def create_wallet(wallet_in: WalletCreate, current_user: User = Depends(get_current_user)):
    new_wallet = Wallet(
        **wallet_in.model_dump(), 
        owner_id=current_user
    )
    await new_wallet.insert()
    return new_wallet

@router.get("/", response_model=List[Wallet])
async def list_wallets(current_user: User = Depends(get_current_user)):
    return await Wallet.find(Wallet.owner_id.id == current_user.id).to_list()

@router.put("/{wallet_id}", response_model=Wallet)
async def update_wallet(wallet_id: str, wallet_in: WalletCreate, current_user: User = Depends(get_current_user)):
    wallet = await Wallet.get(wallet_id)
    if not wallet or wallet.owner_id.ref.id != current_user.id:
        raise HTTPException(status_code=404, detail="Carteira não encontrada")
    
    wallet.name = wallet_in.name
    wallet.balance = wallet_in.balance
    wallet.color = wallet_in.color
    wallet.description = wallet_in.description
    
    await wallet.save()
    return wallet

@router.delete("/{wallet_id}", status_code=204)
async def delete_wallet(wallet_id: str, current_user: User = Depends(get_current_user)):
    wallet = await Wallet.get(wallet_id)
    if not wallet or wallet.owner_id.ref.id != current_user.id:
        raise HTTPException(status_code=404, detail="Carteira não encontrada")
    
    await wallet.delete()
    return None

@router.patch("/{wallet_id}/add-balance", response_model=Wallet)
async def add_balance(wallet_id: str, update: BalanceUpdate, current_user: User = Depends(get_current_user)):
    wallet = await Wallet.get(wallet_id)
    if not wallet or wallet.owner_id.ref.id != current_user.id:
        raise HTTPException(status_code=404, detail="Carteira não encontrada")
    
    wallet.balance += update.amount
    await wallet.save()
    return wallet

@router.get("/summary")
async def get_wallet_summary(current_user: User = Depends(get_current_user)):
    """Calcula o Saldo Disponível vs. Reserva de Emergência."""
    wallets = await Wallet.find(Wallet.owner_id.id == current_user.id).to_list()
    
    disponivel = sum(w.balance for w in wallets if w.type == WalletType.CORRENTE)
    reserva = sum(w.balance for w in wallets if w.type == WalletType.POUPANCA)
    
    return {
        "saldo_disponivel": disponivel,
        "reserva_total": reserva,
        "total_geral": disponivel + reserva
    }