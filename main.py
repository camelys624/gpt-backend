from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import AzureOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv('API_KEY'),
    azure_endpoint=os.getenv('AZURE_ENDPOINT'),
    api_version="2024-05-01-preview"
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有域名，或者使用具体域名列表  
    allow_credentials=True,  
    allow_methods=["*"],  # 允许所有方法，或者 ["POST", "GET"] 等  
    allow_headers=["*"],  # 允许所有头部，或者具体头部列表
)

class QueryItem(BaseModel):
    role: str
    content: str
    
class QueryItems(BaseModel):
    messages: list[QueryItem]

@app.post('/api/query')
async def query_gpt(request: QueryItems):
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=messages + request.messages,
        temperature=0.7
    )
    return {"status": True, "message": completion.choices[0].message}