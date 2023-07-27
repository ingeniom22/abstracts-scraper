# Abstracts Scraper

**Abstracts Scraper** is a Scrapy project designed to collect abstracts from various journals. This documentation provides step-by-step instructions on how to set up and use the project to collect abstracts.

WIP for COMPFEST2023

## Prerequisites
- Python 3.11
- Scrapy

## Setup

1. Clone the Abstracts Scraper repository from GitHub:

   ```bash
   git clone https://github.com/yourusername/abstracts-scraper.git
   cd abstracts-scraper
   ```

2. Create a virtual environment and activate it:

   ```bash
   # On macOS and Linux
   python3 -m venv venv
   source venv/bin/activate

   # On Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Configure the Spider**: Open the `abstracts_scraper/spiders/pjpi_spider.py` file and adjust the spider logic

2. **Run the Spider**: To start scraping, run the spider using the following command:
   ```bash
   scrapy crawl pjpi -O pjpi.jsonl
   ```

3. **Data Output**: After the spider finishes scraping, you will find the collected abstracts in the `pjpi.jsonl` file in the project's root directory. Each line in the `jsonl` file contains a JSON object representing an abstract.

## Advanced Configuration

If you want to scrape abstracts from multiple journals, you can create additional spider classes in the `abstracts_scraper/spiders/` directory. Each spider should target a different journal website and define the necessary parsing logic.


You can modify the spider names and the output file names as per your preference.
