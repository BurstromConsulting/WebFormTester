import unittest
import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import page


def edgeWebpageSetup():
    edge_driver = webdriver.Edge(EdgeChromiumDriverManager().install())
    return edge_driver


def firefoxWebpageSetup():
    fox_driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    return fox_driver


def chromeWebpageSetup():
    chrome_driver = webdriver.Chrome(ChromeDriverManager().install())
    return chrome_driver


class TestClassWebform(unittest.TestCase):
    websiteList = ["http://www.github.com"]
    repoList = ["https://github.com/BurstromConsulting/WebFormTester"]
    web_drivers = {}
    websiteName = "GitHub"
    delay = 2 #seconds
    keyword = "webform"
    username = ""
    # Browser dictionary for future use of making it more dynamical in regards of how many browsers we're testing
    # In this case We're testing Chrome, Edge, Firefox but we're not using the dict for anything currently.
    browserList = {
        "chrome": "chrome_driver",
        "edge": "edge_driver",
        "firefox": "fox_driver"
    }

    # @pytest.fixture
    # def websites(self):
    #     return self.websiteList
    #
    @pytest.mark.xdist_group(name="chrome")
    def test_chrome(self):
        self.run_test(self.web_drivers.get("chrome"))

    @pytest.mark.xdist_group(name="firefox")
    def test_firefox(self):
        self.run_test(self.web_drivers.get("firefox"))

    @pytest.mark.xdist_group(name="edge")
    def test_edge(self):
        self.run_test(self.web_drivers.get("edge"))

    def run_test(self, driver):
        self.website_found(driver)
        self.repo_found(driver)
        self.check_issues(driver)

    def repo_found(self, driver):
        repo_page = page.MainPage(driver)
        repo_page.search_text_element = self.keyword
        repo_page.go_search()
        try:
            pageLoad = WebDriverWait(driver, self.delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.codesearch-results')))
            print("Page is ready!")
        except TimeoutException:
            print("Page loading took too much time!")
        search_results_page = page.SearchResultsPage(driver)
        # Verifies that the results page is not empty
        assert search_results_page.is_results_found(), "No results found."
        links = search_results_page.find_link(self.keyword)
        assert len(links) != 0, "No Matches to Keyword"
        search_results_page.click_link(links, self.keyword, self.username)

    def check_issues(self, driver):
        driver.get(self.repoList[0])
        repository_page = page.RepositoryPage(driver)
        repository_page.select_tab("Issues", driver)
        repository_page.click_issue("Closed")

    def website_found(self, driver):
        main_page = page.MainPage(driver)
        # main_page = page.MainPage(self.web_drivers)
        assert main_page.is_title_matches(self.websiteName), "Website not Found"
        # assert True, "test"

    def setUp(self):
        chrome_driver = chromeWebpageSetup()
        fox_driver = firefoxWebpageSetup()
        edge_driver = edgeWebpageSetup()
        self.web_drivers = {"chrome": chrome_driver, "edge": edge_driver, "firefox": fox_driver}
        for driver in self.web_drivers:
            self.web_drivers[driver].get(self.websiteList[0])
        # self.web_drivers = self.chromeWebpageSetup(self.websiteList[0])

    def tearDown(self):
        for driver in self.web_drivers:
            self.web_drivers[driver].close()


if __name__ == '__main__':
    unittest.main()
