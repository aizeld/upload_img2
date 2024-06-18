from fastapi import FastAPI, Request, Response, UploadFile, File, Depends, HTTPException, Cookie
from api import Api
import uvicorn
import json
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from aiohttp import FormData
from datetime import datetime 
import transform_json
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
    json_contents = json.loads(form.get("json"))
    company_id=form.get('company_id')
    
    context = form.get("context")
    shape = form.get("shape")
    
    
    
    curr_date = datetime.now()
    formatted_date = curr_date.strftime("%Y-%m-%d")

    for i, file in enumerate(files):
        print(file.filename)
        print(json_contents[i])
        
        json_cont = json.loads(json_contents[i])
        
        metrics = transform_json.transform(json_cont)
        map_info = transform_json.extract_map_info(file.filename)
        map_type = transform_json.extract_map_type(file.filename)
        
        print(map_info)
        print(map_type)
        print(metrics)
                
        contents = await file.read()
        
        form_dict = FormData()
        
        form_dict.add_field("company_id", company_id)
        form_dict.add_field("shape", shape)
        form_dict.add_field("context", context)
        
        form_dict.add_field('file', contents)
        
        form_dict.add_field("map_info", json.dumps(map_info))
        form_dict.add_field("date", formatted_date)
        form_dict.add_field("map_type", map_type)
        form_dict.add_field("metrics", json.dumps(metrics))
        
        response = await Api.image_upload_test1(access_token=token, form=form_dict, company_id=company_id)
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
    json_contents = json.loads(form.get("json"))
    company_id=form.get('company_id')
    
    context = form.get("context")
    shape = form.get("shape")
    
    
    
    curr_date = datetime.now()
    formatted_date = curr_date.strftime("%Y-%m-%d")

    for i, file in enumerate(files):
        print(file.filename)
        print(json_contents[i])
        
        json_cont = json.loads(json_contents[i])
        
        contents = await file.read()
        
        form_dict = FormData()
        
        form_dict.add_field("company_id", company_id)
        form_dict.add_field("shape", shape)
        form_dict.add_field("context", context)
        
        form_dict.add_field('file', contents)
        
        form_dict.add_field("map_info", json.dumps(json_cont.get("map_info")))
        form_dict.add_field("date", formatted_date)
        form_dict.add_field("map_type", json_cont.get("map_type"))
        form_dict.add_field("metrics", json.dumps(json_cont.get("metrics")))
        
        response = await Api.image_upload_test1(access_token=token, form=form_dict, company_id=company_id)
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
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level = "debug", workers = 4)
    
