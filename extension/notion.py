import os
import pandas as pd
import httpx
from notion_client import Client
from config.secret import NOTION_KEY, SA_DATABASE_ID
from config.setup import setup_proxy

api_key = NOTION_KEY

# Initialize Notion client
setup_proxy()
notion = Client(auth=api_key)

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
