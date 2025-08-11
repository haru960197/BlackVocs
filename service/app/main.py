from fastapi import FastAPI
import uvicorn
import core.config as config
from fastapi.middleware.cors import CORSMiddleware
from db.session import client
from routes.user import router as user_router
from routes.word import router as word_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # reactのurl? よくわからない    
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(word_router)

@app.on_event("shutdown")
def shutdown_event():
    client.close()

@app.get("/", status_code=200)
def root():
    return "成功！"

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(config.SERVICE_PORT), reload=True)
