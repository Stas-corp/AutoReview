from .github_content import GithubManager
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

app = FastAPI()

class ReviewRequest(BaseModel):
    description: str
    repo_url: HttpUrl
    level: str

@app.post("/review")
async def review_code(request: ReviewRequest):
    try:
        logging.info("Review process started")
        repo_data = await GithubManager.main(request.repo_url)
        prompt = ''
        logging.info("Creating prompt")
        for file, content in repo_data.items():
            prompt += f'{file}\n{content}\n\n'
        logging.info("Reqest to OpenAI")
        # review = await analyze_code(prompt, OPENAI_API_KEY)
        review = await analyze_code(prompt)
        print ({"review": review})
    except Exception as e:
        logging.error(f"Error during review: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    
def analyze_code(code: str):
    client_openai = openai.Client(api_key=OPENAI_API_KEY)
    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": f"Analyze this code and provide a review: {code}"}],
    }
    try:
        if httpx.Response.is_success:
            chat = client_openai.chat.completions.create(messages=data["messages"], model=data['model'], stream=True)
            for chunk in chat:
                return chunk.choices[0].delta.content
        else:
            raise HTTPException(status_code=429, detail="Error response OpenAI")
    except:
        raise HTTPException(status_code=500, detail="Error analyzing code with OpenAI")


