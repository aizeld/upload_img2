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
    username, password, remember = data['username'], data['password'], data.get('remember', False)
    
    response = await Api.login(username, password, remember)
    status_code = response.get('status_code')
    if status_code == 200:
        
        token = response.get('access')
    
        response_cookie = "token"
        response_cookie_value = token
        response_cookie_max_age = 60 * 60 * 4 # 4часa
        samesite = "None" if remember else "Lax"
        if remember:
            token = response.get('refresh')
            response_cookie_max_age = 60 * 60 * 24 * 30  # 30 дней
        # токен в куки
        response = JSONResponse(content={"token": token})
        
        # Установка куки
        response.set_cookie(
            key=response_cookie,
            value=response_cookie_value,
            max_age=response_cookie_max_age,
            httponly=False,
            samesite=samesite,
            secure=True  # обязательно, если используете SameSite=None
        )   
        return response
    else:
        print(response)
        raise HTTPException(status_code = status_code)
        

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
    if "error" in response:
        raise HTTPException(status_code=response["status_code"], detail=response["error"])
    return JSONResponse(content=response["data"])




# для загрузки файлов
@app.post("/upload_test")
async def upload_test(request : Request, files : list[UploadFile] = File(...), token: str = Depends(get_current_user)):
    form = await request.form() 
    responses = []
    for file in files:
        contents = await file.read()
        print(file.filename)
        response = await Api.image_upload_test(access_token=token, form=form, file = contents)
        responses.append(response)
    
    for response in responses:
        if response['status_code'] not in (201, 200):
            print(response)
            return JSONResponse(content={"error": response['message']}, status_code=response["status_code"])
            
    print(responses[-1]["message"], responses[-1]["status_code"])
    return JSONResponse(content = responses[-1]["message"], status_code = responses[-1]["status_code"]) #если нет ошибок ни в одной, то возвращаем последний респосн

@app.post("/upload")
async def upload(request : Request, files : list[UploadFile] = File(...), token: str = Depends(get_current_user)):
    form = await request.form() 
    responses = []
    for file in files:
        contents = await file.read()
        print(file.filename)
        response = await Api.image_upload(access_token=token, form=form, file = contents)
        responses.append(response)
    
    for response in responses:
        if response['status_code'] not in (201, 200):
            print(response)
            return JSONResponse(content={"error": response['message']}, status_code=response["status_code"])
            
    print(responses[-1]["message"], responses[-1]["status_code"])
    return JSONResponse(content = responses[-1]["message"], status_code = responses[-1]["status_code"])



@app.get("/get_fields")
async def get_field(company_id:str ,token : str = Depends(get_current_user)):
    print("shit",company_id)
    response = await Api.get_fields(token, company_id)
    status_code = response.get('status_code')
    
    if status_code == 200:
        return JSONResponse(content = response["data"], status_code = status_code) 
    return HTTPException(status_code = status_code, detail = response["error"])
       
        
    


# Запуск 
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
