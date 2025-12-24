import requests


class AOAILLM:
    """Configurable Azure OpenAI LLM that can be called directly."""
    
    def __init__(self, endpoint: str, api_key: str, temperature: float = 0.3, top_p: float = 0.95):
        """Initialize Azure OpenAI LLM with configuration.
        
        Args:
            endpoint (str): The endpoint URL for the API request.
            api_key (str): The API key for authentication.
            temperature (float): Temperature parameter for response generation.
            top_p (float): Top-p parameter for response generation.
        """
        self.endpoint = endpoint
        self.api_key = api_key
        self.temperature = temperature
        self.top_p = top_p
    
    def __call__(self, userPrompt: str) -> str:
        """Generate a response from the Azure OpenAI endpoint.
        
        Args:
            userPrompt (str): Prompt provided by the user.
            
        Raises:
            ValueError: If the API response format is unexpected.
            
        Returns:
            str: LLM generated response text.
        """
        headers = {"Content-Type": "application/json", "api-key": self.api_key}
        payload = {
            "messages": [{"role": "user", "content": userPrompt}],
            "temperature": self.temperature,
            "top_p": self.top_p,
        }
        
        response = requests.post(self.endpoint, headers=headers, json=payload)
        response.raise_for_status()
        
        try:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        
        except (KeyError, IndexError) as e:
            raise ValueError(f"Unexpected API response format: {e}\nResponse: {result}")