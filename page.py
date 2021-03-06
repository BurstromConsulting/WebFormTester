from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from element import BasePageElement
from locators import MainPageLocators, SearchResultsPageLocators, IssuesPageLocators
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time


class SearchTextElement(BasePageElement):
    """This class gets the search text from the specified locator"""
    # The locator for search box where search string is entered
    def __init__(self, val='q'):
        self.locator = val


class BasePage(object):
    """Base class to initialize the base page that will be called from all
    pages"""

    def __init__(self, driver):
        self.driver = driver


class MainPage(BasePage):
    """Home page action methods come here. I.e. GitHub.com"""

    # Declares a variable that will contain the retrieved text
    search_text_element = SearchTextElement()

    def is_title_matches(self, title):
        """Verifies that the hardcoded text "GitHub" appears in page title"""

        return title in self.driver.title

    def go_search(self):
        """Triggers the search"""

        element = self.driver.find_element(*MainPageLocators.SEARCH_FIELD)
        element.send_keys(Keys.RETURN)


class SearchResultsPage(BasePage):
    """Search results page action methods come here"""

    def is_results_found(self):
        # Probably should search for this text in the specific page
        # element, but as for now it works fine
        return "We couldn’t find any repositories" not in self.driver.page_source

    def find_link(self, keyword):
        # Search the div ending in "codesearch-results" for the link matching our criteria.
        links = []
        for link in self.driver.find_elements_by_css_selector('.v-align-middle'):
            text = link.get_attribute('href')
            if text is not None:
                if keyword.casefold() in link.text.casefold():
                    links.append(link)
        return links

    def click_link(self, link_list, keyword, username=""):
        # Clicks the first match according to our Keyword and Username that we've specified in our search.

        for link in link_list:
            if keyword in link.text.casefold() and username in link.text.casefold():
                link.click()
                return
        return


class RepositoryPage(MainPage):
    search_text_element = SearchTextElement()

    def select_tab(self, tab, driver):
        # Method meant for the purpose of selecting the various types of Tabs in a Repository, e.g Issues
        # Currently only checks for the Issues tab.
        try:
            load = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="issues-tab"]')))
            # print("Page is ready!")
        except TimeoutException:
            print("Page loading took too much time!")
        currentpage = driver.find_element(By.XPATH, '//*[@id="issues-tab"]')
        if tab in currentpage.text:
            currentpage.click()

    def click_issue(self, state):

        wait = WebDriverWait(self.driver, 10)
        issuesList = []
        issuesPage = wait.until(EC.visibility_of_element_located((By.ID, 'js-issues-search')))
        issuesPage.clear()
        issuesPage.send_keys("is:issue")
        issuesPage.send_keys(Keys.RETURN)
        issuesPage = wait.until(EC.visibility_of_element_located((By.ID, 'js-issues-search')))
        time.sleep(2)
        issues = self.driver.find_elements(*IssuesPageLocators.ISSUES_LIST)
        length = len(issues)
        for i in range(length):
            issues = self.driver.find_elements(*IssuesPageLocators.ISSUES_LIST)
            issues[i].click()
            status = wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.gh-header-meta span[class^=State]')))
            status = self.driver.find_element(By.CSS_SELECTOR, '.gh-header-meta span[class^=State]')
            if status.text in state:
                issuesList.append(issues[i])
                self.driver.execute_script("window.history.go(-1)")
            else:
                self.driver.execute_script("window.history.go(-1)")
