from selenium import webdriver

browser = webdriver.Chrome()

# Edith has heard about a great comics site and decides to
# check out its Home Page
browser.get('http://localhost:8000')

# She notices the page title and header mention comics
assert 'Comics' in browser.title

# She sees some comics on the home page

browser.quit()