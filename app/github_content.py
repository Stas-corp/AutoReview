from fastapi import HTTPException
import httpx

async def fetch_repo_contents(repo_url: str, github_token: str):
    headers = {"Authorization": f"Bearer {github_token}",
               "Accept": "application/vnd.github.raw+json"}
    api_url = f"https://api.github.com/repos/{repo_url}/contents/{path}"
    async with httpx.AsyncClient() as client:
        response = await client.get(api_url, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Error fetching repository data from GitHub")
        return response.json()