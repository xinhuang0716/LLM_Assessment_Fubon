from typing import Dict, Optional
from openai import AsyncAzureOpenAI

class AsyncAzureOAIClient:
    def __init__(self,
                 api_key: str,
                 azure_endpoint: str,
                 api_version: str,
                 model: str = "gpt-4o",
                 max_tokens: Optional[int] = None,
                 temperature: float = 1.0,
                 top_p: float = 0.5):
        self.client = AsyncAzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=azure_endpoint
        )
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p

    async def generate(self, prompt: str, system: str = "You are a helpful assistant.") -> Dict:
        try:
            resp = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=self.top_p
            )
            return {"success": True, "text": resp.choices[0].message.content}
        except Exception as e:
            return {"success": False, "error": str(e), "text": None}

    async def aclose(self):
        await self.client.close()
