import json
from fastapi import FastAPI, UploadFile, Request
from producer import MessageProducer
import uvicorn
# ===========
import time
time.sleep(15)

# ===========
app = FastAPI()

ProducerMessage = MessageProducer()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q):
    return {"item_id": item_id, "q": q}


@app.post("/upload_file/")
def receive_file_from_user(file):
    try:
        contents = file.read()
        json_data = json.loads(contents.decode('utf-8'))
        print(contents)
        ProducerMessage.publish("send_to_discord",json_data)

        return {"message": "File received and sent to Discord!"}
    except Exception as e:
        return {"error": str(e)}

@app.post("/upload/")
async def receive_from_user(request:Request):
    body_data = await request.json()
    print(body_data)

    try:
        ProducerMessage.publish("send_to_discord",body_data,routing_key="discord.routing.key")
        return {"status":"OK!"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run("backend:app", host="0.0.0.0", port=8888, reload=True)