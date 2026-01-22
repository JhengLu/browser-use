import asyncio
from browser_use import Agent
from browser_use import ChatOllama

# EITHER use local Ollama (default port)…
# llm = ChatOllama(model="llama3.1:8b")  # local ollama

# …OR point to your remote Ollama explicitly:
llm = ChatOllama(
    model="deepseek-r1:7b",
    host="http://169.254.182.70:11434",  # change me or remove for local
    timeout=120,
)

async def main():
    agent = Agent(
        task="Go to https://github.com/JhengLu/browser-use and read the first paragraph of the README.",
        llm=llm,
    )
    result = await agent.run()
    print("\n=== AGENT RESULT ===\n", result)

if __name__ == "__main__":
    asyncio.run(main())
