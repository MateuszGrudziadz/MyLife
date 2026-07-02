from fastapi import APIRouter, Request
from backend.app.core.templates import templates

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
async def hello(request: Request):
    return templates.TemplateResponse("hello.html", {"request": request, "hello": "Witaj na mojej stronie!"})

@router.get("/all")
def get_users():
    return {"users": ["siema"]}