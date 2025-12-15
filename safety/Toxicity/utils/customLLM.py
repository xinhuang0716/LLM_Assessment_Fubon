import requests
from deepeval.models.base_model import DeepEvalBaseLLM


class GeminiRequestsLLM(DeepEvalBaseLLM):
    """Custom LLM class for interacting with Google's Gemini models via REST API.

    Args:
        DeepEvalBaseLLM (_type_): Following DeepTeam requirements for custom LLMs, inheriting DeepEvalBaseLLM.
    """

    def __init__(self, api_key: str, model_name: str = "gemini-2.5-flash"):
        """_summary_

        Args:
            api_key (str): API key for authentication.
            model_name (str, optional): The response LLM model. Defaults to "gemini-2.5-flash".
        """
        self.api_key = api_key
        self.model_name = model_name
        self.api_endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"

    def load_model(self) -> DeepEvalBaseLLM:
        return self

    def generate(self, prompt: str) -> str:
        # Prepare request
        headers = {"Content-Type": "application/json", "X-goog-api-key": self.api_key}
        payload = {"contents": [{"role": "user", "parts": [{"text": prompt}]}]}

        # Make API request
        response = requests.post(self.api_endpoint, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        response_data = response.json()

        return response_data["candidates"][0]["content"]["parts"][0]["text"]

    async def a_generate(self, prompt: str) -> str:
        # TODO: Implement true async with aiohttp or httpx for better performance
        return self.generate(prompt)

    def get_model_name(self) -> str:
        return f"Custom Gemini {self.model_name}"
