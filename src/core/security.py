from abc import ABC, abstractmethod
from fastapi.security import HTTPBearer
from passlib.context import CryptContext


class PasswordManager(ABC):
    """
    密码管理器的抽象基类。

    定义了密码管理器应该实现的基本方法。使用抽象基类可以确保所有子类都实现这些方法，
    提高代码的一致性和可维护性。
    """

    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        验证明文密码是否与哈希密码匹配。

        Args:
            plain_password (str): 用户输入的明文密码。
            hashed_password (str): 存储在数据库中的哈希密码。

        Returns:
            bool: 如果密码匹配返回True，否则返回False。
        """
        pass

    @abstractmethod
    def hash_password(self, password: str) -> str:
        """
        将明文密码转换为哈希密码。

        Args:
            password (str): 需要哈希化的明文密码。

        Returns:
            str: 哈希后的密码。
        """
        pass


class BcryptPasswordManager(PasswordManager):
    """
    使用Bcrypt算法的具体密码管理器实现。

    Bcrypt是一种设计用于密码哈希的算法，它具有可调整的工作因子，可以随着计算能力的增加而增加哈希的复杂度。
    """

    def __init__(self):
        """
        初始化Bcrypt密码管理器。

        创建一个CryptContext实例，配置使用bcrypt方案。
        'deprecated="auto"' 允许自动处理已弃用的哈希方法。
        """
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        验证明文密码是否与Bcrypt哈希密码匹配。

        使用CryptContext的verify方法来安全地比较密码。

        Args:
            plain_password (str): 用户输入的明文密码。
            hashed_password (str): 存储的Bcrypt哈希密码。

        Returns:
            bool: 如果密码匹配返回True，否则返回False。
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def hash_password(self, password: str) -> str:
        """
        使用Bcrypt算法哈希明文密码。

        Args:
            password (str): 需要哈希的明文密码。

        Returns:
            str: Bcrypt哈希后的密码。
        """
        return self.pwd_context.hash(password)


# 创建一个HTTPBearer实例，用于处理Bearer令牌认证
bearer = HTTPBearer()