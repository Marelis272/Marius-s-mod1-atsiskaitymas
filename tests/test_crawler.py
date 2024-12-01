import os
import unittest
from unittest.mock import patch, Mock
from marius_s_mod1_atsiskaitymas.crawler import crawling, crawl

class TestCrawler(unittest.TestCase):

    @patch('requests.get')
    def test_crawling_lrytas_success(self, mock_get):
        # Mock the HTML to simulate lrytas.lt with one article
        mock_html = """
            <html>
                <h2 class="text-base font-medium text-black-custom"><a>Article 1</a></h2>
                <div class="rounded-[4px]"><a><img src="image1.jpg"></a></div>
            </html>
        """
        mock_get.return_value = Mock(status_code=200, content=mock_html)

        #run the crawling function for lrytas.lt and check the output
        result = crawling(site='lrytas.lt', timeout=5, format='list')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], "Article 1")
        self.assertTrue(result[0][1].endswith("image1.jpg"))

    @patch('requests.get')
    def test_crawling_kaunodiena(self, mock_get):
        # Mock the HTML to simulate lrytas.lt with one article
        mock_html = """
                <html>
                    <a class="articles-list-title">Kaunas News</a>
                    <div class="articles-list-media"><img src="image2.jpg"></div>
                </html>
            """
        mock_get.return_value = Mock(status_code=200, content=mock_html)

        # run the crawling function for kaunodiena.lt and check the output
        result = crawling(site='kaunodiena.lt', timeout=5, format='list')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], "Kaunas News")
        self.assertTrue(result[0][1].endswith("image2.jpg"))

    def test_crawling_invalid_site(self):
        #unsupported site that results in an error
        with self.assertRaises(ValueError):
            crawling(site='unsupportedsite.com')

    @patch('requests.get')
    def test_data_return_list(self, mock_get):
        # Mock the HTML to simulate with valid articles
        mock_html = """
            <html>
                <h2 class="text-base font-medium text-black-custom"><a>Article 1</a></h2>
                <div class="rounded-[4px]"><a><img src="image1.jpg"></a></div>
            </html>
        """
        mock_get.return_value = Mock(status_code=200, content=mock_html)

        # Test for lrytas.lt
        result = crawling(site='lrytas.lt', timeout=5, format='list')
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], "Article 1")
        self.assertTrue(result[0][1].endswith("image1.jpg"))

        # Test for kaunodiena.lt
        mock_html_kaunas = """
            <html>
                <a class="articles-list-title">Kaunas News</a>
                <div class="articles-list-media"><img src="image2.jpg"></div>
            </html>
        """
        mock_get.return_value = Mock(status_code=200, content=mock_html_kaunas)
        result = crawling(site='kaunodiena.lt', timeout=5, format='list')
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], "Kaunas News")
        self.assertTrue(result[0][1].endswith("image2.jpg"))


    def test_data_return_csv(self):
        #simulate crawling for kaunodiena and check for csv creation
        site = "kaunodiena.lt"
        csv_file_name = "articles.csv"

        if os.path.isfile(csv_file_name):
            os.remove(csv_file_name)

        crawling(site=site, timeout=5, format='csv')

        self.assertTrue(os.path.isfile(csv_file_name), "CSV file was not created")

        if os.path.isfile(csv_file_name):
            os.remove(csv_file_name)

    @patch('marius_s_mod1_atsiskaitymas.crawler.crawling')
    def test_crawl_function(self, mock_crawling):
        # Mock the output of the crawling function
        mock_crawling.return_value = [("Article 1", "image1.jpg")]

        with patch("sys.argv", ["main.py", "lrytas.lt", "5", "list"]):
            crawl()
            mock_crawling.assert_called_once_with(site="lrytas.lt", timeout=5, format="list")

    def test_wrong_site(self):
        #testing if wrong website URL is chosen
        site = "https://camelia.lt/"
        with self.assertRaises(ValueError):
            crawling(site=site, timeout=5, format='list')

    def test_title_processing(self):
        #test for str title
        title = "Example title"
        article_title = title.strip() if isinstance(title, str) else None
        self.assertEqual(article_title, "Example title")

        #test for invalid type title
        title = 123
        article_title = title.strip() if isinstance(title, str) else None
        self.assertIsNone(article_title)

    def test_image_processing(self):
        #test for str image
        image = "example image url"
        image_url = image
        self.assertEqual(image_url, "example image url")

        #test for invalid type image
        img = 185
        image_url = img if isinstance(img, str) else None
        self.assertIsNone(image_url)

if __name__ == '__main__':
    unittest.main()