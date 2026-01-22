import asyncio
from browser_use import Agent
from browser_use import ChatOllama

# Test with a very simple task
llm = ChatOllama(
    model="deepseek-r1:7b",
    host="http://169.254.182.70:11434",
    timeout=120,
)

async def main():
    agent = Agent(
        task="Go to https://example.com and tell me what you see on the page.",
        llm=llm,
    )
    result = await agent.run()
    print("\n=== AGENT RESULT ===\n", result)

if __name__ == "__main__":
    asyncio.run(main())


