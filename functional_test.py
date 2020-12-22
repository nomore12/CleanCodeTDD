from selenium import webdriver
from selenium.webdriver.chrome.options import Options


browser = webdriver.Chrome("./chromedriver")
browser.get("http://localhost:8000")

print(browser.title)

assert "Django" in browser.title
