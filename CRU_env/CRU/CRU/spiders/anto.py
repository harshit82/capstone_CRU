import scrapy
from ..items import CruItem
import os
from ..utils import get_filename


class AntoSpider(scrapy.Spider):
    """
     A Scrapy spider that downloads PDF files from a website, specifically those
     containing the word 'annual' in their URL.

         Attributes:
             name (str): The name of the spider.
             start_urls (list): List of initial URLs to start the crawling process.
             base_url (str): Base URL to prepend to relative links.
     """
    name = "anto"
    allowed_domains = ["www.antofagasta.co.uk"]
    start_urls = ['https://www.antofagasta.co.uk/investors/reports-presentations/']
    base_url = 'https://www.antofagasta.co.uk'

    def parse(self, response):
        """
        Parses the response to extract links that contain the word 'annual' and
        initiates requests to download these files.

           Args:
               response (scrapy.http.Response): The HTTP response object containing the page content.

           Yields:
               scrapy.Request: A Scrapy request for each file URL found, with the filename passed in metadata.
        """
        link_obj = CruItem()
        links = response.css('a[class="cta-small"]::attr(href)').extract()
        annual_links = [link for link in links if 'annual' in link.lower()]
        link_obj['file_urls'] = [self.base_url + annual_links[0]]
        for url in link_obj['file_urls']:
            filename = get_filename(url)
            yield scrapy.Request(url=url, callback=self.save_file,meta={'filename': filename})

    def save_file(self, response):
        """
        Saves the file content to the local filesystem.

            Args:
                response (scrapy.http.Response): The HTTP response object containing the file content.

            Creates:
                - The directory 'input_dataset' if it does not exist.
                - Saves the file to the specified directory with the filename provided in metadata.
        """
        filename = response.meta['filename']
        directory = 'input_dataset'
        file_path = os.path.join(directory, f'{filename}.pdf')

        if not os.path.exists(directory):
            os.makedirs(directory)
            self.log(f"Directory {directory} created.")

        with open(file_path, 'wb') as f:
            f.write(response.body)
        self.log(f"Saved file {file_path}")
