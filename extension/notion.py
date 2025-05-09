import os
from notion_client import Client
from config.secret import NOTION_KEY, SA_DATABASE_ID

api_key = NOTION_KEY

# Initialize Notion client
os.environ["http_proxy"] = ""
os.environ["https_proxy"] = ""
notion = Client(auth=api_key)


# https://www.notion.so/{workspace}/{database_id}?v={view_id}
# https://www.notion.so/timothyhay/298dfef81f834bfaa335e65e7c1c7249?v=cba1cfb5a5c44ffd954d88ec5edbfcb8&pvs=4
def read_database(database_id):
    try:
        results = notion.databases.query(database_id=database_id)
        # 遍历数据库中的每一行（页面）
        for page in results["results"]:
            properties = page["properties"]
            # 打印每一列的名称和值
            for prop_name, prop_value in properties.items():
                # 根据属性类型提取值
                if prop_value["type"] == "title":
                    value = prop_value["title"][0]["plain_text"] if prop_value["title"] else ""
                elif prop_value["type"] == "rich_text":
                    value = prop_value["rich_text"][0]["plain_text"] if prop_value["rich_text"] else ""
                elif prop_value["type"] == "number":
                    value = prop_value["number"]
                elif prop_value["type"] == "select":
                    value = prop_value["select"]["name"] if prop_value["select"] else ""
                else:
                    value = "Unsupported type"
                print(f"{prop_name}: {value}")
            print("-" * 50)
    except Exception as e:
        print(f"Error: {e}")

# 执行查询
read_database(SA_DATABASE_ID)
