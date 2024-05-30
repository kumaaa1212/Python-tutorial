from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status
from app.services.auth import main as auth_service
from app.schemas.main import UserCeate, UserResponse, Token
from database import get_db
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["auth"])

DbDepend = Annotated[Session, Depends(get_db)]
# FormDepend = Annotated[OAuth2PasswordRequestForm, Depends(OAuth2PasswordRequestForm)]
# Annotatedに渡す型とDependsに渡す型がおなじばあいは、Dependsに渡す型を省略できる
FormDepend = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post(
    "/singup", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def singup(db: DbDepend, user_create: UserCeate):
    return auth_service.create_user(db, user_create)


@router.post(
    "/login",
    response_model=Token,
    status_code=status.HTTP_200_OK,
)
async def login(db: DbDepend, form_data: FormDepend):
    user = auth_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    token = auth_service.create_access_token(
        user.username, user.id, timedelta(minutes=20)
    )
    return {"access_token": token, "token_type": "bearer"}


# token_typeはtokenの種類を表す文字列で、bearerを指定することが多い
