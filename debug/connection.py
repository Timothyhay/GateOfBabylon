from agents import Agent, Runner

from openai import AsyncOpenAI
from agents import set_default_openai_client


from google import genai

from config.secret import GEMINI_KEY

from google import genai

from config.setup import setup_proxy

setup_proxy()


client = genai.Client(api_key=GEMINI_KEY)

response = client.models.generate_content(
    model="gemini-2.0-flash", contents="Explain how AI works in a few words"
)
print(response.text)

custom_client = AsyncOpenAI(base_url="...", api_key="...")
set_default_openai_client(custom_client)

agent = Agent(name="Assistant", instructions="You are a helpful assistant")

result = Runner.run_sync(agent, "Write a haiku about recursion in programming.")
print(result.final_output)

# Code within the code,
# Functions calling themselves,
# Infinite loop's dance.