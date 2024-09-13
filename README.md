<p align="center">
  <a href="https://fastapi.tiangolo.com" target="blank"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" width="200" alt="FastAPI Logo" /></a>
</p>

[circleci-image]: https://img.shields.io/circleci/build/github/tiangolo/fastapi/master?token=abc123def456
[circleci-url]: https://circleci.com/gh/tiangolo/fastapi

<p align="center">
    <em>FastAPI 框架，高性能，易于学习，快速编码，适合生产环境</em>
</p>

<p align="center">
   <a href="https://github.com/tiangolo/fastapi/actions?query=workflow%3ATest+event%3Apush+branch%3Amaster" target="_blank">
        <img src="https://github.com/tiangolo/fastapi/workflows/Test/badge.svg?event=push&amp;branch=master" alt="Test">
    </a>
    <a href="https://codecov.io/gh/tiangolo/fastapi" target="_blank">
        <img src="https://img.shields.io/codecov/c/github/tiangolo/fastapi?color=%2334D058" alt="Coverage">
    </a>
    <a href="https://pypi.org/project/fastapi" target="_blank">
        <img src="https://img.shields.io/pypi/v/fastapi?color=%2334D058&label=pypi%20package" alt="Package version">
    </a>
    <a href="https://pypi.org/project/fastapi" target="_blank">
        <img src="https://img.shields.io/pypi/pyversions/fastapi.svg?color=%2334D058" alt="Supported Python versions">
    </a>
</p>

## 描述

FastAPI 是一个现代、快速（高性能）的 Web 框架，用于构建 API，基于 Python 3.6+ 的标准类型提示。

主要特点：

* 快速：可与 NodeJS 和 Go 相媲美的极高性能（感谢 Starlette 和 Pydantic）。最快的 Python 框架之一。
* 快速编码：提高功能开发速度约 200% 至 300%。
* 更少的错误：减少约 40% 的人为（开发者）导致错误。
* 直观：强大的编辑器支持。处处皆可自动补全。花更少的时间调试。
* 简单：易于使用和学习。较少的文档阅读时间。
* 简短：最小化代码重复。每个参数声明的多个功能。更少的错误。
* 健壮：生产可用的代码。具有自动交互式文档。
* 基于标准：完全兼容开放标准：OpenAPI（以前称为 Swagger）和 JSON Schema。

## 安装

```bash
# 安装poetry
$ pip install poetry

# 安装项目依赖
$ poetry install
```

## 运行应用程序

```bash
# 启动
$ poetry run uvicorn src.main:app

# 自定义端口号
$ poetry run uvicorn src.main:app --port 8005
```

## 核心组件
1. **数据库配置** (src/core/dbConfig.py)
   使用Tortoise ORM进行数据库操作,配置文件定义了数据库连接和模型加载。
2. **认证** (src/core/auth.py, src/core/jwt.py)
   实现了基于JWT的用户认证系统,包括token创建、验证和刷新功能。
3. **中间件** (src/core/auth_middleware.py)
   实现了全局认证中间件,用于保护需要认证的路由。
4. **响应处理** (src/core/custom_response.py, src/core/response.py)
   自定义了JSON响应格式,确保所有API返回统一的响应结构。
5. **路由加载** (src/core/load_routers.py)
   实现了自动扫描和注册模块路由的功能,简化了路由管理。
6. **日志模块** (src/core/log_config.py)
   自定义的日志记录功能，包括API调用日志和错误日志。日志文件存储在项目根目录的 logs 文件夹中。


## 公共组件

### 1. 模型 (src/common/models.py)

定义了通用的数据库模型基类。

### 2. 模式 (src/common/schemas.py)

定义了通用的Pydantic模型,如响应模型和分页查询模型。

### 3. 服务 (src/common/service.py)

提供了通用的服务类,实现了基础的CRUD操作。

## 主应用 (src/main.py)

配置了FastAPI应用,包括CORS中间件、Tortoise ORM集成、认证中间件和路由注册。

## 开发指南

1. 新增模块:
- 在 `src/modules` 下创建新的模块目录
- 实现模型、模式、控制器和服务
- 系统将自动加载新模块的路由

2. 自定义响应:
- 使用 `src/core/response.py` 中的 `response` 函数来确保一致的响应格式

3. 数据库操作:
- 使用 `src/core/dbhelper.py` 中的 `DbHelper` 类来简化数据库操作

4. 认证:
- 使用 `@Depends(get_current_user)` 来保护需要认证的路由


## 注意事项

- 确保在生产环境中更新 `SECRET_KEY` 和数据库配置
- 根据需要调整CORS设置