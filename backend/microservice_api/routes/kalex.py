from fastapi import APIRouter, Depends, HTTPException, Path
from microservice_api.utils.functions import ask_kalex

router = APIRouter(prefix="/kalex", tags=["kalex"])

@router.get("/query_kalex/")
async def get_a_response(user_prompt:str):
  response = ask_kalex(user_prompt)
  
  return {"ai":response}