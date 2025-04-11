from fastapi import FastAPI

app = FastAPI(title="FastAPI Sample")

@app.get("/", status_code=200)
def root():
    return "成功！"