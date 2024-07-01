from fastapi import Request, HTTPException
from config import Config




def verify_auth_header(request: Request):

    if Config.API_KEY:
        api_key_from_header: str = request.headers.get("X-API-KEY")
        if Config.API_KEY != api_key_from_header:
            raise HTTPException(status_code=401, detail="Invalid API key")