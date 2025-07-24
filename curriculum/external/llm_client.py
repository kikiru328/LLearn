from typing import List, Dict, Optional
import aiohttp
from config import get_settings
from curriculum.domain.repository.llm_client_repo import ILLMClient


class RealLLMClient(ILLMClient):
    def __init__(self, api_key: Optional[str] = None):
        settings = get_settings()
        self.api_key = api_key or settings.llm_api_key
        self.endpoint = settings.llm_endpoint

    async def generate_schedule(self, goal: str, weeks: int) -> List[Dict[str, object]]:
        payload = {
            "goal": goal,
            "weeks": weeks,
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.endpoint, json=payload, headers=headers
            ) as resp:
                resp.raise_for_status()
                return await resp.json()
