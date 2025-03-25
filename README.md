# Rufus - Intelligent Web Data Extraction for RAG Pipelines

Rufus is an AI-powered tool designed to intelligently crawl websites based on user-defined prompts, extract relevant content, and synthesize structured documents for use in Retrieval-Augmented Generation (RAG) pipelines. It leverages Playwright for web crawling (including dynamic content) and the OpenAI API for content analysis.

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

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/rufus.git
cd rufus
```

### 2. Create and Activate a Virtual Environment

On macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```


### 3. Install Playwright Browsers

After installing the package, run:


```bash
python -m playwright install chromium
```

This command downloads the necessary browser binaries for Playwright.

## Usage

You can use Rufus as a library in your Python projects. For example:

```python
from rufus import RufusClient
import os

# Set your OpenAI API key (either via environment variable or directly)
key = os.getenv("OPENAI_API_KEY")
client = RufusClient(api_key=key)

# Define extraction instructions and target URL
instructions = "How much did Mickey 17 collect this Sunday?"
documents = client.scrape("https://www.boxofficemojo.com/", instructions)

print(documents)
```

## Testing

To run the tests, execute:

```bash
python -m unittest discover tests
```

## Repository Structure

```
rufus/
├── rufus/
│   ├── __init__.py         # Package initializer (exposes RufusClient)
│   ├── client.py           # Contains RufusCrawler and RufusClient classes
│   └── utils.py            # (Optional) Helper functions
├── tests/
│   └── test_client.py      # Basic tests for RufusClient
├── setup.py                # Packaging configuration
├── requirements.txt        # Dependency list
└── README.md               # Project documentation (this file)
```



## Additional Notes

- **OpenAI API Key:**  
  Make sure to set your OpenAI API key either through the OPENAI_API_KEY environment variable or by passing it when initializing the RufusClient.

- **Playwright:**  
  Rufus uses Playwright to handle dynamic web content. Don’t forget to run `python -m playwright install` after installing the package.

- **Editable Installation:**  
  The `pip install -e .` command installs Rufus in editable mode, allowing for rapid development and testing.

Enjoy using Rufus for intelligent web data extraction!
