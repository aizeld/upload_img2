import aiohttp
import json
from aiohttp import FormData






class Api:
    __url = "https://dev1.agroonline.kz/api"          
        
    
    @staticmethod
    async def request(url: str, method: str, data: dict = None, headers: dict = {}) -> dict:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(method, url, data=data, headers=headers) as response:
                    if response.status in (200, 201):
                        return {"data": await response.json(), "status_code": response.status}
                    else:
                        return {"message": f"Request failed with details {await response.json()}", "status_code": response.status}
        except aiohttp.ClientError as e:
            return {"error": str(e)}
    

        
    @staticmethod
    async def login(username: str, password: str, remember: bool = False) -> dict:
        url = f"{Api.__url}/auth/token/"
        data = {
            "email": username,
            "password": password
        }
        headers = {
            "Content-Type": "application/json",
        }
        response = await Api.request(url, "POST", data=json.dumps(data), headers=headers)
        status_code = response.get('status_code', 500)
        if status_code in (200, 201):
            tokens = {'access': response['data'].get('access'), 'status_code': status_code}
            if remember:
                tokens['refresh'] = response['data'].get('refresh')
            return tokens

        return {
            "error": response.get('message', 'unknown error'),
            "status_code": status_code
        }

    @staticmethod
    async def get_user(access_token: str) -> dict:
        url = f"{Api.__url}/users/me/"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        response = await Api.request(url, method="GET", headers=headers)
        status_code = response.get('status_code')
        if response:
            return {"data": response["data"], "status_code": status_code}
        return {"error": response, "status_code": status_code}

    @staticmethod
    async def get_fields(access_token: str, company_id: str) -> dict:
        url = f"{Api.__url}/company/{company_id}/fields/"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        response = await Api.request(url=url, method="GET", headers=headers)

        if response.get('status_code') != 200:
            return {"error": response, "status_code": response.get('status_code')}
        
        return {'data': response, "status_code": 200}



    @staticmethod
    async def image_upload_test(form: FormData, access_token: str, file):
        # Prepare upload URL and headers
        company_id = form.get('company_id')
        url = f"{Api.__url}/company/{company_id}/maps/satellites/upload/"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        fields = ["map_info", "date", "map_type", "metrics", "context", "shape"]
    
        form_upload = FormData()
    
    
        for field in fields:
            value = form.get(field)
            if value:
                form_upload.add_field(field, value)
                
                
        form_upload.add_field('file', file)

       

   
        response = await Api.request(url=url, method="POST", data=form_upload, headers=headers)

  
        status_code = response.get('status_code')
        return {
            "message": "Successfully uploaded" if status_code == 201 else response.get('message', "Unknown error"),
            "status_code": status_code
        }

    @staticmethod
    async def image_upload_test1(form: FormData, access_token: str, company_id):
        # Prepare upload URL and headers
        url = f"{Api.__url}/company/{company_id}/maps/satellites/upload/"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
     
        
       
        

   
        response = await Api.request(url=url, method="POST", data=form, headers=headers)

  
        status_code = response.get('status_code')
        return {
            "message": "Successfully uploaded" if status_code == 201 else response.get('message', "Unknown error"),
            "status_code": status_code
        }

            
    @staticmethod
    async def image_upload(form: FormData, access_token: str, file):
        company_id = form.get('company_id')
        shape = form.get("shape")
        context = form.get("context")
        

        gis_data = get_gis_data()
        url = f"{Api.__url}/company/{company_id}/maps/satellites/upload/"
    
        headers = {
            "Authorization" : F"Bearer {access_token}"
        } 
        form_upload = FormData() #пришлось создать новую форм дату ибо, add_field почему то не работал с формдаты которая с фронтенда, костыль понимаю
        
        for key, value in gis_data.items():
            form_upload.add_field(key, str(value))
            
            
        form_upload.add_field("company_id", company_id)
        form_upload.add_field("context", context)
        form_upload.add_field("shape",  shape)
        form_upload.add_field('file', file)
        
        print(form_upload)
        
        response = await Api.request(url = url, method="POST", data = form_upload, headers = headers)

        status_code = response.get('status_code')
        return {
            "message": "Successfully uploaded" if status_code == 201 else response.get('message', "Unknown error"),
            "status_code": status_code
        }
            
            
            
    @staticmethod
    async def test():
        login = "intern@on-track.ai"
        password = "Intern123"
        COMPANY_ID = "1093"
        file_path = 'C:/Users/Asilk/Desktop/work/14072023_59158r2_NDVI_P20160317_S2A.png'
        
        token_response = await Api.login(login, password, False)
        if 'error' in token_response:
            print("Login failed:", token_response)
            return
        
        token = token_response['access']
        
        fields_response = await Api.get_fields(access_token=token, company_id=COMPANY_ID)
        if 'error' in fields_response:
            print("Get fields failed:", fields_response)
            return
        
        with open(file_path, 'rb') as f:
            file_data = {'file': f}
            upload_response = await Api.upload_image(access_token=token, company_id=COMPANY_ID, files=file_data, data={})
            if 'error' in upload_response:
                print("Upload image failed:", upload_response)
                return
        
        print("Image uploaded successfully:", upload_response)
