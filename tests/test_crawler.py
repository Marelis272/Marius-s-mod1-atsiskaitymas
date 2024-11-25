import unittest
from marius_s_mod1_atsiskaitymas.crawler import crawling

class TestCrawler(unittest.TestCase):
    def test_data_return_type(self):
        #testing if crawling function returns a list
        site = "https://www.lrytas.lt/"
        result = crawling(site=site, timeout=5, format='list')
        self.assertIsInstance(result, list) #result is a list
        if result: # check elements only if list is not empty
            for item in result:
                self.assertIsInstance(item, tuple) #check that each item is a tuple
                self.assertEqual(len(item), 2) #check that each tuple has 2 elements


if __name__ == '__main__':
    unittest.main()