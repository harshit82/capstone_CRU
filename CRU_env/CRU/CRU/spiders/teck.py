import scrapy
from ..items import CruItem
import os
from ..utils import get_filename, ends_with_pdf


class TeckSpider(scrapy.Spider):
    """
    Scrapy Spider to scrape annual reports from Teck's financial reports archive.

      Attributes:
          name (str): The name of the spider.
          allowed_domains (list): List of domains that the spider is allowed to crawl.
          start_urls (list): List of initial URLs to start the crawling process.
    """
    name = "teck"
    allowed_domains = ["www.teck.com"]
    start_urls = ['https://www.teck.com/investors/financial-reports/annual-reports-archive/']

    def parse(self, response):
        """
        Parses the response to extract URLs of annual reports ending with '.pdf'
        and initiates requests to download these files.

           Args:
               response (scrapy.http.Response): The HTTP response object containing the page content.

           Yields:
               scrapy.Request: A Scrapy request for each PDF URL found, with the filename passed in metadata.
        """
        link_obj = CruItem()
        report_urls = response.css('div[class="row row-cols-4 justify-content-center"] a::attr(href)').extract()
        reports = [report for report in report_urls if ends_with_pdf(report)]
        link_obj['file_urls'] = reports
        for url in link_obj['file_urls']:
            filename = get_filename(url)
            yield scrapy.Request(url=url, callback=self.save_file, meta={'filename': filename})

    def save_file(self, response):
        """
        Saves the downloaded PDF file to the local filesystem.

           Args:
               response (scrapy.http.Response): The HTTP response object containing the file content.

           Creates:
               - The directory 'input_dataset' if it does not exist.
               - Saves the file to the specified directory with the filename provided in metadata.
        """
        filename = response.meta['filename']
        directory = 'input_dataset'
        file_path = os.path.join(directory, f'{filename}.pdf')

        # Create directory if it does not exist
        if not os.path.exists(directory):
            print("not found")

        with open(file_path, 'wb') as f:
            f.write(response.body)
