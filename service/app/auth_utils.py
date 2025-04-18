import jwt
from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta
import config

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
    def encode_jwt(self, email) -> str:  # ユーザーemail
        """
        jwtの生成(期限付き)

        Parameters:
            email (str): トークンの対象となるユーザーのメールアドレス

        Returns:
            str: エンコードされたJWTトークン

        """

        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, minutes=5),  # jwtの有効期限ここでは５分
            'iat': datetime.utcnow(),  # jwtが生成された日時
            'sub': email  # ユーザーを一意に識別出来るものを指定
        }
        return jwt.encode(
            payload,
            self.secret_key,
            algorithm='HS256'  # アルゴリズム
        )

    def decode_jwt(self, token) -> str:
        """
        JWTトークンをデコードして、トークンの対象ユーザー（sub）を返す。

        Parameters:
            token (str): クライアントから渡されたJWTトークン

        Returns:
            str: トークンに含まれるユーザー識別情報（例：email）

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
