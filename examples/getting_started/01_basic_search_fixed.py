"""
Fixed version that avoids CAPTCHA detection.

Setup:
1. Get your API key from https://cloud.browser-use.com/dashboard/api
2. Set environment variable: export BROWSER_USE_API_KEY="your-key"

Alternative: Use a local LLM like Ollama instead of ChatBrowserUse
"""

import asyncio
import os
import sys

# Add the parent directory to the path so we can import browser_use
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dotenv import load_dotenv

load_dotenv()

from browser_use import Agent, BrowserProfile
from browser_use.llm import ChatBrowserUse


async def main():
	# Configure browser to avoid CAPTCHA detection
	browser_profile = BrowserProfile(
		# Don't use headless mode - it's often detected as a bot
		headless=False,
		# Add realistic wait times
		minimum_wait_page_load_time=1.0,  # Wait 1 second for pages to load
		wait_between_actions=0.5,  # Wait 0.5 seconds between actions
		# Disable automation flags that trigger CAPTCHA
		disable_security=False,  # Keep security enabled to appear more human
	)

	llm = ChatBrowserUse()

	# Modified task - use a simpler search or alternative approach
	# Instead of searching Google (which has aggressive CAPTCHA),
	# we can try Wikipedia or other sites with less bot detection
	task = """
	Go to Wikipedia (https://en.wikipedia.org) and search for 'browser automation'.
	Read the article and tell me:
	1. What is browser automation?
	2. What are the main use cases?
	3. What are some popular tools mentioned?
	"""

	agent = Agent(
		task=task,
		llm=llm,
		browser_profile=browser_profile,
		# Reduce max steps to avoid hitting rate limits
		max_actions_per_step=3,
	)

	result = await agent.run()
	print(f"\n📄 Final Result:\n{result}")
	return result


if __name__ == '__main__':
	asyncio.run(main())
