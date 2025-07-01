"""
Uses Crawl4AI to crawl a Markdown (.md, .txt) document, then splits the content into chunks based on # and ## headers.
Prints each chunk, and saves any Markdown links ([text](URL)) found in each chunk to a Supabase database.

Usage:
1. Set the target URL in the main() function.
2. Run the script to perform crawling, chunk splitting, printing, and link saving in sequence.
"""

import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
import re
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def save_to_supabase(url, link_url, description):
    data = {
        "source_url": url,  # The original document URL that was crawled
        "url": link_url,  # The extracted link URL
        "description": description,  # The description of the extracted link
        "time": datetime.utcnow().isoformat(),
    }
    supabase.table("pydantic_docs_llms").insert(data).execute()


async def scrape_and_chunk_markdown(url: str):
    """
    Scrape a Markdown page and split into chunks by # and ## headers.
    """
    browser_config = BrowserConfig(headless=True)
    crawl_config = CrawlerRunConfig()
    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(url=url, config=crawl_config)
        if not result.success:
            print(f"Failed to crawl {url}: {result.error_message}")
            return
        markdown = result.markdown
        # Split by headers (#, ##)
        # Find all # and ## headers to use as chunk boundaries
        header_pattern = re.compile(r"^(# .+|## .+)$", re.MULTILINE)
        headers = [m.start() for m in header_pattern.finditer(markdown)] + [
            len(markdown)
        ]
        chunks = []
        # Split the markdown into chunks between headers
        for i in range(len(headers) - 1):
            chunk = markdown[headers[i] : headers[i + 1]].strip()
            if chunk:
                chunks.append(chunk)
        print(f"Split into {len(chunks)} chunks:")
        for idx, chunk in enumerate(chunks):
            print(f"\n--- Chunk {idx+1} ---\n{chunk}\n")
            # Find Markdown link patterns
            link_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
            for match in link_pattern.finditer(chunk):
                description = match.group(1)
                link_url = match.group(2)
                print(f"Saving: description={description}, url={link_url}")
                save_to_supabase(url, link_url, description)


if __name__ == "__main__":
    url = "https://docs.pydantic.dev/latest/llms.txt"
    asyncio.run(scrape_and_chunk_markdown(url))
