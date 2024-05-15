import requests
import user_token
import corpus.bubbletea_menu as bbt

system_prompt = "你是一个奶茶店店长，可以礼貌地根据用户需求推荐他们的产品。并将结果翻译成中文。"
menu_prompt = "店内产品和介绍如下：" + bbt.coco_menu_raw
final_system_prompt = system_prompt + menu_prompt

user_prompt = "我想喝带巨峰葡萄和柠檬的水水！"

data = {
    "messages": [
        {
            "role": "system",
            "content": final_system_prompt
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ],
    "model": "meta-llama/Meta-Llama-3-70B-Instruct",
    "max_tokens": 512,
    "temperature": 0.7,
    "top_p": 0.9
}

response = requests.post(user_token.url, headers=user_token.headers, json=data)
answer_json = response.json()
print(answer_json)
print(answer_json["choices"][0]["message"]["content"])