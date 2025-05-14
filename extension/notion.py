import os
from textwrap import dedent

import pandas as pd
import httpx
from google.genai import types
from notion_client import Client
from config.secret import NOTION_KEY, SA_DATABASE_ID
from config.setup import setup_proxy
from config.secret import GEMINI_KEY, GEMINI_OAI_BASE_URL

from google import genai
from pydantic import BaseModel

class SentimentEvaluation(BaseModel):
    recipe_name: str
    score: int


# Initialize Notion client
setup_proxy()
notion = Client(auth=NOTION_KEY)

list_users_response = notion.users.list()
print(list_users_response)


# https://www.notion.so/timothyhay/298dfef81f834bfaa335e65e7c1c7249?v=cba1cfb5a5c44ffd954d88ec5edbfcb8&pvs=4
def read_my_heart(database_id):

    sort_index = [
        {
            "property": "Week",
            "direction": "ascending"
        },
        {
            "property": "Created time",
            "direction": "ascending"
        }
    ]
    filter = {
    "property": "Created time",
    "date": {
            "before": "2025-01-01"
        }
    }


    results = notion.databases.query(database_id=database_id, sorts=sort_index, filter=filter)
    # https://www.notion.so/{workspace}/{database_id}?v={view_id}
    sentiment_prompt_list = []
    sentiment_dataframe_list = []
    for page in results["results"]:
        properties = page["properties"]

        if not properties['Description']['rich_text']:
            continue
        extracted_data = {
            'Week': properties['Week']['formula']['number'],
            'Title': properties['Title']['title'][0]['plain_text'],
            'OutsideHour': properties['OutsideHour']['number'],
            'Mood': properties['Mood']['number'],
            'Description': properties['Description']['rich_text'][0]['plain_text'],
            #'Synced': properties['Synced']['checkbox'],
            #'Afterthought': properties['Afterthought']['checkbox'],
            #'Created_by': properties['Created by']['created_by']['name'],
            'Created_time': properties['Created time']['created_time'],
            #'Last_edited_by': properties['Last edited by']['last_edited_by']['name'],
            #'Last_edited_time': properties['Last edited time']['last_edited_time']
        }
        sentiment_prompt_list.append(extracted_data)
        # dataframe_entry = extracted_data
        # dataframe_entry['Created time'] = properties['Created time']['created_time']
        # sentiment_dataframe_list.append(dataframe_entry)

        print(extracted_data)
        print("-" * 50)
    return sentiment_prompt_list

if __name__ == '__main__':
    records = read_my_heart(SA_DATABASE_ID)

    client = genai.Client(api_key=GEMINI_KEY)
    system_prompt = dedent('''
    你是能力极强的情感分析师。接下来你会收到用户关于某个休息日的描述，你需要分析用户的日程描述，给出一段简短的评价，以及一个由你决定的当日心情量化得分。
    接收到的输入以一个JSON表示，包含的键与含义如下：
    {
        'Week': '记录所在周序号', 
        'Title': '记录标题，通常无意义', 
        'OutsideHour': '出门时长', 
        'Mood': '用户的主观心情打分，是0~5之间的浮点数，越高表示记录时认为自己的心情越好', 
        'Description': '当日日程的详细描述，你应当以此为主要依据来分析用户心情', 
        'Created_time': '记录时间'
    }

    请注意：
    1. 你的最终目的是积极地引导用户理解如何过上更快乐、更有意义的生活，因此你需要在评价中使用温和语气对用户进行正面引导。
    2. 你仍然需要客观地根据'Description'字段内容给出一个客观的用户一日心情评价。这个评价不需要参考'Mood'字段，而应该由你的独立分析给出。
    ''').strip()

    response_format = '你的回复也应该是一个包含自然语言评价(键为"mood_analysis")和一个当日心情状况的量化打分(键为"Mood_evaluation")的JSON呈现。'
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction=system_prompt),
        contents="Explain how AI works in a few words"
    )
    print(response.text)
