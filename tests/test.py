import httpx
from app.main import analyze_code, GithubManager
import asyncio

code = '''import os
import logging

import httpx
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from pydantic import BaseModel, HttpUrl

logging.basicConfig(level=logging.INFO)

app = FastAPI()
load_dotenv()
'''

def test_analyze():
    print(analyze_code(code))

async def test_GitHubManager():
    result = await GithubManager.main('https://github.com/Stas-corp/tlb_project')
    with open('result.txt', 'w', encoding='utf-8') as f:
        for file, content in result.items():
            f.write(f'{file}\n{content}\n\n' )

async def test_main():
    url = "http://127.0.0.1:8000/review"
    payload = {
        "description": "This is a coding assignment",
        "repo_url": "https://github.com/Stas-corp/tlb_project",
        "level": "Junior"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        print(response.json())

if __name__ == '__main__':
    test_analyze()
    # asyncio.run(test_GitHubManager())
    # asyncio.run(test_main())