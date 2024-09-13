from fastapi import APIRouter, Depends

from src.core.auth import get_current_user, get_refresh_token
from src.core.log import log_api_call
from src.core.response import response
from src.modules.user.schemas.user import UserCreate, UserLogin
from src.modules.user.user_service import UserService


class UserController:
    def __init__(self):
        self.router = APIRouter(prefix="/user", tags=["用户模块"])

        @self.router.post("/register", summary="注册")
        async def register_user(user: UserCreate, user_service: UserService = Depends(UserService)):
            return await user_service.create_user(user)

        @self.router.post("/login", summary="登录")
        # @log_api_call
        async def login_user(user: UserLogin, user_service: UserService = Depends(UserService)):
            return await user_service.authenticate_user(user)

        @self.router.post("/refresh", summary="刷新访问令牌")
        async def refresh_token_route(
            refresh_token: str = Depends(get_refresh_token),
            user_service: UserService = Depends(UserService)
        ):
            return await user_service.refresh_token(refresh_token)

        @self.router.get("/userInfo", summary="获取当前用户信息")
        async def get_current_user_info(current_user=Depends(get_current_user)):
            return response(data=current_user)

        @self.router.get("/test", summary="测试")
        async def get_current_user2():
            return response(code=404, message="你可以啊")
