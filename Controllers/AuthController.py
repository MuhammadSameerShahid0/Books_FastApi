import datetime
import os
from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status
from starlette.requests import Request
from OAuthandJwt.JWTToken import create_jwt
from Models import User
from Database import get_db
from OAuthandJwt.oauth_config import google_oauth
from Schema.AuthSchema import Token

app = FastAPI()
AuthRouter = APIRouter(tags=["Auth"])

@AuthRouter.get("/register_via_google")
async def register(request: Request):
    try:
        redirect_uri = os.getenv("REDIRECT_URI")
        if not redirect_uri:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Redirect URI not configured"
            )
        return await google_oauth.google.authorize_redirect(request, redirect_uri)
    except Exception as ex:
        code = getattr(ex, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
        if isinstance(ex, HTTPException):
            raise ex

        raise HTTPException(
            status_code=code,
            detail=str(ex)
        )


@AuthRouter.get("/callback", response_model=Token)
async def callback(request: Request, db : Session = Depends(get_db)):
    try:
        token = await google_oauth.google.authorize_access_token(request)
        if not token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to fetch access token"
            )

        user_info = token["userinfo"]
        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to fetch user info"
            )

        user = db.query(User).filter(User.google_id == user_info['sub']).first()
        if not user:
            user = User(
                google_id=user_info['sub'],
                name=user_info['name'],
                email=user_info['email'],
                picture=user_info['picture'],
                user_created_at = datetime.datetime.now()
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        token = create_jwt({"email": user.email, "name" : user.name, "from_project": "OAuth2.0 FastAPI"})
        return {"access_token" : token , "token_type" : "bearer" }
    except Exception as ex:
        code=getattr(ex, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
        if isinstance(ex, HTTPException):
            raise ex

        raise HTTPException(
            status_code=code,
            detail=str(ex)
        )
