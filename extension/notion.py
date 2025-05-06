import os
from notion_client import Client
from config.secret import NOTION_KEY, SA_DATABASE_ID

api_key = NOTION_KEY

# Initialize Notion client
notion = Client(auth=api_key)


async def query_database(database_id):
    """Query a Notion database for pages with 'Last ordered' date after 2022-12-31."""
    print("Querying database...")
    last_ordered_in_2023 = await notion.databases.query(
        database_id=database_id,
        # filter={
        #     "property": "Last ordered",
        #     "date": {
        #         "after": "2022-12-31"
        #     }
        # }
    )

    print("Pages with the 'Last ordered' date after 2022-12-31:")
    print(last_ordered_in_2023)


async def main():
    database_id = SA_DATABASE_ID
    await query_database(database_id)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())