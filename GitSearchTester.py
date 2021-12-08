import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


class GitSearchTester(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def test_search_github_landing_page(self):
        driver = self.driver
        driver.get("https://github.com/")
        self.assertIn("GitHub", driver.title)
        searchfield = driver.find_element_by_name("q")
        searchfield.send_keys("pycon")
        searchfield.send_keys(Keys.RETURN)
        assert "No results found." not in driver.page_source

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
