from fastapi import APIRouter

from app.api.endpoints import users, items

api_router = APIRouter()
api_router.include_router(users.router, tags=["users"], prefix="/users") # tagsやprefixは設計に応じて付与
api_router.include_router(items.router, tags=["items"], prefix="/items")