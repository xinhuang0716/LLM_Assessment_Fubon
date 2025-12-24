import requests


class OllamaLLM:
    """Configurable Ollama LLM that can be called directly."""
    
    def __init__(self, endpoint: str, model: str, stream: bool = False, **kwargs):
        """Initialize Ollama LLM with configuration.
        
        Args:
            endpoint (str): The endpoint URL for the API request.
            model (str): The model to use for generating the response.
            stream (bool): Whether to stream the response or not.
            **kwargs: Additional parameters for the request.
        """
        self.endpoint = endpoint
        self.model = model
        self.stream = stream
        self.kwargs = kwargs
    
    def __call__(self, userPrompt: str) -> str:
        """Generate a response from the Ollama endpoint.
        
        Args:
            userPrompt (str): Prompt provided by the user.
            
        Returns:
            str: LLM generated response text.
        """
        headers = {"Content-Type": "application/json"}
        data = {"model": self.model, "prompt": userPrompt, "stream": self.stream, **self.kwargs}
        
        response = requests.post(self.endpoint, headers=headers, json=data)
        response.raise_for_status()
        
        return response.json()["response"]