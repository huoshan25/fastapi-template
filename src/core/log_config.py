import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logger(name, log_file, level=logging.INFO):
    """函数设置任意多的记录器"""

    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    # 设置日志文件最大为1MB，保留5个旧文件
    handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024, backupCount=5)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    print(f"Logger '{name}' 设置完成。日志文件: {log_file}")
    return logger


# 确保日志目录存在
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
print(f"已创建/检查日志目录: {log_dir}")

# 创建不同的日志器
api_logger = setup_logger('api_logger', os.path.join(log_dir, 'api.log'))
error_logger = setup_logger('error_logger', os.path.join(log_dir, 'error.log'), level=logging.ERROR)

print("记录器设置完成.")
