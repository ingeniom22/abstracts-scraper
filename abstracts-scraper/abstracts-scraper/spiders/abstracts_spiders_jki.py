import scrapy
from urllib.parse import urljoin
import re


class JKISpider(scrapy.Spider):
    name = "jki"

    start_urls = [
        "https://jki.ui.ac.id/index.php/jki/issue/archive/1",
        # "https://jki.ui.ac.id/index.php/jki/issue/archive/2",
        # "https://jki.ui.ac.id/index.php/jki/issue/archive/3",
    ]

    # Set the download delay (in seconds)
    custom_settings = {
        "DOWNLOAD_DELAY": 1,  # Set your desired delay here (e.g., 1 second)
    }

    def parse(self, response):
        for issue_summary in response.css("div.obj_issue_summary"):
            link = issue_summary.css("a.title::attr(href)").get()
            series = issue_summary.css("div.series").get()
            year_re = (
                r"\((\d{4})\)"  # Pattern to match the year in parentheses (four digits)
            )
            match = re.search(year_re, series)
            year = int(match.group(1))

            if year > 2018:
                # Follow the link and send a request to the linked page
                yield scrapy.Request(link, callback=self.parse_linked_page)

    def parse_linked_page(self, response):
        # Extract doi
        for article_summary in response.css("div.obj_article_summary"):
            doi = article_summary.css(".jatsParser__meta-doi a::text").get()
            if doi:
                # Prepend the scheme to the DOI value to form a valid URL
                doi_url = urljoin("https://doi.org/", doi.strip())
                # Follow the link and send a request to the article page to extract abstracts
                yield scrapy.Request(doi_url, callback=self.parse_abstracts)

    def parse_abstracts(self, response):
        # Extract abstract text without HTML tags
        abstract_text = response.css("div.jatsParser__center-article-block")
        full_abstract = " ".join(abstract_text.css("*::text").extract()).strip()

        start_index = full_abstract.find("Abstract")
        end_index = full_abstract.find("Abstrak")
        abstract_clean = full_abstract[
            start_index + len("Abstract") : end_index
        ].strip()

        yield {
            "abstract": abstract_clean,
            "citation": None,
        }
