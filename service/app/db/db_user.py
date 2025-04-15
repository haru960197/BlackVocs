from auth_utils import AuthJwtCsrt

# 新規ユーザー作成
async def db_signup(data: dict) -> dict:
    email = data.get("email")
    password = data.get("password")
    # emailの存在の判定
    overlap_user = await collection_user.find_one({"email": email}) # ユーザーが存在すればtrue
    if overlap_user:
        raise HTTPException(status_code=400, detail='Email is already taken') # trueの場合の例外発生
    if not password or len(password) < 6: # パスワードが６文字以下、入力されていない場合
        raise HTTPException(status_code=400, detail='Password too short')
    # DBに登録
    user = await collection_user.insert_one({"email": email, "password": auth.generate_hashed_pw(password)}) # generate_hashed_pwハッシュ化してDBに返す
    new_user = await collection_user.find_one({"_id": user.inserted_id})
    return user_serializer(new_user)
