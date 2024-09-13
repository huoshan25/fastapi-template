TORTOISE_ORM = {
    "connections": {
        "default": {
            'engine': 'tortoise.backends.mysql',  # MySQL or Mariadb
            'credentials': {
                'host': 'localhost',
                'port': '3306',
                'user': 'root',
                'password': '123456',
                'database': 'web-test',
                'minsize': 1,
                'maxsize': 5,
                'charset': 'utf8mb4',
                'echo': True
            }
        }
    },
    "apps": {
        "models": {
            "models": [
                'src.modules.user.models.user',
                # 'src.modules.test.models.test'
            ],
            #  your_models_path: 例如my_api.models;
            # aerich.models必须要有，但不用创建对应的models文件
            "default_connection": "default",
        }
    },
    "use_tz": False,  # 建议不要开启，不然存储日期时会有很多坑，时区转换在项目中手动处理更稳妥。
    "timezone": "Asia/Shanghai"
}
