# united_explore.py - crawling components for looking at united prices

# Selenium stuff
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# Regular stuff
import pickle
import time
import random

# Local stuff
from flightlib import *

def united_form_oneway(browser, flight):
    """
    fill the form of one way flight
    some of the elements in the form are located but not used because they may be useful in the future 
    """

    oneWayTrip = browser.find_element_by_id("ctl00_ContentInfo_Booking1_rdoSearchType2")
    oneWayTrip.click()
    #roundTrip = browser.find_element_by_id("ctl00_ContentInfo_Booking1_rdoSearchType1")
    #roundTrip.click()

    depart = browser.find_element_by_id("ctl00_ContentInfo_Booking1_Origin_txtOrigin")
    destination = browser.find_element_by_id("ctl00_ContentInfo_Booking1_Destination_txtDestination")
    depart.clear()
    destination.clear()
    depart.send_keys(flight.depart_airport)
    destination.send_keys(flight.arrive_airport)

    #searchNearby = browser.find_element_by_id("ctl00_ContentInfo_Booking1_Nearbyair_chkFltOpt")
    #lowFare =  browser.find_element_by_id("ctl00_ContentInfo_Booking1_AltDate_chkFltOpt")
    #searchNearby.click()
    #searchNearby.click()
    #lowFare.click()
    #lowFare.click()

    specialDate = browser.find_element_by_id("ctl00_ContentInfo_Booking1_DepDateTime_rdoDateSpecific")
    #flexible = browser.find_element_by_id("ctl00_ContentInfo_Booking1_DepDateTime_rdoDateFlex")
    #flexible.click()
    specialDate.click()

    departDate = browser.find_element_by_id("ctl00_ContentInfo_Booking1_DepDateTime_Depdate_txtDptDate")
    departDate.clear()
    #departTime = browser.find_element_by_id("ctl00_ContentInfo_Booking1_DepDateTime_Deptime_cboDptTime")
    departDate.send_keys(flight.depart_date)

    #returnDate = browser.find_element_by_id("ctl00_ContentInfo_Booking1_RetDateTime_Retdate_txtRetDate")
    #returnTime = browser.find_element_by_id("ctl00_ContentInfo_Booking1_RetDateTime_Rettime_cboDptTime")
    #returnDate.send_keys("06/20/2013")

    #cabin = browser.find_element_by_id("ctl00_ContentInfo_Booking1_Cabins_cboCabin")

    #searchByPrice = browser.find_element_by_id("ctl00_ContentInfo_Booking1_SearchBy_rdosearchby1")
    #searchBySchedule = browser.find_element_by_id("ctl00_ContentInfo_Booking1_SearchBy_rdosearchby2")
    #searchByAward = browser.find_element_by_id("ctl00_ContentInfo_Booking1_SearchBy_rdosearchby3")
    #searchByAward.click()
    #searchBySchedule.click()
    #searchByPrice.click()

    #nonstop =  browser.find_element_by_id("ctl00_ContentInfo_Booking1_Direct_chkFltOpt")
    #nonstop.click()

    submit = browser.find_element_by_id("ctl00_ContentInfo_Booking1_btnSearchFlight")
    submit.click()

    #wait up to 20 second for page to load
    #otherwise move back and try again
    waiting = 20
    while waiting > 0:
        time.sleep(1)
        if "United Airlines - Flight Search Results" in browser.title:
            break
        waiting = waiting - 1
    if waiting <= 0:
        browser.back()
        united_form_oneway(browser, flight)



