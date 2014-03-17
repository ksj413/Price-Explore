from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time

browser = webdriver.Firefox()
browser.get("http://www.amazon.com/")
assert "Amazon.com" in browser.title

elem = browser.find_element_by_id("twotabsearchtextbox")
elem.send_keys("bike" + Keys.RETURN)
time.sleep(0.2)

link0 = browser.find_element_by_xpath("//div[@id='result_0']/h3[@class='newaps']/a")
link0_addr = link0.get_attribute("href")
price0 = browser.find_element_by_xpath("//div[@id='result_0']/ul[@class='rsltL']/li/a/span")
price0_num = price0.text

print 0, price0_num
#print link0_addr

link1 = browser.find_element_by_xpath("//div[@id='result_1']/h3[@class='newaps']/a")
link1_addr = link1.get_attribute("href")
price1 = browser.find_element_by_xpath("//div[@id='result_1']/ul[@class='rsltL']/li/a/span")
price1_num = price1.text

print 1, price1_num
#print link1_addr

link2 = browser.find_element_by_xpath("//div[@id='result_2']/h3[@class='newaps']/a")
link2_addr = link2.get_attribute("href")
price2 = browser.find_element_by_xpath("//div[@id='result_2']/ul[@class='rsltL']/li/a/span")
price2_num = price2.text

print 2, price2_num
#print link2_addr

#try:
 #   browser.find_element_by_xpath("//a[contains(@href,'http://seleniumhq.org')]")
#except NoSuchElementException:
 #   assert 0, "can't find seleniumhq"
#browser.close()
