from fastapi.responses import JSONResponse
from src.core.interfaces.response import response


class CustomJSONResponse(JSONResponse):
    def render(self, content: any) -> bytes:
        if not isinstance(content, dict) or not all(key in content for key in ["code", "data", "message"]):
            content = response(data=content).__dict__
        return super().render(content)