def united_form_round(browser, flight1, flight2):
    """
    fill the form of round trip flights
    """

    roundTrip = browser.find_element_by_id("ctl00_ContentInfo_Booking1_rdoSearchType1")
    roundTrip.click()

    depart = browser.find_element_by_id("ctl00_ContentInfo_Booking1_Origin_txtOrigin")
    destination = browser.find_element_by_id("ctl00_ContentInfo_Booking1_Destination_txtDestination")
    depart.clear()
    destination.clear()
    depart.send_keys(flight1.depart_airport)
    destination.send_keys(flight2.depart_airport)

    specialDate = browser.find_element_by_id("ctl00_ContentInfo_Booking1_DepDateTime_rdoDateSpecific")
    specialDate.click()

    departDate = browser.find_element_by_id("ctl00_ContentInfo_Booking1_DepDateTime_Depdate_txtDptDate")
    departDate.clear()
    departDate.send_keys(flight1.depart_date)

    returnDate = browser.find_element_by_id("ctl00_ContentInfo_Booking1_RetDateTime_Retdate_txtRetDate")
    returnDate.clear()
    returnDate.send_keys(flight2.depart_date)

    #nonstop =  browser.find_element_by_id("ctl00_ContentInfo_Booking1_Direct_chkFltOpt")
    #nonstop.click()

    submit = browser.find_element_by_id("ctl00_ContentInfo_Booking1_btnSearchFlight")
    submit.click()

    #wait up to 20 second for page to load
    #otherwise move back and try again
    waiting = 20
    while waiting > 0:
        time.sleep(1)
        if "United Airlines - Flight Search Results" in browser.title:
            break
        waiting = waiting - 1
    if waiting <= 0:
        browser.back()
        united_form_round(browser, flight1, flight2)


def get_flight_oneway(browser, navigation_path, flight_id, database, explore_or_search = "search"):
    """
    get one way flights info from the page
    """
    navigation_path.append(str(browser.current_url))
    flight = FlightInfo()
    flight.navigation_path = navigation_path
    flight.oneway_or_round = "oneway"
    flight.explore_or_search = explore_or_search
    flight.flight_id = flight_id
    
    num = 1
    while True:
        query = "//tbody[@id='revenueSegments']/tr[" + str(num) + "]"
        num = num + 1
        try:
            flight_query = browser.find_element_by_xpath(query)
        except NoSuchElementException:
            break
        if "NonStop" in flight_query.get_attribute("id"):
            continue
        elif "FlightsWithStops" in flight_query.get_attribute("id"):
            break
        else:
            price = browser.find_element_by_xpath(query + "//td[@class='tdPrice']//span[@class='fResultsPrice']")
            depart_time = browser.find_element_by_xpath(query + "//td[@class='tdDepart']//strong[@class='timeDepart']")
            depart_date = browser.find_element_by_xpath(query + "//td[@class='tdDepart']/div[3]/b")
            depart_airport = browser.find_element_by_xpath(query + "//td[@class='tdDepart']/div[4]")
            arrive_time = browser.find_element_by_xpath(query + "//td[@class='tdArrive']//strong[@class='timeArrive']")
            arrive_date = browser.find_element_by_xpath(query + "//td[@class='tdArrive']/div[3]/b")
            arrive_airport = browser.find_element_by_xpath(query + "//td[@class='tdArrive']/div[4]")
            flight_number = browser.find_element_by_xpath(query + "//td[@class='tdSegmentDtl']/div[1]/b")
            
            flight.price= price.text
            flight.depart_time = depart_time.text
            flight.depart_date = date_transform(depart_date.text)
            flight.depart_airport = depart_airport.text
            flight.arrive_time = arrive_time.text
            flight.arrive_date = date_transform(arrive_date.text)
            flight.arrive_airport = arrive_airport.text
            flight.flight_number = flight_number.text

            print flight
            database.insert(flight)
    return flight


