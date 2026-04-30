# Create venv and install dependencies:
uv sync

source .venv/bin/activate
# Then install Chromium:
uv pip install playwright && playwright install chromium
uv pip install steel-sdk
