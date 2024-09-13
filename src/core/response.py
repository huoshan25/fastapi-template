from fastapi import status
from fastapi.responses import JSONResponse

from src.common.schemas import Response


def response(data=None, code=status.HTTP_200_OK, message="请求成功"):
    return JSONResponse(
        status_code=code,
        content=Response(code=code, data=data, message=message).dict()
    )
