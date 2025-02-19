from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio
from dotenv import load_dotenv
load_dotenv()

async def main():
    agent = Agent(
        task=(
            'Validate the following test case about successfully recovering your username from RBC'
            "1. Go to RBC Royal bank Website"
            '3. Click on sign in and then on Recover your username'
            '4. Validate the next screen gives important notice about having a valid email id on file with RBC '
            '5.Select Client Card. Enter client card number 1234 and email b.m@gmail.com'
            '6.Assert the text One or more of your responses do not match our records.'
        ),
        llm=ChatOpenAI(model="gpt-4o"),
    )
    result = await agent.run()
    print(result)

asyncio.run(main())