from functools import wraps

from .log_config import api_logger, error_logger


def log_api_call(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            api_logger.info(f"API call: {func.__name__}")
            result = await func(*args, **kwargs)
            api_logger.info(f"API call completed: {func.__name__}")
            return result
        except Exception as e:
            error_logger.error(f"Error in {func.__name__}: {str(e)}")
            raise

    return wrapper