def get_flight_round(browser, navigation_path, flight_id, database, explore_or_search = "search"):
    """
    get round trip flights info from the page
    """
    navigation_path.append(str(browser.current_url))
    flight1 = FlightInfo()
    flight1.navigation_path = navigation_path
    flight1.oneway_or_round = "round_depart"
    flight1.explore_or_search = explore_or_search
    flight1.flight_id = flight_id
    
    num = 1
    while True:
        query = "//tbody[@id='revenueSegments']/tr[" + str(num) + "]"
        num = num + 1
        try:
            flight_query = browser.find_element_by_xpath(query)
        except NoSuchElementException:
            break
        if "NonStop" in flight_query.get_attribute("id"):
            continue
        elif "FlightsWithStops" in flight_query.get_attribute("id"):
            break
        else:
            price = browser.find_element_by_xpath(query + "//td[@class='tdPrice']//span[@class='fResultsPrice']")
            depart_time = browser.find_element_by_xpath(query + "//td[@class='tdDepart']//strong[@class='timeDepart']")
            depart_date = browser.find_element_by_xpath(query + "//td[@class='tdDepart']/div[3]/b")
            depart_airport = browser.find_element_by_xpath(query + "//td[@class='tdDepart']/div[4]")
            arrive_time = browser.find_element_by_xpath(query + "//td[@class='tdArrive']//strong[@class='timeArrive']")
            arrive_date = browser.find_element_by_xpath(query + "//td[@class='tdArrive']/div[3]/b")
            arrive_airport = browser.find_element_by_xpath(query + "//td[@class='tdArrive']/div[4]")
            flight_number = browser.find_element_by_xpath(query + "//td[@class='tdSegmentDtl']/div[1]/b")
            
            flight1.price= price.text
            flight1.depart_time = depart_time.text
            flight1.depart_date = date_transform(depart_date.text)
            flight1.depart_airport = depart_airport.text
            flight1.arrive_time = arrive_time.text
            flight1.arrive_date = date_transform(arrive_date.text)
            flight1.arrive_airport = arrive_airport.text
            flight1.flight_number = flight_number.text

            print flight1
            database.insert(flight1)

    #get to returning flight page
    select = browser.find_element_by_id("ctl00_ContentInfo_Results_ShowSegments1_ShowSegment_ctl00_selectbutton")
    select.click()
    waiting = 20
    while True:
        time.sleep(1)
        if "United Airlines - Flight Search Results" in browser.title:
            break
        waiting = waiting - 1
        if waiting <= 0:
            browser.back()
            select = browser.find_element_by_id("ctl00_ContentInfo_Results_ShowSegments1_ShowSegment_ctl00_selectbutton")
            select.click()
            waiting = 20

    navigation_path.append(str(browser.current_url))
    flight2 = FlightInfo()
    flight2.navigation_path = navigation_path
    flight2.oneway_or_round = "round_return"
    flight2.explore_or_search = explore_or_search
    flight2.flight_id = flight_id

    num = 1
    while True:
        query = "//tbody[@id='revenueSegments']/tr[" + str(num) + "]"
        num = num + 1
        try:
            flight_query = browser.find_element_by_xpath(query)
        except NoSuchElementException:
            break
        if "NonStop" in flight_query.get_attribute("id"):
            continue
        elif "FlightsWithStops" in flight_query.get_attribute("id"):
            break
        else:
            price = browser.find_element_by_xpath(query + "//td[@class='tdPrice']//span[@class='fResultsPrice']")
            depart_time = browser.find_element_by_xpath(query + "//td[@class='tdDepart']//strong[@class='timeDepart']")
            depart_date = browser.find_element_by_xpath(query + "//td[@class='tdDepart']/div[3]/b")
            depart_airport = browser.find_element_by_xpath(query + "//td[@class='tdDepart']/div[4]")
            arrive_time = browser.find_element_by_xpath(query + "//td[@class='tdArrive']//strong[@class='timeArrive']")
            arrive_date = browser.find_element_by_xpath(query + "//td[@class='tdArrive']/div[3]/b")
            arrive_airport = browser.find_element_by_xpath(query + "//td[@class='tdArrive']/div[4]")
            flight_number = browser.find_element_by_xpath(query + "//td[@class='tdSegmentDtl']/div[1]/b")
            
            flight2.price= price.text
            flight2.depart_time = depart_time.text
            flight2.depart_date = date_transform(depart_date.text)
            flight2.depart_airport = depart_airport.text
            flight2.arrive_time = arrive_time.text
            flight2.arrive_date = date_transform(arrive_date.text)
            flight2.arrive_airport = arrive_airport.text
            flight2.flight_number = flight_number.text

            print flight2
            database.insert(flight2)
    return (flight1, flight2)



