from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def status():
    return {"status": "OK"}

@app.post("/webhook")
def webhook(body:dict):
    print(body)
    return body