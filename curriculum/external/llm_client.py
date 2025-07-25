import json
import logging
from typing import List, Dict, Optional
import aiohttp
from config import get_settings
from curriculum.domain.repository.llm_client_repo import ILLMClient

logger = logging.getLogger(__name__)


class RealLLMClient(ILLMClient):
    def __init__(
        self,
        api_key: Optional[str] = None,
        endpoint: Optional[str] = None,
    ):
        settings = get_settings()
        self.api_key = api_key or settings.llm_api_key
        self.endpoint = settings.llm_endpoint

    async def generate_schedule(self, goal: str, weeks: int) -> List[Dict[str, object]]:
        payload = {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a curriculum generator. "
                        "When you respond, output *only* valid JSON — "
                        "no markdown, no explanations, nothing else. "
                        "The JSON must be an array of objects, each with "
                        "`week_number` (integer) and `topics` (array of strings). "
                        "Example:\n"
                        '[{"week_number":1,"topics":["Intro","Setup"]},'
                        '{"week_number":2,"topics":["Deep Dive"]}]'
                    ),
                },
                {
                    "role": "user",
                    "content": f"Generate a {weeks}-week curriculum for the goal: {goal}",
                },
            ],
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
                data = await resp.json()
                text = data["choices"][0]["message"]["content"]

                # 1) 로그로 원시 응답 남기기
                logger.info("🔍 LLM RAW RESPONSE: %s", text)

                # 2) JSON 파싱 시도 및 실패 시 로깅
                try:
                    return json.loads(text)
                except json.JSONDecodeError:
                    logger.error("❌ Failed to parse JSON from LLM response: %r", text)
                    # 필요하면 여기서 예외를 던지거나, 빈 리스트/기본값으로 처리할 수 있습니다.
                    raise

    async def generate_feedback(
        self, topics: List[str], summary_content: str
    ) -> Dict[str, object]:
        payload = {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a learning feedback generator. "
                        "When you respond, output *only* valid JSON — "
                        "no markdown, no explanations, nothing else. "
                        "The JSON must have exactly these fields: "
                        "`comment` (string, detailed feedback in Korean, minimum 100 characters) and "
                        "`score` (integer, 1-10). "
                        'Example: {"comment":"상세한 피드백 내용...","score":8}'
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"학습 주제들: {', '.join(topics)}\n"
                        f"학습자의 요약: {summary_content}\n\n"
                        "위 학습 주제에 대한 학습자의 요약을 평가하고 피드백을 제공해주세요."
                    ),
                },
            ],
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
                data = await resp.json()
                text = data["choices"][0]["message"]["content"]

                logger.info("🔍 LLM FEEDBACK RESPONSE: %s", text)

                try:
                    return json.loads(text)
                except json.JSONDecodeError:
                    logger.error("❌ Failed to parse feedback JSON: %r", text)
                    raise
