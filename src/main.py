from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from src.core.auth_middleware import add_auth_middleware
from src.core.custom_response import CustomJSONResponse
from src.core.dbConfig import TORTOISE_ORM
from src.core.load_routers import register_routes

app = FastAPI(
    title="fastapi-template",
    description="fastapi的模板项目",
    version="1.0.0",
    default_response_class=CustomJSONResponse,
    # Swagger UI 配置
    docs_url="/docs",  # Swagger UI的访问地址
    redoc_url="/redoc",  # ReDoc文档的访问地址
    openapi_url="/openapi.json"  # OpenAPI架构的地址
)

# 注册数据库
register_tortoise(
    app=app,
    config=TORTOISE_ORM,
    # generate_schemas=True,  # 如果数据库为空，则自动生成对应表单，生产环境不要开
    # add_exception_handlers=True,  # 生产环境不要开，会泄露调试信息
)

# 定义允许的来源、方法和头
origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://example.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 允许的来源列表
    allow_credentials=True,  # 是否允许证书（cookies等）
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有的头部信息
)

# 添加认证中间件
add_auth_middleware(app)

# 自动注册路由
register_routes(app)
