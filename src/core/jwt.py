from abc import ABC, abstractmethod
from datetime import datetime, timedelta

from jose import jwt, JWTError
from pydantic import BaseModel

from src.core.interfaces.response import response


class TokenData(BaseModel):
    """
    定义令牌数据的结构。

    包含用户名信息，用于从令牌中提取用户标识。
    """
    username: str


class TokenManager(ABC):
    """
    令牌管理器的抽象基类。

    定义了令牌管理所需的基本方法。使用抽象基类确保所有子类都实现这些方法，
    提高代码的一致性和可扩展性。
    """

    @abstractmethod
    def create_access_token(self, data: dict) -> str:
        """
        创建访问令牌。

        Args:
            data (dict): 要编码到令牌中的数据。

        Returns:
            str: 生成的访问令牌。
        """
        pass

    @abstractmethod
    def create_refresh_token(self, data: dict) -> str:
        """
        创建刷新令牌。

        Args:
            data (dict): 要编码到令牌中的数据。

        Returns:
            str: 生成的刷新令牌。
        """
        pass

    @abstractmethod
    def verify_token(self, token: str) -> TokenData:
        """
        验证令牌并提取其中的数据。

        Args:
            token (str): 要验证的令牌。

        Returns:
            TokenData: 从令牌中提取的数据。

        Raises:
            ValueError: 如果令牌无效或无法验证。
        """
        pass

    @abstractmethod
    def refresh_tokens(self, refresh_token: str) -> tuple:
        """
        使用刷新令牌生成新的访问令牌和刷新令牌。

        Args:
            refresh_token (str): 用于刷新的令牌。

        Returns:
            tuple: 包含新的访问令牌和刷新令牌的元组。

        Raises:
            ValueError: 如果刷新令牌无效或无法验证。
        """
        pass


class JWTTokenManager(TokenManager):
    """
    使用JWT（JSON Web Tokens）的具体令牌管理器实现。
    """

    def __init__(self):
        """
        初始化JWT令牌管理器。

        设置密钥、算法和令牌过期时间。
        """
        self.SECRET_KEY = "your-secret-key"  # 在实际应用中应使用环境变量或配置文件
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 30
        self.REFRESH_TOKEN_EXPIRE_DAYS = 7

    def create_access_token(self, data: dict) -> str:
        """
        创建JWT访问令牌。

        Args:
            data (dict): 要编码到令牌中的数据。

        Returns:
            str: 生成的JWT访问令牌。
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    def create_refresh_token(self, data: dict) -> str:
        """
        创建JWT刷新令牌。

        Args:
            data (dict): 要编码到令牌中的数据。

        Returns:
            str: 生成的JWT刷新令牌。
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=self.REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    def verify_token(self, token: str) -> TokenData:
        """
        验证JWT令牌并提取其中的数据。

        Args:
            token (str): 要验证的JWT令牌。

        Returns:
            TokenData: 从令牌中提取的数据。

        Raises:
            ValueError: 如果令牌无效或无法验证。
        """
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise ValueError("令牌无效")
                # raise response(code=401, message="令牌无效")
            token_data = TokenData(username=username)
            return token_data
        except JWTError as e:
            # raise ValueError("无法验证凭据")
            raise response(code=401, message=f"无法验证凭据 - {e}")

    def refresh_tokens(self, refresh_token: str) -> tuple:
        """
        使用刷新令牌生成新的访问令牌和刷新令牌。

        Args:
            refresh_token (str): 用于刷新的JWT令牌。

        Returns:
            tuple: 包含新的访问令牌和刷新令牌的元组。

        Raises:
            ValueError: 如果刷新令牌无效或无法验证。
        """
        try:
            payload = jwt.decode(refresh_token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise ValueError("无效刷新令牌")
                # raise response(code=500, message="无效刷新令牌")
            new_access_token = self.create_access_token({"sub": username})
            new_refresh_token = self.create_refresh_token({"sub": username})
            return new_access_token, new_refresh_token
        except JWTError:
            raise ValueError("无法验证刷新令牌")
            # raise response(code=500, message="无法验证刷新令牌")


class RefreshTokenRequest(BaseModel):
    """
    定义刷新令牌请求的数据结构。

    用于API请求中接收刷新令牌。
    """
    refresh_token: str
