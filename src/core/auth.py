from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette.responses import JSONResponse

from src.core.jwt import JWTTokenManager
from src.core.interfaces.response import response
from src.modules.user.models import User
from src.modules.user.schemas.user import UserInDB

# 创建OAuth2PasswordBearer实例，用于处理token的依赖
# tokenUrl指定了获取token的endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")

# 创建JWTTokenManager实例，用于处理JWT token的操作
token_manager = JWTTokenManager()


async def get_refresh_token(token: str = Depends(oauth2_scheme)) -> str:
    """
    从请求中获取刷新token。

    这个函数作为一个依赖项，用于从请求的Authorization头中提取刷新token。
    它处理了带有"Bearer "前缀的token，如果存在前缀则去除。

    Args:
        token (str): 从请求中提取的token，由oauth2_scheme依赖提供。

    Returns:
        str: 处理后的刷新token。
    """
    if token.startswith("Bearer "):
        return token[7:]
    return token


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    验证token并获取当前用户。

    这个函数作为一个依赖项，用于验证提供的token，并返回对应的用户信息。
    如果token无效或用户不存在，则抛出相应的错误响应。

    Args:
        token (str): 从请求中提取的token，由oauth2_scheme依赖提供。

    Returns:
        UserInDB: 当前认证用户的信息。

    Raises:
        HTTPException: 当token无效或用户不存在时抛出。
    """
    try:
        # 验证token
        token_data = token_manager.verify_token(token)
        # 根据token中的用户名查找用户
        user = await User.get_or_none(username=token_data.username)
        if user is None:
            raise HTTPException(status_code=401, detail="未找到用户")
        # 返回用户信息
        return await UserInDB.from_tortoise_orm(user)
    except Exception:
        # raise HTTPException(status_code=401, detail="无法验证凭据")
        raise response(code=404, message="无法验证凭据")
