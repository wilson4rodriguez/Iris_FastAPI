from fastapi import APIRouter
from controllers.todo_controllers import router as todo_router

router= APIRouter()
router.include_router(todo_router)