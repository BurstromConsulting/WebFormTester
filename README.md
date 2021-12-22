# WebFormTester
Barebones python test suite for searching www.github.com with the idea of finding a repository
that's on your first result page of your GitHub search.

The test *currently* performs 3 different types of checks before finishing:

- Check if website successfully loaded (in this case, https://www.github.com, GitHubs frontpage)
- Search GitHub for repositories matching "Keyword", then check the results if they match your Keyword,
add them to your list of matches and returns your matches.
- Clicks into the first repository that matches your Keyword and Username
- After the Repository has been entered, it will then proceed to open a pre-specified repository
- Upon opening the new Repository it will open the Issues Tab. Search for all issues, check each issue if its matching your search crieria.



From here it's possible to expand upon what it does when it lands on a repository.
But for the moment it just enters the repository you've clicked, then it will go to a specific repository you've predetermined and click the issues tab and search for all issues. click on them one by one until its entered and gone through each issue.
Each issue that matches your criteria, e.g if its status is open, it will then be added to a Issues list, which is currently not being used for anything.
It could be returned and used for future testing.

Possible improvements that could be done:

* Reading website, search args and more from file rather than being defined in the code.
* Adding functionality to the issues tab function to be able to go into more tabs than just issues.
* Return the result of your test(s) to a file rather than in the terminal.
* Making it more versatile in what browsers it tests during each of its tests.


## Setting up your own test
There are a few things you'll need to make sure to have installed:
- Pytest
- Selenium
- Webdriver-Manager(make sure you have the latest version, else there is an issue with testing edge)
- Python v3.10
- pytest-xdist

Running the pytest:
> pytest test_webformtester.py -n=x

> pytest test_webformtester.py::test_chrome

> pytest test_webformtester.py::test_edge

> pytest test_webformtester.py::test_firefox

where in your "-n=x" replace x with the number of threads you'd like to run concurrently. or run the other pytests if youre only interested in testing it for a single browser.

