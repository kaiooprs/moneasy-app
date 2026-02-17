from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import User
from app.core.auth import get_password_hash, verify_password, create_access_token
from app.core.security import get_current_user
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["Autenticação"])

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate):
    """
    Cria um novo usuário. 
    O e-mail é gerado automaticamente para simplificar o MVP.
    """
    user_exists = await User.find_one(User.username == user_in.username)
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Este nome de usuário já está em uso."
        )
    
    hashed_password = get_password_hash(user_in.password)
    new_user = User(
        username=user_in.username,
        email=f"{user_in.username}@moneasy.com",
        password_hash=hashed_password
    )
    await new_user.insert()
    return {"message": "Usuário criado com sucesso! Agora você pode fazer login."}

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Rota de Login compatível com o botão 'Authorize' do Swagger.
    Retorna um token JWT válido por 30 dias.
    """
    user = await User.find_one(User.username == form_data.username)
    
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    """
    Retorna os dados do usuário logado.
    """
    return {
        "id": str(current_user.id),
        "username": current_user.username,
        "email": current_user.email,
        "created_at": current_user.created_at
    }