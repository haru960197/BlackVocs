# start application
from fastapi import FastAPI
from endpoint.word_endpoint import router as word_router

app = FastAPI(title="Vocabulary App")

app.include_router(word_router, prefix="/words", tags=["Words"])
