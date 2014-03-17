from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
browser1 = webdriver.Firefox()
browser1.get("https://www.google.com/settings/u/0/ads?hl=en&sig=ACi0TCiiEncisUVF6z7Vl_d4mOqZKHMD0z_afQMcBKWK9YkWzx32dveG4OMXEHk5GJOrAFllpY7EC9jrZjDJbFRxJjIQOiWhxA")

time.sleep(10)

browser1.find_element_by_xpath("//div[@class='kc']")
print "done"
