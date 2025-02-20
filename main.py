import asyncio
import os
from typing import List
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
import requests
from xml.etree import ElementTree
import argparse

# Função para criar o diretório "documentos" se ele não existir
def ensure_directory_exists(directory: str):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Função para obter URLs do sitemap de um site
def get_sitemap_urls(sitemap_url: str) -> List[str]:
    """
    Fetches all URLs from the provided sitemap URL.
    
    Args:
        sitemap_url (str): The URL of the sitemap.xml file.
    
    Returns:
        List[str]: List of URLs extracted from the sitemap.
    """
    try:
        response = requests.get(sitemap_url)
        response.raise_for_status()
        
        # Parse the XML
        root = ElementTree.fromstring(response.content)
        
        # Extract all URLs from the sitemap
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = [loc.text for loc in root.findall('.//ns:loc', namespace)]
        
        return urls
    except Exception as e:
        print(f"Error fetching sitemap: {e}")
        return []

# Função para salvar o conteúdo Markdown em um arquivo único
def save_combined_markdown_to_file(directory: str, site_name: str, combined_content: str):
    """
    Saves the combined Markdown content to a single file named '<site_name>_combined.md'.
    
    Args:
        directory (str): Directory where the file will be saved.
        site_name (str): The base name of the site (used for naming the file).
        combined_content (str): The combined Markdown content to save.
    """
    filename = f"{site_name}_combined.md"
    filepath = os.path.join(directory, filename)
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(combined_content)
    print(f"Saved combined output to: {filepath}")

# Função para salvar o conteúdo Markdown em arquivos separados
def save_split_markdown_to_files(directory: str, site_name: str, markdown_chunks: List[str]):
    """
    Saves the Markdown content to separate files named '<site_name>_1.md', '<site_name>_2.md', etc.
    
    Args:
        directory (str): Directory where the files will be saved.
        site_name (str): The base name of the site (used for naming the files).
        markdown_chunks (List[str]): List of Markdown chunks to save.
    """
    for i, chunk in enumerate(markdown_chunks, start=1):
        filename = f"{site_name}_{i}.md"
        filepath = os.path.join(directory, filename)
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(chunk)
        print(f"Saved: {filepath}")

# Função principal para realizar o crawling sequencial
async def crawl_sequential(urls: List[str], output_dir: str, split_mode: int, site_name: str):
    browser_config = BrowserConfig(
        headless=True,
        # For better performance in Docker or low-memory environments:
        extra_args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"],
    )
    crawl_config = CrawlerRunConfig(
        markdown_generator=DefaultMarkdownGenerator()
    )
    # Create the crawler (opens the browser)
    crawler = AsyncWebCrawler(config=browser_config)
    await crawler.start()
    try:
        session_id = "session1"  # Reuse the same session across all URLs
        combined_content = ""
        markdown_chunks = []
        for url in urls:
            result = await crawler.arun(
                url=url,
                config=crawl_config,
                session_id=session_id
            )
            if result.success:
                print(f"Successfully crawled: {url}")
                markdown_content = result.markdown_v2.raw_markdown
                combined_content += f"# Page: {url}\n\n{markdown_content}\n\n---\n\n"
                
                # If splitting into multiple files, group content into chunks
                if split_mode > 0:
                    markdown_chunks.append(f"# Page: {url}\n\n{markdown_content}\n\n")
        if split_mode == 0:
            # Save everything in one file
            save_combined_markdown_to_file(output_dir, site_name, combined_content)
        elif split_mode > 0:
            # Split into specified number of files
            num_files = split_mode
            total_chunks = len(markdown_chunks)
            chunk_size = total_chunks // num_files + (1 if total_chunks % num_files != 0 else 0)
            
            # Distribute chunks evenly across the specified number of files
            distributed_chunks = [
                markdown_chunks[i * chunk_size:(i + 1) * chunk_size]
                for i in range(num_files)
            ]
            
            # Combine chunks for each file and save
            for i, file_chunks in enumerate(distributed_chunks, start=1):
                file_content = "\n".join(file_chunks)
                filename = f"{site_name}_{i}.md"
                filepath = os.path.join(output_dir, filename)
                with open(filepath, "w", encoding="utf-8") as file:
                    file.write(file_content)
                print(f"Saved: {filepath}")
    finally:
        # After all URLs are done, close the crawler (and the browser)
        await crawler.close()

# Função principal
async def main():
    parser = argparse.ArgumentParser(description="Scrape a website and save the results as Markdown files.")
    parser.add_argument("--site", required=True, help="The base URL of the website to scrape (e.g., https://example.com)")
    parser.add_argument("--split", type=int, nargs='?', const=-1, default=0, 
                        help="Split the output into multiple files. Provide a number to specify how many files to split into. "
                             "If no number is provided, each URL will be saved in a separate file.")
    args = parser.parse_args()

    # Define o diretório de saída
    output_dir = "documentos"
    ensure_directory_exists(output_dir)

    # Constrói a URL do sitemap
    sitemap_url = f"{args.site.rstrip('/')}/sitemap.xml"
    print(f"Fetching URLs from sitemap: {sitemap_url}")

    # Obtém as URLs do sitemap
    urls = get_sitemap_urls(sitemap_url)
    if urls:
        print(f"Found {len(urls)} URLs to crawl")
        # Extrai o nome do site da URL base
        site_name = args.site.replace("https://", "").replace("http://", "").split("/")[0]
        await crawl_sequential(urls, output_dir, args.split, site_name)
    else:
        print("No URLs found to crawl")

if __name__ == "__main__":
    asyncio.run(main())