# united_random_explore.py - crawling randomly for looking at united prices

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

    
def get_all_links_on_page(browser):
    links = browser.find_elements_by_tag_name("a")
    return links

def random_explore(browser, navigation_path, step):
    navigation_path.append(browser.current_url)
    if not browser.current_url.startswith("http://www.united.com/"):
        browser.get("http://www.united.com/")
        navigation_path.append(browser.current_url)
        time.sleep(0.2)
        assert "United Airlines" in browser.title
    elif step < 0:
        return
        
    while True:
        try:
            links = get_all_links_on_page(browser)
            rand = random.randint(0, len(links) - 1)
            next_link = links[rand]
            url = str(next_link.get_attribute("href"))
        except Exception:
            continue
        if url.startswith("http://www.united.com/"):
            try:
                next_link.click()
                break
            except Exception:
                pass
    random_explore(browser, navigation_path, step - 1)

def explore(database):

    cities = ["Chicago, IL (ORD - O'Hare)", "New York, NY (NYC - All Airports)", "Los Angeles, CA (LAX-All Airports)", "Houston, TX (IAH - Intercontinental)",
              "San Francisco, CA (SFO)", "Washington, DC (WAS - All Airports)", "Philadelphia, PA (PHL)", "Phoenix, AZ (PHX)", "Boston, MA (BOS)",
              "Austin, TX (AUS)", "Miami, FL (MIA - All Airports)", "San Diego, CA (SAN)", "Seattle, WA (SEA)"]
    dates = ["6/14/2013", "6/15/2013", "6/16/2013", "6/18/2013", "6/22/2013",
             "6/25/2013", "6/30/2013", "7/10/2013", "7/20/2013", "7/30/2013"]
    num = 0
    for date in dates:
        for depart_city in cities:
            for arrive_city in cities:
                if arrive_city == depart_city:
                    continue
                browser1 = webdriver.Firefox()
                browser1.get("http://www.united.com/")
                waiting = 10
                while True:
                    time.sleep(1)
                    if "Airline Tickets" in browser1.title:
                        break
                    waiting = waiting - 1
                    if waiting <= 0:
                        browser2.get("http://www.united.com/")
                        waiting = 10
                navigation_path = ["http://www.united.com/"]
                num = num + 1
                flight = FlightInfo(depart_city, date, "0:00", arrive_city, date, "0:00",
                                    "oneway", num, "UA0000", "$0", navigation_path, "search", "")
                united_form_oneway(browser1, flight)
                get_flight_oneway(browser1, navigation_path, num, database, "search")
                browser1.close()

                browser2 = webdriver.Firefox()
                browser2.get("http://www.united.com/")
                navigation_path = ["http://www.united.com/"]
                random_explore(browser2, navigation_path, 5)
                browser2.get("http://www.united.com/")
                waiting = 10
                while True:
                    time.sleep(1)
                    if "Airline Tickets" in browser2.title:
                        break
                    waiting = waiting - 1
                    if waiting <= 0:
                        browser2.get("http://www.united.com/")
                        waiting = 10
                united_form_oneway(browser2, flight)
                get_flight_oneway(browser2, navigation_path, num, database, "search_after_random_explore")
                browser2.close()




    


if __name__ == "__main__":


    database = FlightDB("united_db.db", "search_and_random")
    explore(database)
    database.closeDB()
    

























    

    
