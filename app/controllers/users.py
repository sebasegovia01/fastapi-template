from fastapi import APIRouter, HTTPException, status
from app.models.users import User
from app.services.users import get_user_by_id, get_all_users, create_user, update_user, delete_user

# Crear un nuevo router específico para las operaciones de usuario
router = APIRouter()

@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    user = await get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.get("/users/", response_model=list[User])
async def get_all_users_endpoint():
    users = await get_all_users()
    return users

@router.post("/users/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_new_user(user: User):
    created_user = await create_user(user)
    return created_user

@router.put("/users/{user_id}", response_model=User)
async def update_existing_user(user_id: int, user: User):
    updated_user = await update_user(user_id, user)
    if updated_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return updated_user

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_user(user_id: int):
    result = await delete_user(user_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message": "User deleted successfully"}

