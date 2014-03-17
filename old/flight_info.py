from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import urllib2
import random
import sys




class flight_info:
    def __init__(self,source_airport,destination_airport,start_date,start_time,arrival_date,arrival_time,flight_number): 
        self.source_airport=source_airport
        self.destination_airport=destination_airport
        self.start_date=start_date
        self.start_time=start_time
        self.arrival_date=arrival_date
        self.arrival_time=arrival_time
        self.flight_number=flight_number

    def __str__(self):
        return "source sirport:%s ,dest_airport=%s, start_date=%s ,start_time =%s ,arrival_date=%s ,arrival_time=%s ,flight_number=%s " %(self.source_airport,self.destination_airport,self.start_date,self.start_time,self.arrival_date,self.arrival_time,self.flight_number)


    def __eq__(self,other):
        if(isinstance(other,flight_info)):
            return ((self.source_airport==other.source_airport) and (self.destination_airport==other.destination_airport) and (self.start_date==other.start_date) and (self.start_time==other.start_time) and (self.arrival_date == other.arrival_date) and (self.arrival_time==other.arrival_time) and (self.flight_number==other.flight_number))


def compare_prices(list1,list2):
    if list1[3]==list2[3]:
        if list1[2]==list2[2]:
            print "Same prices %d, %d" %(list1[2],list2[2])
        else:
            print "Same flight dfferent prices %d %d" %(list1[2],list2[2])
    else:
        print "Different flight"

def explore():
    browser=webdriver.Firefox()
    browser.get("http://www.united.com")
    browser.get("http://www.usairways.com/en-US/specials/default.html")








if(__name__=="__main__"):
 #   obj=flight_info("San Fancisco","Chicago","12 March 2013","12.00 am","13 March 2013","14.00 pm","APRE5678")    
  #  list1=[]
  #  a=2
   # list1.append(a)
   #b="wer"
   # list1.append(b)
   # c=2.0
   # list1.append(c)
   # list1.append(obj)
   # list2=[]
   # list2.append(3)
   # list2.append("wed")
   # list2.append(3.0)
   # obj=flight_info("San Fancisco","Chicago","12 March 2013","12.00 am","13 March 2013","14.00 pm","APRE5678")
   # list2.append(obj)
   # compare_prices(list1,list2)
#for temp in list1:
 #   print temp
    explore()
