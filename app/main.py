from .github_content import fetch_repo_contents
import os
import logging

import openai
import httpx
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from pydantic import BaseModel, HttpUrl

load_dotenv()
logging.basicConfig(level=logging.INFO)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN")

client_openai = openai.Client(api_key=OPENAI_API_KEY)
app = FastAPI()

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
    
def analyze_code(code: str):
    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": f"Analyze this code and provide a review: {code}"}],
    }
    try:
        if httpx.Response.is_success:
            chat = client_openai.chat.completions.create(messages=data["messages"], model=data['model'], stream=True)
            for chunk in chat:
                print(chunk.choices[0].delta.content, end="")
        else:
            raise HTTPException(status_code=429, detail="Error response OpenAI")
    except:
        raise HTTPException(status_code=500, detail="Error analyzing code with OpenAI")