def date_transform(date):
    """
    trasnfer the date to the format used by the search form
    """
    new_date = date[6:]
    month = ""
    if "Jan" in new_date:
        month = "01"
    elif "Feb" in new_date:
        month = "02"
    elif "Mar" in new_date:
        month = "03"
    elif "Apr" in new_date:
        month = "04"
    elif "May" in new_date:
        month = "05"
    elif "Jun" in new_date:
        month = "06"
    elif "Jul" in new_date:
        month = "07"
    elif "Aug" in new_date:
        month = "08"
    elif "Sep" in new_date:
        month = "09"
    elif "Oct" in new_date:
        month = "10"
    elif "Nov" in new_date:
        month = "11"
    elif "Dec" in new_date:
        month = "12"
    else:
        raise Exception('date_transform', 'undefined month')
    new_date = new_date[5:]
    year = new_date[-4:]
    new_date = new_date[:-6]
    if len(new_date) == 1:
        new_date = "0" + new_date
    new_date = month + "/" + new_date + "/" + year
    return new_date


def compare_deals(database, flight_id):
    
    browser1 = webdriver.Firefox()
    browser1.get("http://www.united.com")
    assert "United Airlines" in browser1.title
    navigation_path = ["http://www.united.com"]

    #get to deals page
    deals = browser1.find_element_by_xpath("//li[@id='navDeals']/a")
    deals.click()
    while True:
        #wait for full page load
        time.sleep(1)
        if "United Airlines - Travel Deals" in browser1.title:
            break
    navigation_path.append(str(browser1.current_url))

    #get to specials page
    speicals = browser1.find_element_by_xpath("//div[@id='ctl00_ContentInfo_On5192012']/div[@class='half1']/h3[1]/a")
    speicals.click()
    while True:
        time.sleep(1)
        if "United Airlines - United Specials" in browser1.title:
            break
    navigation_path.append(str(browser1.current_url))

    xpath1 = "//div[@id='ctl00_ContentInfo_trSpecials']/table[@class='specials1']/tbody/tr[" + str(flight_id) + "]/td[@style='width:7%;background:#ffc']/a"
    link = browser1.find_element_by_xpath(xpath1)
    link.click()
    while True:
        time.sleep(1)
        if "United Airlines - Flight Fare Calendar Results" in browser1.title:
            break
    navigation_path.append(str(browser1.current_url))

    lowest_flight = browser1.find_element_by_xpath("//table[@id='calendarFare']/tbody/tr/td[1]/table[@class='Calendar']/tbody//td[@class='on lowest']/div[@class='fare']/a")
    lowest_flight.click()
    while True:
        time.sleep(1)
        if "United Airlines - Flight Search Results" in browser1.title:
            break
    navigation_path.append(str(browser1.current_url))
    
    flight1, flight2 = get_flight_round(browser1, navigation_path, flight_id, database, "explore")

    home = browser1.find_element_by_id("ctl00_CustomerHeader_logoHome")
    home.click()
    navigation_path.append(str(browser1.current_url))
    while True:
        time.sleep(1)
        if "Airline Tickets" in browser1.title:
            break
    united_form_round(browser1, flight1, flight2)
    get_flight_round(browser1, navigation_path, flight_id, database, "search")

    home = browser1.find_element_by_id("ctl00_CustomerHeader_logoHome")
    home.click()
    navigation_path.append(str(browser1.current_url))
    while True:
        time.sleep(1)
        if "Airline Tickets" in browser1.title:
            break
    united_form_oneway(browser1, flight1)
    get_flight_oneway(browser1, navigation_path, flight_id, database, "search")

    home = browser1.find_element_by_id("ctl00_CustomerHeader_logoHome")
    home.click()
    navigation_path.append(str(browser1.current_url))
    while True:
        time.sleep(1)
        if "Airline Tickets" in browser1.title:
            break
    united_form_oneway(browser1, flight2)
    get_flight_oneway(browser1, navigation_path, flight_id, database, "search")

    browser1.close()
    time.sleep(2)

    #direct search
    browser2 = webdriver.Firefox()
    browser2.get("http://www.united.com")
    assert "United Airlines" in browser2.title
    navigation_path = ["http://www.united.com"]

    united_form_round(browser2, flight1, flight2)
    get_flight_round(browser2, navigation_path, flight_id, database, "search")
    browser2.close()
    time.sleep(2)

    browser3 = webdriver.Firefox()
    browser3.get("http://www.united.com")
    assert "United Airlines" in browser3.title
    navigation_path = ["http://www.united.com"]

    united_form_oneway(browser3, flight1)
    get_flight_oneway(browser3, navigation_path, flight_id, database, "search")
    browser3.close()
    time.sleep(2)

    browser4 = webdriver.Firefox()
    browser4.get("http://www.united.com")
    assert "United Airlines" in browser4.title
    navigation_path = ["http://www.united.com"]

    united_form_oneway(browser4, flight2)
    get_flight_oneway(browser4, navigation_path, flight_id, database, "search")
    browser4.close()
    
    
    
    

