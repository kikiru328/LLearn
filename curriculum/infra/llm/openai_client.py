import json
import aiohttp
import logging
from typing import Any, Dict, List, Optional
from config import Settings, get_settings
from curriculum.infra.llm.I_llm_client_repo import ILLMClientRepository
from monitoring.metrics import track_llm_metrics

logger = logging.getLogger(__name__)


class OpenAILLMClient(ILLMClientRepository):
    def __init__(
        self,
        api_key: Optional[str] = None,
        endpoint: Optional[str] = None,
    ):
        settings: Settings = get_settings()
        self.api_key: str = api_key or settings.llm_api_key
        self.endpoint: str = endpoint or settings.llm_endpoint

    @track_llm_metrics("curriculum_generation")
    async def generate(self, prompt: str, timeout: float | None = 10.0) -> str:
        payload = {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a curriculum generator. "
                        "Generate in Korean "
                        "Output *only* valid JSON "
                        "The JSON must be an array with these fields "
                        "`title` (string), and `schedule` (array of objects with {week_number:int, topics:list[str]})."
                        "no markdown, no explanations, nothing else "
                        "if request for Computer Science, refer to OSSU curriculum "
                        "else, generate as request"
                    ),
                },
                {"role": "user", "content": prompt},
            ],
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.endpoint, json=payload, headers=headers
            ) as response:
                response.raise_for_status()
                data = await response.json()
                text = data["choices"][0]["message"]["content"]
                logger.info("🔍 LLM RAW RESPONSE: %s", text)
                return text

    @track_llm_metrics("feedback_generation")
    async def generate_feedback(
        self,
        lessons: List[str],
        summary_content: str,
        timeout: float | None = 10.0,
    ) -> Dict[str, Any]:
        """
        LLM에 요약(summary_content)과 학습 주제(lessons)를 보내
        {"comment": "...", "score": 8} 형태의 JSON을 받습니다.
        """
        payload = {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a learning feedback generator. "
                        "Output *only* valid JSON with exactly `comment` (string) "
                        "Generate in Korean "
                        "no markdown, no explanations, nothing else "
                        "and `score` (float 0–10). No other keys or markdown."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"학습 주제들: {', '.join(lessons)}\n"
                        f"학습자의 요약: {summary_content}\n\n"
                        "위 요약에 대해 자세한 피드백과 점수를 제공하세요."
                    ),
                },
            ],
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=timeout)
        ) as session:
            async with session.post(
                self.endpoint, json=payload, headers=headers
            ) as resp:
                resp.raise_for_status()
                body = await resp.json()
                text = body["choices"][0]["message"]["content"]
                logger.info("🔍 LLM FEEDBACK RAW: %s", text)
                # JSON-only 이므로 바로 파싱
                return json.loads(text)
