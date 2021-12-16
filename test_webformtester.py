import unittest
import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import page


class TestClassWebform(unittest.TestCase):
    websiteList = ["http://www.github.com"]
    web_drivers = []
    websiteName = "GitHub"
    keyword = "webform"
    username = ""

    # @pytest.fixture
    # def websites(self):
    #     return self.websiteList
    #
    # def website_names(self):
    #     return self.websiteName

    def test_repoFound(self):
        length = len(self.web_drivers)
        for i in range(length):
            main_page = page.MainPage(self.web_drivers[i])
            main_page.search_text_element = self.keyword
            main_page.go_search()
            search_results_page = page.SearchResultsPage(self.web_drivers[i])
        # Verifies that the results page is not empty
            assert search_results_page.is_results_found(), "No results found."
            links = search_results_page.find_link(self.keyword)
            assert len(links) != 0, "No Matches to Keyword"
            search_results_page.click_link(links, self.keyword, self.username)

    # def test_issues(self):
    #     pass

    def test_Website_found(self):
        length = len(self.web_drivers)
        for i in range(length):
            main_page = page.MainPage(self.web_drivers[i])
        # main_page = page.MainPage(self.web_drivers)
            assert main_page.is_title_matches(self.websiteName), "Website not Found"
        # assert True, "test"

    def chromeWebpageSetup(self, website):
        chrome_driver = webdriver.Chrome(ChromeDriverManager().install())
        chrome_driver.get(website)
        return chrome_driver

    def firefoxWebpageSetup(self, website):
        fox_driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        fox_driver.get(website)
        return fox_driver

    def edgeWebpageSetup(self, website):
        edge_driver = webdriver.Edge(EdgeChromiumDriverManager().install())
        edge_driver.get(website)
        return edge_driver

    def setUp(self):
        chrome_driver = self.chromeWebpageSetup(self.websiteList[0])
        fox_driver = self.firefoxWebpageSetup(self.websiteList[0])
        edge_driver = self.edgeWebpageSetup(self.websiteList[0])
        self.web_drivers = [chrome_driver, fox_driver, edge_driver]
        # self.web_drivers = self.chromeWebpageSetup(self.websiteList[0])

    def tearDown(self):
        length = len(self.web_drivers)
        for i in range(length):
            self.web_drivers[i].close()
            self.web_drivers[i].quit()


if __name__ == '__main__':
    unittest.main()
