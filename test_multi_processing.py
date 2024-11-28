import logging
import os
import unittest
from bs4 import BeautifulSoup
from multiprocessing import Queue
from multi_processing import *

class TestWebScraper(unittest.TestCase):

    @classmethod

    def setUpClass(cls):
        """

        configurations before running the tests.

        """

        create_timestamped_logfile()

        logging.getLogger().disabled = True

    def test_create_timestamped_logfile(self):
        """

        Test log file creation with a timestamped name.

        """

        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")

        files = os.listdir()

        log_files = [f for f in files if f.startswith(f"web_scraper_{timestamp.split('_')[0]}")]

        self.assertGreater(len(log_files), 0, "No log file created.")

    def test_fetch_https_links(self):
        """

        Test the extraction of HTTPS links from HTML.

        """

        html = '''

        <a href="https://example.com">Link 1</a>

        <a href="http://example.com">Non-HTTPS</a>

        <a href="https://test.com">Link 2</a>

        '''

        soup = BeautifulSoup(html, "html.parser")

        links = fetch_https_links(soup)

        self.assertEqual(links, ["https://example.com", "https://test.com"])

    def test_fetch_title(self):
        """

        Test the extraction of a webpage's title.

        """

        html = '<html><head><title>Test Title</title></head></html>'

        soup = BeautifulSoup(html, "html.parser")

        self.assertEqual(fetch_title(soup), "Test Title")

        html_no_title = "<html><head></head><body></body></html>"

        soup_no_title = BeautifulSoup(html_no_title, "html.parser")

        self.assertEqual(fetch_title(soup_no_title), "No Title Found")

    def test_fetch_meta_description(self):
        """

        Test the extraction of a meta description.

        """

        html = '<meta name="description" content="Test Description">'

        soup = BeautifulSoup(html, "html.parser")

        self.assertEqual(fetch_meta_description(soup), "Test Description")

        html_no_meta = "<html><head></head><body></body></html>"

        soup_no_meta = BeautifulSoup(html_no_meta, "html.parser")

        self.assertEqual(fetch_meta_description(soup_no_meta), "No Meta Description Found")

    def test_count_paragraphs(self):
        """

        Test the counting of <p> tags in a webpage.

        """
        html = "<p>Para 1</p><p>Para 2</p><p>Para 3</p>"
        soup = BeautifulSoup(html, "html.parser")
        self.assertEqual(count_paragraphs(soup), 3)

        html_no_paragraphs = "<html><head></head><body></body></html>"

        soup_no_paragraphs = BeautifulSoup(html_no_paragraphs, "html.parser")

        self.assertEqual(count_paragraphs(soup_no_paragraphs), 0)

    def test_fetch_site_info(self):
        """

        Test the fetching of website information.

        """

        queue = Queue()

        test_url = "https://www.example.com"

        fetch_site_info(test_url, queue)

        site_info = queue.get()

        self.assertIn("url", site_info)

        self.assertEqual(site_info["url"], test_url)

        self.assertTrue("title" in site_info or "error" in site_info)



    def test_save_to_csv(self):
        """

        Test saving data to a CSV file.

        """
        queue = Queue()

        queue.put({

            "url": "https://example.com",

            "title": "Example Title",

            "meta_description": "Example Meta Description",

            "num_paragraphs": 5,

            "num_links": 2,

            "links": ["https://link1.com", "https://link2.com"],

        })

        queue.put({"url": "https://error.com", "error": "Timeout Error"})



        output_file = "test_output.csv"

        save_to_csv(queue, output_file)

        self.assertTrue(os.path.exists(output_file))



        with open(output_file, "r", encoding="utf-8") as file:

            lines = file.readlines()

            self.assertGreater(len(lines), 1)  # Ensure header and at least one row



        os.remove(output_file)  # Cleanup



    @classmethod

    def tearDownClass(cls):
        """

        Clean up resources after tests have completed.

        """

        log_files = [f for f in os.listdir() if f.startswith("web_scraper_") and f.endswith(".log")]

        for log_file in log_files:

            os.remove(log_file)  # Remove generated log files after testing





if __name__ == "__main__":

    unittest.main()







