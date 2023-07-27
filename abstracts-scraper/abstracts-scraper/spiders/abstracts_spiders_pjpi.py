import scrapy


class PJPISpider(scrapy.Spider):
    name = "pjpi"

    start_urls = [
        "https://journal.walisongo.ac.id/index.php/Psikohumaniora/issue/archive",
        #
    ]

    # Set the download delay (in seconds)
    custom_settings = {
        "DOWNLOAD_DELAY": 1,  # Set your desired delay here (e.g., 1 second)
    }

    def parse(self, response):
        for issue_year in response.css("div#issues > div"):
            vol_text = issue_year.css("h3::text")
            if vol_text:
                year = int(
                    issue_year.css("h3::text")
                    .get()
                    .strip()
                    .replace(" ", "")
                    .replace(":", "")
                )

                if year > 2018:
                    for issue in issue_year.css("div.list"):
                        href = issue.css("h4 a::attr(href)").get()
                        yield scrapy.Request(href, callback=self.parse_linked_page)

    def parse_linked_page(self, response):
        # Extracting all the links of the articles from the current page
        for article_link in response.css("div.tocTitle > a::attr(href)").getall():
            yield scrapy.Request(article_link, callback=self.parse_article)

    def parse_article(self, response):
        # Extracting data from the article page
        abstract = response.css("meta[name='DC.Description']::attr(content)").get()
        citation_title = response.css(
            "meta[name='citation_title']::attr(content)"
        ).get()
        doi = response.css("meta[name='DC.Identifier.DOI']::attr(content)").get()

        yield {
            "Abstract": abstract.strip(),
            "Citation Title": citation_title.strip(),
            "DOI": doi,
            # Add other fields you want to collect
        }
