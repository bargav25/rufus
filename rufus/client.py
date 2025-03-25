import os
import json
from typing import List, Dict
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright
import openai
from openai import OpenAI

class RufusCrawler:
    def __init__(self, max_depth: int = 2, max_pages: int = 10):
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.visited_urls = set()
        self.results = []
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch()

    def _normalize_url(self, url: str) -> str:
        return url.split('#')[0].strip().lower()

    def _extract_links(self, page) -> List[str]:
        links = page.query_selector_all('a')
        return list(set(
            link.get_attribute('href')
            for link in links
            if link.get_attribute('href')
        ))

    def _is_valid_url(self, url: str) -> bool:
        # Basic check: URL should start with http or https
        return url.startswith("http://") or url.startswith("https://")

    def _crawl_page(self, url: str, instructions: str, current_depth: int):
        if current_depth > self.max_depth or len(self.results) >= self.max_pages:
            return

        normalized_url = self._normalize_url(url)
        if normalized_url in self.visited_urls:
            return

        self.visited_urls.add(normalized_url)

        try:
            page = self.browser.new_page()
            page.goto(url, wait_until="domcontentloaded")
            
            # Wait for dynamic content to load.
            page.wait_for_timeout(2000)
            
            text_content = page.inner_text('body')
            
            # Process content with OpenAI.
            processed = self._process_content(text_content, instructions, url)
            if processed.get('relevant'):
                self.results.append(processed)
                
            # Recursively crawl links.
            if current_depth < self.max_depth:
                links = self._extract_links(page)
                for link in links:
                    absolute_url = urljoin(url, link)
                    if self._is_valid_url(absolute_url):
                        self._crawl_page(absolute_url, instructions, current_depth + 1)

            page.close()
        except Exception as e:
            print(f"Error crawling {url}: {str(e)}")

    def _process_content(self, text: str, instructions: str, url: str) -> Dict:
        # Ensure the OpenAI API key is set.
        if not openai.api_key:
            openai.api_key = os.getenv("OPENAI_API_KEY")
            if not openai.api_key:
                raise ValueError("OpenAI API key not set. Please set the OPENAI_API_KEY environment variable.")

        # Build a prompt that instructs OpenAI to analyze and extract relevant information.
        prompt = f"""You are a JSON-only response bot. Analyze the following web content and extract information relevant to the instructions.
IMPORTANT: Respond ONLY with valid JSON, no other text.

Instructions: {instructions}

Web Content:
{text[:3000]}

Return a JSON object in exactly this format:
{{
    "relevant": <boolean>,
    "summary": "<string>",
    "key_points": ["<string>", ...],
    "content_type": "<faq|pricing|product|other>"
}}"""
        client = OpenAI()

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a JSON-only response bot. You must always respond with valid JSON, no other text."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=500
        )

        result_text = response.choices[0].message.content.strip()
        print(result_text)
        try:
            result = json.loads(result_text)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from OpenAI response: {e}")
            print(f"Raw response: {result_text}")
            result = {"relevant": False, "summary": "", "key_points": [], "content_type": "other"}
        
        result['source_url'] = url
        return result

    def crawl(self, start_url: str, instructions: str) -> List[Dict]:
        self._crawl_page(start_url, instructions, 0)
        return self.results

    def __del__(self):
        try:
            self.browser.close()
            self.playwright.stop()
        except Exception:
            pass

class RufusClient:
    def __init__(self, api_key: str):
        os.environ["OPENAI_API_KEY"] = api_key

    def scrape(self, url: str, instructions: str, max_depth: int = 2) -> List[Dict]:
        crawler = RufusCrawler(max_depth=max_depth)
        return crawler.crawl(url, instructions)

if __name__ == "__main__":
    client = RufusClient(api_key="XXXXXXXXXXXXX")
    # documents = client.scrape(
    #     url="https://www.boxofficemojo.com/",
    #     instructions="How much Mickey 17 collected this sunday ?"
    # )
    # print(json.dumps(documents, indent=2))

    documents = client.scrape(
        url="https://sites.google.com/site/mittangoclub/",
        instructions="What's the spring schedule for classes?"
    )
    print(json.dumps(documents, indent=2))