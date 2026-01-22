"""
Fixed version using Ollama (free, no API key needed) that avoids CAPTCHA detection.

Setup:
1. Install Ollama: https://github.com/ollama/ollama
2. Run: ollama pull llama3.2:3b  (or any other model)
3. Run: ollama serve
4. Run this script

This version:
- Uses local Ollama instead of cloud API
- Configures browser to avoid CAPTCHA
- Uses Wikipedia instead of Google (less aggressive bot detection)
"""

import asyncio
import os
import sys

# Add the parent directory to the path so we can import browser_use
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dotenv import load_dotenv

load_dotenv()

from browser_use import Agent, BrowserProfile
from browser_use.llm import ChatOllama


async def main():
	# Configure browser to avoid CAPTCHA detection
	browser_profile = BrowserProfile(
		# Don't use headless mode - it's often detected as a bot
		headless=False,
		# Add realistic wait times to appear more human
		minimum_wait_page_load_time=2.0,  # Wait 2 seconds for pages to load
		wait_between_actions=1.0,  # Wait 1 second between actions
		# Keep security settings normal
		disable_security=False,
	)

	# Use Ollama with a small, fast model
	# Popular options: llama3.2:3b, llama3.1:8b, qwen2.5:3b
	llm = ChatOllama(model='llama3.2:3b', temperature=0.0)

	# Modified task - use Wikipedia instead of Google
	# Wikipedia is much more bot-friendly and rarely shows CAPTCHAs
	task = """
	Go to Wikipedia (https://en.wikipedia.org) and search for 'browser automation'.
	Read the article and tell me the top 3 key points about what browser automation is and what it's used for.
	"""

	agent = Agent(
		task=task,
		llm=llm,
		browser_profile=browser_profile,
	)

	result = await agent.run()
	print(f"\n📄 Final Result:\n{result}")
	return result


if __name__ == '__main__':
	print("🚀 Starting browser automation with Ollama...")
	print("💡 Make sure Ollama is running: ollama serve")
	print("💡 Make sure you have the model: ollama pull llama3.2:3b\n")
	asyncio.run(main())
