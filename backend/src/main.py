from fastapi import FastAPI, Request, Response, UploadFile, File, Depends, HTTPException, Cookie
from api import Api
import uvicorn
import json
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse


# Настройка 
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"], #for frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ППроверка текущего пользователя по токену
async def get_current_user(token: str = Cookie(None)) -> str:
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return token

# Логин
@app.post("/login")
async def login(request: Request):
    data = await request.json()
    username, password = data['username'], data['password']
    
    response = await Api.login(username, password)
    
    if response.get('status_code') == 200:
        token = response.get('access')
        if token:
            response_cookie = "token"
            response_cookie_value = token
            response_cookie_max_age = 60 * 60  # 1час
            # токен в куки
            return JSONResponse(content={"token": token}, headers={"Set-Cookie": f"{response_cookie}={response_cookie_value}; Max-Age={response_cookie_max_age}"})
        else:
            return JSONResponse(content = {"message": "Token expired, log in again"}, status_code = response['status_code'])
    else:
        status_code=response["status_code"]
        return JSONResponse(content={"message": "Invalid credentials", "status_code": status_code})


#логаут
@app.post("/logout")
async def logout():
    response = JSONResponse(content={"message": "Logged out"})
    response.delete_cookie("token")
    return response



# для получения информации о текущем пользователе
@app.get("/users/whoami")
async def get_user(token:str = Depends(get_current_user)):
    response = await Api.get_user(token)
    print(response)
    if "error" in response:
        raise HTTPException(status_code=response["status_code"], detail=response["error"])
    return JSONResponse(content=response["data"])




# для загрузки файлов
@app.post("/upload")
async def upload(request: Request, files: list[UploadFile] = File(...), token: str = Depends(get_current_user)):
    form = await request.form()
    print(form)
    company_id = form.get("company_id")
    print(company_id)
    responses = []
    for file in files:
        contents = await file.read() 
        print(file.filename)
        response = await Api.upload_image_test(access_token=token, company_id=company_id, file=contents) 
        responses.append(response)#сахраняем все респонсы, для проверки 
    
    for response in responses:
        if response['status_code'] not in (201, 200):
            print(response)
            return JSONResponse(content={"error": response['message']}, status_code=response["status_code"])
    print(responses[-1]["message"], responses[-1]["status_code"])
    return JSONResponse(content=responses[-1]["message"], status_code=responses[-1]["status_code"]) #если нет ошибок ни в одной, то возвращаем последний респосн

# Запуск 
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
