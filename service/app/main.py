from fastapi import FastAPI
import uvicorn
import mongo_utils
import config
from db.session import client, get_db
import schemas

app = FastAPI()

@app.on_event("shutdown")
def shutdown_event():
    client.close()

@app.get("/", status_code=200)
def root():
    return "成功！"

@app.post("/add_new_word/", response_model=schemas.AddNewWordResponse)
async def add_new_word(request: schemas.AddNewWordRequest):
    """
    単語からitemを生成し，データベースに保存
    """
    word = request.item.word
    try:
        print("Received: ", word)
        inserted_id = mongo_utils.generate_and_insert_item(word)
        return {"message": f"Item '{word}' was saved."}
    except Exception as e:
        print("Error occurred:", e)
        return {"error": str(e)}

@app.get("/items/all", response_model=schemas.GetAllItemsResponse)
async def get_all_items():
    items = mongo_utils.get_all_items()
    return {"items": items}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=config.SERVICE_PORT, reload=True)
