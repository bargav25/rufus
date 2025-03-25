import unittest
from rufus import RufusClient

class TestRufusClient(unittest.TestCase):
    def test_scrape_invalid_url(self):
        # This test uses a dummy API key and an invalid URL.
        client = RufusClient(api_key="XXXXXXXXXXXXX")
        results = client.scrape("https://www.boxofficemojo.com/", "Mickey 17 movie collection this sunday")
        self.assertIsInstance(results, list)

if __name__ == '__main__':
    unittest.main()