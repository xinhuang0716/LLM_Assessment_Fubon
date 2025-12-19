from typing import Dict, Optional
import aiohttp

class AsyncLlamaClient:
    def __init__(self,
                 model: str = "llama3.1:8b",
                 temperature: float = 0.8,
                 base_url: str = "http://172.21.134.121:11434"):
        """
        Initialize AsyncLlamaClient for Ollama API.
        
        Args:
            model: Model name (e.g., "llama3.1:8b", "gemma3:1b")
            temperature: Controls randomness (0.0-1.0). Lower = more deterministic
            base_url: Ollama server base URL
        """
        self.model = model
        self.temperature = temperature
        self.base_url = base_url
        self._session: Optional[aiohttp.ClientSession] = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session
    
    async def generate(self, prompt: str, system: str, stream: bool = False) -> Dict:
        """
        Generate response from Ollama model.
        
        Args:
            prompt: Input prompt
            stream: Whether to stream response (not implemented in this version)
            
        Returns:
            Dict with keys: success (bool), text (str or None), error (str or None)
        """
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": stream,
            "system": system,
            "options": {
                "temperature": self.temperature
            }
        }
        
        session = await self._get_session()
        try:
            async with session.post(url, json=payload) as resp:
                if resp.status != 200:
                    t = await resp.text()
                    raise RuntimeError(f"Ollama API {resp.status}: {t[:200]}")
                data = await resp.json()
            
            text = data.get("response", "")
            return {"success": True, "text": text}
        except Exception as e:
            return {"success": False, "error": str(e), "text": None}
    
    async def aclose(self):
        """Close the aiohttp session."""
        if self._session and not self._session.closed:
            await self._session.close()