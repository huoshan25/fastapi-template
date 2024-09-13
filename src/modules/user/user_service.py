from fastapi import Depends, status
from tortoise.exceptions import IntegrityError

from src.core.security import PasswordManager, BcryptPasswordManager
from src.core.jwt import TokenManager, JWTTokenManager
from src.core.log_config import api_logger, error_logger
from src.core.response import response
from src.modules.user.models import User
from src.modules.user.schemas.user import UserCreate, UserLogin, UserInDB


class UserService:
    """
    用户服务类，处理用户相关的业务逻辑。

    这个类负责用户的创建、认证、获取用户信息以及刷新令牌等操作。
    它依赖于密码管理器和令牌管理器来处理密码加密和JWT令牌操作。
    """

    def __init__(
            self,
            password_manager: PasswordManager = Depends(BcryptPasswordManager),
            token_manager: TokenManager = Depends(JWTTokenManager)
    ):
        """
        初始化UserService实例。

        Args:
            password_manager (PasswordManager): 用于处理密码加密和验证的管理器。
            token_manager (TokenManager): 用于处理JWT令牌的创建和验证的管理器。
        """
        self.password_manager = password_manager
        self.token_manager = token_manager

    async def create_user(self, user: UserCreate):
        """
        创建新用户。

        Args:
            user (UserCreate): 包含用户创建信息的模型。

        Returns:
            dict: 包含创建结果的响应。如果成功，返回用户ID和用户名；如果失败，返回错误信息。

        Raises:
            IntegrityError: 当尝试创建已存在的用户名时抛出。
        """
        hashed_password = self.password_manager.hash_password(user.password)
        try:
            new_user = await User.create(
                username=user.username,
                password=hashed_password,
            )
            return response(message="用户创建成功", data={"id": new_user.id, "username": new_user.username})
        except IntegrityError as e:
            if "username" in str(e):
                return response(code=404, message="用户名已存在")
            else:
                return response(code=404, message="未知错误")

    async def authenticate_user(self, user: UserLogin):
        """
        验证用户登录。

        Args:
            user (UserLogin): 包含登录信息的模型。

        Returns:
            dict: 包含认证结果的响应。如果成功，返回访问令牌和刷新令牌；如果失败，返回错误信息。
        """
        db_user = await User.get_or_none(username=user.username)

        if db_user is None:
            return response(code=404, message="用户名不存在！")

        if self.password_manager.verify_password(user.password, db_user.password):
            access_token = self.token_manager.create_access_token(data={"sub": db_user.username})
            refresh_token = self.token_manager.create_refresh_token(data={"sub": user.username})
            # 确保令牌是字符串类型
            if isinstance(access_token, bytes):
                access_token = access_token.decode('utf-8')
            if isinstance(refresh_token, bytes):
                refresh_token = refresh_token.decode('utf-8')

            data = {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer"
            }
            api_logger.info(f"用户登录成功: {user.username}")
            return response(data=data, message="登录成功！")
        else:
            error_logger.error(f'用户登录失败: {user.username}')
            return response(code=404, message="密码错误！")

    async def get_current_user(self, token: str):
        """
        获取当前认证用户的信息。

        Args:
            token (str): JWT访问令牌。

        Returns:
            UserInDB: 当前用户的信息。

        Raises:
            HTTPException: 当令牌无效或用户不存在时抛出。
        """
        try:
            token_data = self.token_manager.verify_token(token)
            user = await User.get_or_none(username=token_data.username)
            if user is None:
                raise response(code=status.HTTP_404_NOT_FOUND, message="未找到用户")
            return await UserInDB.from_tortoise_orm(user)
        except Exception as e:
            raise response(code=status.HTTP_401_UNAUTHORIZED, message=f"无法验证凭据, {e}")

    async def refresh_token(self, refresh_token: str):
        """
        刷新访问令牌。

        Args:
            refresh_token (str): 用于刷新的令牌。

        Returns:
            dict: 包含新的访问令牌和刷新令牌的响应。

        Raises:
            ValueError: 当刷新令牌无效时抛出。
        """
        try:
            new_access_token, new_refresh_token = self.token_manager.refresh_tokens(refresh_token)
            return response(
                data={
                    "access_token": new_access_token,
                    "refresh_token": new_refresh_token,
                    "token_type": "bearer"
                },
                message="令牌刷新成功"
            )
        except ValueError:
            return response(code=status.HTTP_401_UNAUTHORIZED, message="无效的刷新令牌")