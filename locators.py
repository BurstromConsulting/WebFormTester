from selenium.webdriver.common.by import By


class MainPageLocators(object):
    """A class for main page locators. All main page locators should come here"""

    SEARCH_FIELD = (By.NAME, 'q')


class SearchResultsPageLocators(object):
    """A class for search results locators. All search results locators should
    come here"""
    LANGUAGE_FILTER_LIST = (By.XPATH, '//ul[@class=filter-list small]')
    NAV_MENU_FILTER_LIST = (By.XPATH, '//nav[@class=menu border d-none d-md-block]')
    SEARCH_RESULTS_LIST = (By.CSS_SELECTOR, 'div.codesearch-results')

class IssuesPageLocators(object):

    ISSUES_LIST = (By.CSS_SELECTOR, '.js-navigation-container a[id^=issue_]')