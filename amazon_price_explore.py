from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.keys import Keys
import time
import random


result = []

def main():
    browser = webdriver.Firefox()
    browser.get("http://www.amazon.com/")
    assert "Amazon.com" in browser.title

    explore_pages(browser, 0)
    
    print_result()
    
    browser.close()

def print_result():
    global result
    num = 0
    for product in result:
        print(num)
        print(product)
        num = num + 1

def get_all_links_on_page(browser):
    links = browser.find_elements_by_tag_name("a")
    return links

def is_product_page(browser):
    try:
        elem =  browser.find_element_by_xpath("/html/body")
    except NoSuchElementException:
        return False
    if elem.get_attribute("class") == "dp":
        print("got one product")
        return True
    else:
        return False

def add_result(browser):
    this_page = []
    try:
        url = browser.current_url
        this_page.append(url)
    except NoSuchElementException:
        pass
    try:
        name = browser.find_element_by_xpath("//span[@id='btAsinTitle']").text
        this_page.append(name)
    except NoSuchElementException:
        pass
    try:
        price = browser.find_element_by_xpath("//span[@id='actualPriceValue']/b").text
        this_page.append(price)
    except NoSuchElementException:
        pass
    global result
    result.append(this_page)

def explore_pages(browser, step):
    if not browser.current_url.startswith("http://www.amazon.com"):
        browser.get("http://www.amazon.com/")
        time.sleep(0.2)
        assert "Amazon.com" in browser.title
    elif is_product_page(browser):
        add_result(browser)
    elif step >= 20:
        return
    
    links = get_all_links_on_page(browser)
    if len(links) < 10:
        browser.get("http://www.amazon.com/")
        time.sleep(0.2)
        assert "Amazon.com" in browser.title
        links = get_all_links_on_page(browser)
        
    while True:
        rand = random.randint(0, len(links) - 1)
        next_link = links[rand]
        url = str(next_link.get_attribute("href"))
        if url.startswith("http://www.amazon.com/"):
            try:
                next_link.click()
                break
            except Exception:
                pass
    explore_pages(browser, step + 1)

if __name__ == "__main__":
    main()
