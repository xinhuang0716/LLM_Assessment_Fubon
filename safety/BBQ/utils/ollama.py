import requests


def ollama_response(prompt: str, model: str = "gemma3:1b", stream: bool = False, url: str = "http://172.21.134.121:11434/api/generate") -> str:
    """Gets a response from the Ollama LLM.

    Args:
        prompt (str): Prompt to send to the model.
        model (_type_, optional): The response LLM model. Defaults to "gemma3:1b".
        stream (bool, optional): Whether to stream the response. Defaults to False.
        url (str, optional): API endpoint URL. Defaults to `http://172.21.134.121:11434/api/generate`.

    Returns:
        str: LLM response.
    """

    # payload
    headers = {"Content-Type": "application/json"}
    data = {
        "model": model,
        "prompt": prompt,
        "stream": stream
    }

    # request
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

    return response.json()["response"]