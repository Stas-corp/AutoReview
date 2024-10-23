import os
import logging

import httpx
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from pydantic import BaseModel, HttpUrl

logging.basicConfig(level=logging.INFO)

app = FastAPI()
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN")

class ReviewRequest(BaseModel):
    description: str
    repo_url: HttpUrl
    level: str

@app.post("/review")
async def review_code(request: ReviewRequest):
    try:
        logging.info("Review process started")
        repo_data = await fetch_repo_contents(request.repo_url, GITHUB_API_TOKEN)
        review = await analyze_code(repo_data, OPENAI_API_KEY)
        return {"review": review}
    except Exception as e:
        logging.error(f"Error during review: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

async def fetch_repo_contents(repo_url: str, token: str):
    headers = {"Authorization": f"token {token}"}
    api_url = f"https://api.github.com/repos/{repo_url}/contents"
    async with httpx.AsyncClient() as client:
        response = await client.get(api_url, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Error fetching repository data from GitHub")
        return response.json()
    
async def analyze_code(code: str, openai_api_key: str):
    headers = {
        "Authorization": f"Bearer {openai_api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4o",
        "messages": [{"role": "user", "content": f"Analyze this code and provide a review: {code}"}],
        "temperature" : 0.7
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post("https://api.openai.com/v1/chat/completions", data=data, headers=headers)
            return response #.json()["choices"][0]["text"]
        except Exception as e:
            return e

