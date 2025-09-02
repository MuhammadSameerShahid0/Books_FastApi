from typing import Optional
from fastapi import FastAPI, APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.requests import Request
from Database import get_db
from Factory.factories import ServiceFactory
from Interfaces.IAuthService import IAuthService
from Schema import StudentSchema, AuthorSchema
from Schema.AuthSchema import Token
from Services.AuthService import AuthService

app = FastAPI()
AuthRouter = APIRouter(tags=["Auth"])

# DI provider
def get_auth_service(db: Session = Depends(get_db)) -> IAuthService:
    return ServiceFactory.get_services("auth", db)

Auth_Db_DI = Depends(get_auth_service)

@AuthRouter.get("/register_via_google")
async def register(request: Request, service: IAuthService = Auth_Db_DI):
    return await service.google_register(request)

@AuthRouter.get("/callback", response_model=Token)
async def callback(request: Request, service: IAuthService = Auth_Db_DI):
    return await service.google_callback(request)

@AuthRouter.post("/register_manually_Student", response_model=StudentSchema.StudentResponse)
async def register_student(
        request: StudentSchema.StudentCreate,
        services : IAuthService = Auth_Db_DI,
):
    return services.register_student(request)

@AuthRouter.post('/register_author_manually')
async def register_author(requests: AuthorSchema.CreateAuthor, service : IAuthService = Auth_Db_DI):
    return await service.register_author(requests)

@AuthRouter.get("/login_via_google", response_model=Token)
async def google_login(email: str, otp: Optional[str] = None, service : IAuthService = Auth_Db_DI):
    return  await service.google_login(email, otp)

@AuthRouter.get("/login", response_model=Token)
def login(email : str, otp: Optional[str] = None, service : IAuthService = Auth_Db_DI):
    return service.login(email, otp)