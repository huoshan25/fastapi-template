from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src.common.schemas import Response


def response(data=None, code=status.HTTP_200_OK, message=None):
    """
    统一接口的响应结构。

    该函数用于生成统一格式的JSON响应，包含响应码、数据和消息。

    参数:
    - data (Any): 响应的数据，默认为None。
    - code (int): HTTP状态码，默认为200（HTTP_200_OK）。
    - message (str): 响应的消息，默认为"请求成功"。

    返回:
    - JSONResponse: 包含统一响应结构的JSON响应对象。
    """
    # 如果没有提供消息，则根据状态码设置默认消息
    if message is None:
        message = "请求成功" if code < 400 else "请求失败"

    json_compatible_data = jsonable_encoder(data)
    return JSONResponse(
        status_code=code,
        content=Response(
            code=code,
            data=json_compatible_data,
            message=message
        ).dict()
    )


def token_response(access_token: str, token_type: str = "bearer"):
    """
    专门用于认证接口的响应格式

    参数:
    - access_token (str): JWT token
    - token_type (str): token类型，默认为bearer
    """
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "access_token": access_token,
            "token_type": token_type
        }
    )
