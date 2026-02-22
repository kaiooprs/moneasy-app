from fastapi import APIRouter, Depends, HTTPException, status
from app.models.category import Category
from app.models.user import User
from app.core.security import get_current_user
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/categories", tags=["Categorias"])

class CategoryIn(BaseModel):
    name: str
    icon: str = "💰"
    color: str = "#4CAF50"

@router.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
async def create_category(cat_in: CategoryIn, current_user: User = Depends(get_current_user)):
    """Cria uma nova categoria vinculada ao usuário logado."""
    new_category = Category(
        **cat_in.model_dump(),
        owner_id=current_user
    )
    await new_category.insert()
    return new_category

@router.get("/", response_model=List[Category])
async def list_categories(current_user: User = Depends(get_current_user)):
    """Lista apenas as categorias que pertencem ao usuário autenticado."""
    return await Category.find(Category.owner_id.id == current_user.id).to_list()

@router.put("/{category_id}", response_model=Category)
async def update_category(category_id: str, cat_in: CategoryIn, current_user: User = Depends(get_current_user)):
    """Edita uma categoria existente (valida se o usuário é o dono)."""
    category = await Category.get(category_id)
    
    if not category or category.owner_id.ref.id != current_user.id:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    
    category.name = cat_in.name
    category.icon = cat_in.icon
    category.color = cat_in.color
    
    await category.save()
    return category

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: str, current_user: User = Depends(get_current_user)):
    """Exclui uma categoria (valida se o usuário é o dono)."""
    category = await Category.get(category_id)
    
    if not category or category.owner_id.ref.id != current_user.id:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    
    await category.delete()
    return None