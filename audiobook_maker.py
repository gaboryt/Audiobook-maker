import requests
from bs4 import BeautifulSoup
import time
import os
from tqdm import tqdm
import re
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class NovelScraper:
    def __init__(self, start_url):
        self.start_url = start_url
        self.base_url = "https://novelbin.com"
        
        # Set up session with retry strategy
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.chapters = []
        self.current_file_number = 1

    def get_chapter_content(self, url):
        try:
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Get the chapter content
            content_div = soup.find('div', id='chr-content')
            if not content_div:
                return None, None
            
            # Find the unlock-buttons div to know where to stop
            unlock_div = content_div.find('div', class_='unlock-buttons')
            
            # Get all paragraphs before the unlock-buttons div
            paragraphs = []
            for element in content_div.find_all(['p', 'div']):
                if element == unlock_div:
                    break
                if element.name == 'p':
                    text = element.get_text().strip()
                    if text:
                        paragraphs.append(text)
            
            chapter_text = '\n\n'.join(paragraphs)
            
            # Find the next chapter link
            next_chapter_link = soup.find('a', id='next_chap')
            next_url = next_chapter_link['href'] if next_chapter_link else None
            
            return chapter_text, next_url
        except Exception as e:
            print(f"Error processing {url}: {str(e)}")
            return None, None

    def save_chapters(self, chapters, file_number):
        if not chapters:
            return
        
        # Create output directory if it doesn't exist
        os.makedirs('novel_chapters', exist_ok=True)
        
        # Save chapters to file
        filename = f'novel_chapters/chapters_{file_number}.txt'
        with open(filename, 'w', encoding='utf-8') as f:
            for chapter in chapters:
                f.write(chapter)
                f.write("\n\n" + "="*50 + "\n\n")
        
        print(f"Saved {len(chapters)} chapters to {filename}")

    def scrape_novel(self):
        current_url = self.start_url
        chapters_in_current_file = []
        chapter_count = 0
        
        with tqdm(total=50, desc="Scraping chapters") as pbar:
            while current_url and chapter_count < 50:
                chapter_text, next_url = self.get_chapter_content(current_url)
                
                if chapter_text:
                    chapters_in_current_file.append(chapter_text)
                    chapter_count += 1
                    pbar.update(1)
                
                current_url = next_url
                
                # Save every 50 chapters
                if len(chapters_in_current_file) == 50:
                    self.save_chapters(chapters_in_current_file, self.current_file_number)
                    chapters_in_current_file = []
                    self.current_file_number += 1
                    chapter_count = 0
                    pbar.reset()
                
                # Reduced delay to be more efficient while still being respectful
                time.sleep(0.5)
        
        # Save any remaining chapters
        if chapters_in_current_file:
            self.save_chapters(chapters_in_current_file, self.current_file_number)

def main():
    print("NovelBin Audiobook Maker")
    print("=" * 30)
    
    start_url = input("Enter the URL of the first chapter (e.g., https://novelbin.com/b/super-gene/chapter-1): ")
    
    if not start_url.startswith("https://novelbin.com"):
        print("Error: Please provide a valid NovelBin URL")
        return
    
    scraper = NovelScraper(start_url)
    scraper.scrape_novel()
    
    print("\nScraping completed! Check the 'novel_chapters' directory for the saved chapters.")

if __name__ == "__main__":
    main() 