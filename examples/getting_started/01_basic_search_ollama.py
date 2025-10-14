import asyncio
import logging
import os
import sys
from datetime import datetime

# Add the parent directory to the path so we can import browser_use
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dotenv import load_dotenv

load_dotenv()

# Set environment variables for maximum logging detail
os.environ['BROWSER_USE_LOGGING_LEVEL'] = 'DEBUG'
os.environ['BROWSER_USE_DEBUG'] = 'true'

from browser_use import Agent
from browser_use import ChatOllama


REMOTE_OLLAMA = "http://169.254.182.70:11434"  # e.g. "http://203.0.113.10:11434"

# Setup logging to file in current directory
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
script_dir = os.path.dirname(os.path.abspath(__file__))
log_filename = os.path.join(script_dir, f"browser_automation_log_{timestamp}.log")

# Configure logging to capture all browser-use operations
file_handler = logging.FileHandler(log_filename, mode='w')
file_handler.setLevel(logging.DEBUG)  # Capture all levels
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

# Configure root logger to capture all browser-use logs
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
root_logger.handlers.clear()  # Clear any existing handlers
root_logger.addHandler(file_handler)
root_logger.addHandler(console_handler)

# Specifically configure browser-use loggers for detailed output
browser_loggers = [
    'browser_use',
    'browser_use.agent',
    'browser_use.browser',
    'browser_use.tools',
    'browser_use.dom',
    'Agent',
    'BrowserSession',
    'tools'
]

for logger_name in browser_loggers:
    browser_logger = logging.getLogger(logger_name)
    browser_logger.setLevel(logging.DEBUG)
    browser_logger.propagate = True  # Ensure messages go to root logger

# Ensure immediate flushing
file_handler.flush()

logger = logging.getLogger(__name__)

async def main():
	logger.info(f"Starting browser automation task. Logs will be saved to: {log_filename}")
	logger.info("="*80)

	logger.info(f"Initializing Ollama LLM...")
	llm = ChatOllama(model="deepseek-r1:7b", host=REMOTE_OLLAMA, timeout=120.0)

	task = "Search Google for 'what is browser automation' and tell me the top 3 results"
	logger.info(f"Task: {task}")
	logger.info(f"Using Ollama model: deepseek-r1:7b at {REMOTE_OLLAMA}")

	logger.info("Creating browser automation agent...")
	agent = Agent(
		task=task,
		llm=llm,
		llm_timeout=120,  # 2 minutes for LLM calls
		step_timeout=300   # 5 minutes for each step
	)

	logger.info("Starting agent execution...")
	logger.info("="*80)

	try:
		result = await agent.run()
		logger.info("="*80)
		logger.info("Task completed successfully!")
		logger.info(f"Final result: {result}")

		# Force flush all handlers to ensure logs are written
		for handler in logging.getLogger().handlers:
			if hasattr(handler, 'flush'):
				handler.flush()

	except Exception as e:
		logger.error("="*80)
		logger.error(f"Task failed with error: {e}")
		logger.error("="*80)

		# Force flush on error too
		for handler in logging.getLogger().handlers:
			if hasattr(handler, 'flush'):
				handler.flush()
		raise


if __name__ == '__main__':
	asyncio.run(main())
