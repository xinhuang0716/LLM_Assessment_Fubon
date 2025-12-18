from typing import Dict, Optional
import aiohttp

class AsyncGeminiClient:
    def __init__(self, api_key: str, model: str = "gemini-2.0-flash-exp", temperature: float = 0.0, base_url: str = "https://generativelanguage.googleapis.com/v1beta/models"):
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.base_url = base_url
        self._session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def generate(self, prompt: str) -> Dict:
        url = f"{self.base_url}/{self.model}:generateContent?key={self.api_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": self.temperature}
        }
        session = await self._get_session()
        try:
            async with session.post(url, json=payload) as resp:
                if resp.status != 200:
                    t = await resp.text()
                    raise RuntimeError(f"Gemini API {resp.status}: {t[:200]}")
                data = await resp.json()
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            return {"success": True, "text": text}
        except Exception as e:
            return {"success": False, "error": str(e), "text": None}

    async def aclose(self):
        if self._session and not self._session.closed:
            await self._session.close()
