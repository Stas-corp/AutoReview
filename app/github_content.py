import os
from pydantic import HttpUrl

from fastapi import HTTPException
import httpx

class GithubManager:
    GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN")
    headers = {"Authorization": f"Bearer {GITHUB_API_TOKEN}",
                "Accept": "application/vnd.github.raw+json"}
    
    @classmethod
    async def main(cls, repo_url: HttpUrl):
        repo_path = cls.extract_repo_info(repo_url)
        return await cls.fetch_repo_contents(repo_path)

    @staticmethod
    def extract_repo_info(repo_url: HttpUrl):
        parts = str(repo_url).rstrip('/').split('/')
        if len(parts) >= 2:
            user = parts[-2]
            repo = parts[-1]
            return f'{user}/{repo}'
        else:
            raise ValueError("Invalid GitHub URL")

    @staticmethod
    def build_api_url(repo_path: str, path: str = ''):
        return f"https://api.github.com/repos/{repo_path}/contents/{path}"
    
    @staticmethod
    async def fetch_file_content(download_url: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(download_url)
            if response.status_code == 200:
                return response.text
            else:
                raise HTTPException(status_code=500, detail=f"Error download file: {download_url}")

    @classmethod
    async def fetch_repo_contents(cls, repo_path: str, path: str = ''):
        files_content = {}
        api_url = cls.build_api_url(repo_path, path)
        async with httpx.AsyncClient() as client:
            response = await client.get(url=api_url, headers=cls.headers)
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail=f"Bad url: {api_url}")
            else:
                contents = response.json()
                for item in contents:
                    if item['type'] == 'dir':
                        sub_dir_content = await cls.fetch_repo_contents(repo_path, item['path'])
                        files_content.update(sub_dir_content)
                    else:
                        file_content = await cls.fetch_file_content(item['download_url'])
                        files_content[item['path']] = file_content
                        
                        # print(f"File: {item['path']} - Content:\n{file_content}")
        return files_content