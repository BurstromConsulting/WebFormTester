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


class TestClassWebform(unittest.TestCase):
    websiteList = ["http://www.github.com"]
    repoList = ["https://github.com/BurstromConsulting/WebFormTester"]
    web_drivers = {}
    websiteName = "GitHub"
    delay = 2  # Seconds
    keyword = "webform"
    username = ""
    searchList = {"keyword": keyword, "username": username}
    # Browser dictionary for future use of making it more dynamical in regards of how many browsers we're testing
    # In this case We're testing Chrome, Edge, Firefox but we're not using the dict for anything currently.
    browserList = {}

    @pytest.mark.xdist_group(name="chrome")
    def test_1chrome(self):
        self.init_browser("chrome")
        self.run_test(self.web_drivers["chrome"])
        self.web_drivers["chrome"].close()

    @pytest.mark.xdist_group(name="firefox")
    def test_2firefox(self):
        self.init_browser("firefox")
        self.run_test(self.web_drivers["firefox"])
        self.web_drivers["firefox"].close()

    @pytest.mark.xdist_group(name="edge")
    def test_3edge(self):
        self.init_browser("edge")
        self.run_test(self.web_drivers["edge"])
        self.web_drivers["edge"].close()

    # Initiates each browser called in our test
    def init_browser(self, browsername):
        if browsername in self.browserList.keys():
            func = self.browserList.get(browsername)
            driver = func()
            self.update_web_drivers(browsername, driver)

    # the list of test functions I'm asking each browser function to run.
    def run_test(self, driver):
        self.website_found(driver)
        self.repo_found(driver)
        self.check_issues(driver)

    def update_web_drivers(self, keyword, driver):
        self.web_drivers.update({keyword: driver})

    # Looks for a specific repository on GitHubs website, the repositories found are the
    def repo_found(self, driver):
        repo_page = page.MainPage(driver)
        repo_page.search_text_element = self.searchList.get("keyword")
        repo_page.go_search()
        try:
            pageLoad = WebDriverWait(driver, self.delay).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.codesearch-results')))
            # "Page is ready!"
        except TimeoutException:
            print("Page loading took too much time!")
        search_results_page = page.SearchResultsPage(driver)
        # Verifies that the results page is not empty
        assert search_results_page.is_results_found(), "No results found."
        links = search_results_page.find_link(self.searchList.get("keyword"))
        assert len(links) != 0, "No Matches to Keyword"
        search_results_page.click_link(links, self.searchList.get("keyword"), self.searchList.get("username"))

    # Checks each issue in our Issues Tab for the driver that calls the function.
    def check_issues(self, driver):
        driver.get(self.repoList[0])
        repository_page = page.RepositoryPage(driver)
        repository_page.select_tab("Issues", driver)
        repository_page.click_issue("Closed")

    # One of the tests we're running, this confirms we've ended up on the website we were expecting.
    # This is to confirm things such as, still having a connection, not having a time-out etc... When loading a page.
    def website_found(self, driver):
        main_page = page.MainPage(driver)
        assert main_page.is_title_matches(self.websiteName), "Website not Found"

    # When test is called creates each website for each node we're running in our test
    def setUp(self):
        self.browserList = {
            "chrome": self.chromeWebpageSetup,
            "edge": self.edgeWebpageSetup,
            "firefox": self.firefoxWebpageSetup
        }

    def edgeWebpageSetup(self):
        edge_driver = webdriver.Edge(EdgeChromiumDriverManager().install())
        edge_driver.get(self.websiteList[0])
        return edge_driver

    def firefoxWebpageSetup(self):
        fox_driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        fox_driver.get(self.websiteList[0])
        return fox_driver

    def chromeWebpageSetup(self):
        chrome_driver = webdriver.Chrome(ChromeDriverManager().install())
        chrome_driver.get(self.websiteList[0])
        return chrome_driver

    def tearDown(self):
        print("Done")
        # for driver in self.web_drivers:
        #     self.web_drivers[driver].close()


if __name__ == '__main__':
    unittest.main()