def explore_deals(database):
    """Explores the United deals page, picks a flight, checks the price for the
    resulting pages. A first step in general site exploration"""

    browser = webdriver.Firefox()
    browser.get("http://www.united.com")
    assert "United Airlines" in browser.title

    #get to deals page
    deals = browser.find_element_by_xpath("//li[@id='navDeals']/a")
    deals.click()
    while True:
        #wait for full page load
        time.sleep(1)
        if "United Airlines - Travel Deals" in browser.title:
            break

    #get to specials page
    speicals = browser.find_element_by_xpath("//div[@id='ctl00_ContentInfo_On5192012']/div[@class='half1']/h3[1]/a")
    speicals.click()
    while True:
        time.sleep(1)
        if "United Airlines - United Specials" in browser.title:
            break

    #loop through the deals
    num = 1
    while True:
        num = num + 1
        xpath1 = "//div[@id='ctl00_ContentInfo_trSpecials']/table[@class='specials1']/tbody/tr[" + str(num) + "]/td[@style='width:7%;background:#ffc']/a"
        xpath2 = "//div[@id='ctl00_ContentInfo_trSpecials']/table[@class='specials1']/tbody/tr[" + str(num) + "]/td[@style='width:7%;background:#ffc']/small"
        try:
            link = browser.find_element_by_xpath(xpath1)
            #print link.text
            #link.click()
            #while True:
            #    time.sleep(1)
            #    if "United Airlines - Flight Fare Calendar Results" in browser.title:
            #        break
                
        except NoSuchElementException:
            try:
                soldout = browser.find_element_by_xpath(xpath2)
                print soldout.text
                continue
            except NoSuchElementException:
                break
            
        #lowest_flight = browser.find_element_by_xpath("//table[@id='calendarFare']/tbody/tr/td[1]/table[@class='Calendar']/tbody//td[@class='on lowest']/div[@class='fare']/a")
        #lowest_flight.click()
        #while True:
        #    time.sleep(1)
        #    if "United Airlines - Flight Search Results" in browser.title:
        #        break
        try:    
            compare_deals(database, num)
        except Exception:
            continue

        #browser.back()
        #browser.back()
        #while True:
        #    time.sleep(1)
        #    if "United Airlines - United Specials" in browser.title:
        #        break
        
    
            
    #browser.close()



if __name__ == "__main__":


    database = FlightDB("united_db.db", "search_and_deals")
    explore_deals(database)
    database.closeDB()
    

























    

    
