# NovelBin Audiobook Maker

A Python application that scrapes novel content from novelbin.com and saves it in text files for audiobook creation.

## ⚠️ Disclaimer

This tool is provided for educational purposes only. Please be aware that:
- Web scraping may be against the terms of service of some websites
- Always respect website's robots.txt and rate limits
- Make sure you have the right to use the content you're scraping
- The author is not responsible for any misuse of this tool

## Features

- Scrapes novel chapters from novelbin.com
- Saves chapters in batches of 50
- Progress tracking with progress bar
- Connection pooling for faster scraping
- Automatic retry mechanism for failed requests
- Error handling and logging

## Requirements

- Python 3.6 or higher
- Required Python packages (install using `pip install -r requirements.txt`):
  - requests
  - beautifulsoup4
  - tqdm

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/audiobook-maker.git
cd audiobook-maker
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the script:
```bash
python audiobook_maker.py
```

2. When prompted, enter the URL of the first chapter of the novel you want to scrape (e.g., https://novelbin.com/b/super-gene/chapter-1)

3. The script will:
   - Create a 'novel_chapters' directory
   - Scrape chapters in batches of 50
   - Save each batch to a separate file (chapters_1.txt, chapters_2.txt, etc.)
   - Show progress with a progress bar

## Output

The scraped chapters will be saved in the 'novel_chapters' directory with the following format:
- Each file contains up to 50 chapters
- Chapters are separated by a line of equal signs
- Original chapter formatting is preserved

## Performance Optimizations

- Connection pooling for faster requests
- Automatic retry mechanism for failed requests
- Optimized delay between requests
- Efficient HTML parsing

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 