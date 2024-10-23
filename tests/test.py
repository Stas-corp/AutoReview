from app.main import analyze_code, fetch_repo_contents
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
    analyze_code(code)

async def test_fetch_repo_contents():
    print(await fetch_repo_contents('Stas-corp/Test_USD'))

if __name__ == '__main__':
    # test_analyze()
    asyncio.run(test_fetch_repo_contents())