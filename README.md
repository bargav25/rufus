# Rufus - Intelligent Web Data Extraction

Rufus is an AI-powered tool designed to intelligently crawl websites based on user-defined prompts, extract relevant content, and synthesize structured documents.

## Features

- **Intelligent Crawling:**  
  Recursively crawl websites with configurable depth and page limits, handling both static and dynamic content.

- **Selective Extraction:**  
  Use user-defined instructions to filter and extract only the most relevant data from web pages.

- **Content Synthesis:**  
  Analyze and synthesize web content using the OpenAI API to produce a structured JSON document with summaries, key points, and content types.

- **Easy Integration:**  
  Designed as a Python package with a simple API, making it easy to integrate into your RAG pipeline.


## Installation

```bash
# Install the package
pip install -e .

# Install Playwright browser
python -m playwright install chromium
```

## Usage

```python
from rufus import RufusClient

# Set your OpenAI API key
client = RufusClient(api_key="your-api-key")

# Define extraction instructions and target URL
instructions = "What are the key features of this product?"
documents = client.scrape("https://example.com", instructions)

print(documents)
```

## Requirements

- Python 3.8+
- OpenAI API key
- Playwright browser (install with `python -m playwright install chromium`)
