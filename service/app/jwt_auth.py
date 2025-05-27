import jwt
from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta
import core.config as config

JWT_KEY = config.JWT_KEY

class AuthJwtCsrt():
    """
    認証関係をまとめたクラス
    JWTを使用
    cite: https://qiita.com/kou1121/items/ed29920bc22ef98a1993
    """

    pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret_key = JWT_KEY

    def generate_hashed_pw(self, password) -> str:
        """
        与えられた平文のパスワードをbcryptでハッシュ化して返す

        Parameters:
            password (str): ハッシュ化する平文のパスワード

        Returns:
            str: ハッシュ化されたパスワード文字列
        """
        return self.pwd_ctx.hash(password)

    def verify_pw(self, plain_pw, hashed_pw) -> bool:
        """
        平文パスワードとハッシュ化したパスワードを比較

        Parameters: 
            plain_pw: 平文
            hashed_pw: 保存されたhash

        Returns: 
            bool: 一致 -> true, 不一致 -> false;
        """
        return self.pwd_ctx.verify(plain_pw, hashed_pw)

    # jwtを生成
    def encode_jwt(self, user_id: str, expires_delta: timedelta = timedelta(minutes=5)) -> str:
        """
        JWT(JSON Web Token)を生成

        Parameters:
            subject (str): JWTの対象ユーザー情報。payload内の "sub" フィールドに設定される。
            expires_delta (timedelta, optional): トークンの有効期間。デフォルトは5分, 公式では15分でやっている

        Returns:
            str: HS256アルゴリズムで署名されたJWTトークン。

        """
        now = datetime.utcnow()
        payload = {
            "sub": user_id,
            "iat": now,
            "exp": now + expires_delta,
        }
        return jwt.encode(payload, self.secret_key, algorithm="HS256")

    def decode_jwt(self, token) -> str:
        """
        JWTトークンをデコードして、トークンの対象ユーザー(sub)を返す。

        Parameters:
            token (str): クライアントから渡されたJWTトークン

        Returns:
            str: トークンに含まれるユーザーid

        Raises:
            HTTPException: トークンが期限切れまたは無効な場合は401エラーを返す
        """

        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:  # jwtトークンが執行している
            raise HTTPException(
                status_code=401, detail='The JWT has expired'
            )
        except jwt.InvalidTokenError as e:  # jwtに準拠していない値、空のトークンが渡されたとき
            raise HTTPException(status_code=401, detail='JWT is not valid')
