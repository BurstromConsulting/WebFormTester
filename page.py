from element import BasePageElement
from locators import MainPageLocators, SearchResultsPageLocators
from selenium.webdriver.common.keys import Keys


class SearchTextElement(BasePageElement):
    """This class gets the search text from the specified locator"""

    # The locator for search box where search string is entered
    # locator = MainPageLocators.SEARCH_FIELD
    locator = 'q'


class BasePage(object):
    """Base class to initialize the base page that will be called from all
    pages"""

    def __init__(self, driver):
        self.driver = driver


class MainPage(BasePage):
    """Home page action methods come here. I.e. Python.org"""

    # Declares a variable that will contain the retrieved text
    search_text_element = SearchTextElement()

    def is_title_matches(self):
        """Verifies that the hardcoded text "GitHub" appears in page title"""

        return "GitHub" in self.driver.title

    def go_search(self):
        """Triggers the search"""

        element = self.driver.find_element(*MainPageLocators.SEARCH_FIELD)
        element.send_keys(Keys.RETURN)


class SearchResultsPage(BasePage):
    """Search results page action methods come here"""

    def is_results_found(self):
        # Probably should search for this text in the specific page
        # element, but as for now it works fine
        return "No results found." not in self.driver.page_source

    def find_link(self, keyword):
        # Should search the div ending in "codesearch-results" for the link matching our criteria.
        # element = self.driver.find_element(*SearchResultsPageLocators.SEARCH_RESULTS_LIST)
        links = []
        for link in self.driver.find_elements_by_css_selector('.v-align-middle'):
            text = link.get_attribute('href')
            if text is not None:
                if keyword.casefold() in link.text.casefold():
                     # print("True")
                     links.append(link)
        return links

    def click_link(self, link_list, keyword, username=""):
        for link in link_list:
            if keyword in link.text.casefold() and username in link.text.casefold():
                link.click()
                return
        return