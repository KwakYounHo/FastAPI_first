from fastapi import FastAPI

app = FastAPI()

@app.get("/test")
def sayHello():
  return {"message": "Hello Green!"}