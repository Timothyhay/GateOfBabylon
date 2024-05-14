import requests
import user_token

data = {
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful and polite assistant."
        },
        {
            "role": "user",
            "content": "What is love?"
        }
    ],
    "model": "meta-llama/Meta-Llama-3-70B-Instruct",
    "max_tokens": 512,
    "temperature": 0.7,
    "top_p": 0.9
}

response = requests.post(user_token.url, headers=user_token.headers, json=data)
print(response.json())