from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

import os
import json

app = FastAPI()
filePath = f"data/data.json"
class PostAndPutDataModel(BaseModel):
  key: str
  data: str

def readJson():
  if not os.path.exists(filePath):
    return {"readError": "File not found"}
  try:
    with open(filePath, "r") as file:
      data = json.load(file)
      return data
  except json.JSONDecodeError as e:
    print(e)
    return {"readError": "Read file error"}

@app.get("/json/{field}")
def getData(field: str):
  data = readJson()
  if "readError" in data:
    return JSONResponse({"error": data["readError"]}, status_code=502)
  elif not field in data:
    return JSONResponse({"data": "Invalid field"}, status_code=404)
  else:
    return JSONResponse({"data": data[field]}, status_code=200)

@app.post("/json")
def addData(body: PostAndPutDataModel):
  # 데이터 읽기
  data = readJson()
  if "readError" in data:
    return JSONResponse({"error": data["readError"]}, status_code=502)

  # 이미 있는 key 제거
  if body.key in data:
    return JSONResponse({"error": "The key is duplicated"}, status_code=402)
  
  # error key 사용 금지
  if body.key == "error":
    return JSONResponse({"error": "Invalid key name"}, status_code=402)

  try:
    data[body.key] = body.data
    with open(filePath, "w") as file:
      json.dump(data, file, ensure_ascii=False ,indent=4)
      return JSONResponse({"data": f"{body.key} was created"}, status_code=201)
  except Exception as e:
    print(e)
    return JSONResponse({"error": "Write file error"}, status_code=402)


@app.put("/json")
def updateData(body: PostAndPutDataModel):
  # 파일 읽어오기
  data = readJson()
  if "readError" in data:
    return JSONResponse({"error": data["readError"]}, status_code=502)

  if not body.key in data:
    return JSONResponse({"error": "Not found key"}, status_code=404)

  try:
    data[body.key] = body.data
    with open(filePath, "w") as file:
      json.dump(data, file, ensure_ascii=False ,indent=4)
      return JSONResponse({"data": f"{body.key} was updated"}, status_code=201)
  except Exception as e:
    print(e)
    return JSONResponse({"error": "Write file error"}, status_code=402)

@app.delete("/json/{key}")
def deleteData(key: str):
  data = readJson()
  if not key in data:
    return JSONResponse({"error": "Not found key"}, status_code=404)

  try:
    del data[key]
    with open(filePath, "w") as file:
      json.dump(data, file, ensure_ascii=False, indent=4)
      return JSONResponse({"data": f"{key} was deleted"}, status_code=201)
  except Exception as e:
    print(e)
    return JSONResponse({"error": "Write file error"}, status_code=402)
