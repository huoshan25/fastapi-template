from fastapi import Request, HTTPException

from src.core.auth import get_current_user
from src.core.interfaces.response import response


async def auth_middleware(request: Request, call_next):
    if request.url.path in ["/docs", "/redoc", "/user/token", "/openapi.json", "/user/login", "/user/register", "/user/refresh"]:
        return await call_next(request)

    token = request.headers.get("Authorization")
    if not token:
        return response(code=404, message="认证要求, 无token！")

    try:
        token_parts = token.split()
        if len(token_parts) != 2 or token_parts[0].lower() != "bearer":
            return response(code=404, message="无效的token格式")

        user = await get_current_user(token_parts[1])
        request.state.user = user
    except HTTPException as e:
        return response(code=404, message=f"错误-{e}")

    except Exception:
        return response(code=404, message="token错误！")

    return await call_next(request)


def add_auth_middleware(app):
    app.middleware("http")(auth_middleware)
