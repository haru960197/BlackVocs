from fastapi import FastAPI
import uvicorn
import config
from fastapi.middleware.cors import CORSMiddleware

from routes.route_word import router as word_router
from routes.auth import router as auth_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # reactのurl? よくわからない    
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーター登録
app.include_router(auth_router)
app.include_router(word_router)

@app.get("/", status_code=200)
def root():
    return "成功！"

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=config.SERVICE_PORT, reload=True)
