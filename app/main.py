from .github_content import GithubManager

import os
import logging
from pydantic import BaseModel, HttpUrl
from dotenv import load_dotenv

import openai
import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

load_dotenv()
logging.basicConfig(level=logging.INFO)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN")

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

class ReviewRequest(BaseModel):
    repo_url: HttpUrl
    level: str

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/review")
async def review_code(request: ReviewRequest): #(description="This is a coding assignment", repo_url="https://github.com/Stas-corp/Test_USD", level ="Junior")
    try:
        logging.info("Review process started")
        repo_data = await GithubManager.main(request.repo_url)
        prompt = ''
        for file, content in repo_data.items():
            prompt += f'{file}\n{content}\n\n'
        logging.info("Request to OpenAI")
        review = analyze_code(prompt, request.level)
        return {"files":list(repo_data.keys()),
                "review": review}
    except Exception as e:
        logging.error(f"Error during review: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    
def analyze_code(code: str, level: str):
    client_openai = openai.Client(api_key=OPENAI_API_KEY)
    data = {
        "model": "gpt-4-turbo",
        "messages": [{"role": "user", "content": f"Review this code as a {level} candidate and provide short feedback on what the positives are and what could be improved: {code}.\n Start your answer like this: As for a programmer level {level}"}],
    }
    try:
        if httpx.Response.is_success:
            chat = client_openai.chat.completions.create(messages=data["messages"], model=data['model'])
            return chat.choices[0].message.content
            # for chunk in chat:
            #     # return chunk.choices[0].delta.content
        else:
            raise HTTPException(status_code=429, detail="Error response OpenAI")
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)