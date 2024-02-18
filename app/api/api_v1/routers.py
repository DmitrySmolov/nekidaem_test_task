from fastapi import APIRouter

from app.api.api_v1.endpoints import blogs_router, users_router

main_router = APIRouter(prefix='/api/v1')

main_router.include_router(
    router=users_router,
    prefix='/users',
    tags=['users']
)

main_router.include_router(
    router=blogs_router,
    prefix='/blogs',
    tags=['blogs']
)
