from fastapi import HTTPException
from service.app.jwt_auth import AuthJwtCsrt

auth = AuthJwtCsrt()

async def db_signup(data: dict) -> dict:
    """
    新規ユーザーをデータベースに登録します。

    Args:
        data (dict): ユーザー登録に必要な情報を含む辞書。主に "email" と "password" を含む。

    Raises:
        HTTPException: 
            - Emailがすでに登録されている場合 (status_code=400)
            - Passwordが未入力または6文字未満の場合 (status_code=400)

    Returns:
        dict: 登録された新しいユーザーの情報をシリアライズしたもの。    
    """
    email = data.get("email")
    password = data.get("password")

    # emailの存在確認
    overlap_user = await collection_user.find_one({"email": email})
    if overlap_user:
        raise HTTPException(status_code=400, detail='Email is already taken')

    if not password or len(password) < 6:
        raise HTTPException(status_code=400, detail='Password too short')

    # パスワードをハッシュ化して登録
    user = await collection_user.insert_one({
        "email": email,
        "password": auth.generate_hashed_pw(password)
    })

    new_user = await collection_user.find_one({"_id": user.inserted_id})
    return user_serializer(new_user)

def user_serializer(user: dict) -> dict:
    """
    MongoDBのユーザードキュメントをシリアライズする関数

    Args:
        user (dict): MongoDBから取得したユーザードキュメント

    Returns:
        dict: APIレスポンス用に整形したユーザーデータ
    """
    return {
        "id": str(user["_id"]),
        "email": user["email"],
    }

async def db_login(data: dict) -> str:
    """
    ユーザー認証を行い、JWTトークンを発行します。

    Args:
        data (dict): ログイン情報を含む辞書。主に "email" と "password" を含む。

    Raises:
        HTTPException:
            - Emailが存在しない、またはパスワードが一致しない場合 (status_code=401)

    Returns:
        str: 認証成功時に発行されるJWTトークン。
    """
    email = data.get("email")
    password = data.get("password")

    user = await collection_user.find_one({"email": email})
    if not user or not auth.verify_pw(password, user["password"]):
        raise HTTPException(status_code=401, detail='Invalid email or password')

    token = auth.encode_jwt(user['email'])
    return token

async def db_get_all_users() -> list:
    users_cursor = collection_user.find({})
    users = []
    async for user in users_cursor:
        users.append(user_serializer(user))
    return users
