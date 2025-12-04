import requests


def gemini_response(prompt: str, api_key: str = "", model: str = "gemini-2.0-flash", url: str = "https://generativelanguage.googleapis.com/v1beta/models") -> str:
    """Gets a response from the Gemini LLM.

    Args:
        prompt (str): Prompt to send to the model.
        api_key (str, optional): API key for authentication. Defaults to "".
        model (str, optional): The response LLM model. Defaults to "gemini-2.0-flash".
        url (_type_, optional): _description_. Defaults to "https://generativelanguage.googleapis.com/v1beta/models".

    Returns:
        str: _description_
    """

    # payload
    headers = {"Content-Type": "application/json", "X-goog-api-key": api_key}
    data = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.3, "topP": 0.95, "topK": 40},
    }

    # request
    response = requests.post(f"{url}/{model}:generateContent", headers=headers, json=data)
    response.raise_for_status()

    return response.json()["candidates"][0]["content"]["parts"][0]["text"]