# Playing with selenium

import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from selenium import webdriver

def browse(page):
    
    driver = webdriver.Firefox()
    driver.get(page)
    source = driver.page_source
    
    time.sleep(50)

    driver.quit()

if __name__ == "__main__":
    browse(sys.argv[1])

