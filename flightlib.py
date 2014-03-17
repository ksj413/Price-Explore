# flightlib.py
#
# Holds generic flight info classes and functions. Also home to data storage
# functions and the like.

import pickle
import time
import sqlite3

class FlightInfo(object):
    """ The generic FlightInfo class used to save information about specific
    flights that are collected."""
    
    def __init__(self, depart_airport = "", depart_date = "", depart_time = "",
                 arrive_airport = "", arrive_date = "", arrive_time = "",
                 oneway_or_round = "", flight_id = -1, flight_number = "", price = "0", 
                 navigation_path = [], explore_or_search = "explore", others = ""):
        self.depart_airport = depart_airport
        self.depart_date = depart_date
        self.depart_time = depart_time
        self.arrive_airport = arrive_airport
        self.arrive_date = arrive_date
        self.arrive_time = arrive_time
        #oneway_or_round = "oneway"/"round_depart"/"round_return"
        self.oneway_or_round = oneway_or_round
        #Since there  is only combined price for round trip, use flight id to link the departing and returning flight round trip
        #flight id is the index of the flight in the United special table
        #It is to locate a bunch of queries in the database that are related
        #Flights with the same flight id have the same departing/arriving airports, departing date, but are different in oneway/round trip/navigation path/...
        self.flight_id = flight_id
        self.flight_number = flight_number
        self.navigation_path = navigation_path
        self.price = price
        #explore_or_search = "explore"/"search"/"search after explore"/...
        self.explore_or_search = explore_or_search
        #the experiment time
        self.time = int(time.time())
        #other discriptions
        self.others = others

    def __str__(self):
        return """depart: %s %s %s\narrive: %s %s %s\none way or round trip: %s\nflight id: %s\nflight number: %s\nprice: %s
path: %s\nexperiment time: %s\nexplore_or_search: %s\nother discriptions: %s\n"""\
               % (self.depart_airport, self.depart_date, self.depart_time,
                  self.arrive_airport, self.arrive_date, self.arrive_time,
                  self.oneway_or_round, self.flight_id, self.flight_number, self.price,
                  self.navigation_path, self.time, self.explore_or_search, self.others)

    def __eq__(self, other):
        if(isinstance(other,flight_info)):
            return ((self.depart_airport == other.depart_airport) \
                    and (self.depart_date == other.depart_date) \
                    and (self.depart_time == other.depart_time) \
                    and (self.arrive_airport == other.arrive_airport) \
                    and (self.arrive_date == other.arrive_date) \
                    and (self.arrive_time == other.arrive_time) \
                    and (self.flight_number == other.flight_number))

    def dump_to_file(self, file_name):
        f = open(file_name, "a")
        pickle.dump(self, f)
        f.close()


class FlightDB():
    """
    The database class for storing flight infomation
    """
    def __init__(self, file_name, table_name):
        self.conn = sqlite3.connect(file_name)
        self.cursor = self.conn.cursor()
        # Create table
        self.file_name = file_name
        self.table_name = table_name
        self.cursor.execute("CREATE TABLE '%s' (depart_airport text, depart_date text, depart_time text, "
                            "arrive_airport text, arrive_date text, arrive_time text, "
                            "oneway_or_round text, flight_id integer, flight_number text, price text, "
                            "navigation_path text, experiment_time integer, explore_or_search text, others text)" % table_name)

    def insert(self, flight):
        row = (flight.depart_airport, flight.depart_date, flight.depart_time,
               flight.arrive_airport, flight.arrive_date, flight.arrive_time,
               flight.oneway_or_round, flight.flight_id, flight.flight_number, flight.price,
               str(flight.navigation_path), flight.time, flight.explore_or_search, flight.others)
        self.cursor.execute("INSERT INTO " + self.table_name + " VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", row)
        self.conn.commit()

    def closeDB(self):
        self.conn.commit()
        self.conn.close()


#testing code
if __name__ == "__main__":
    a = FlightInfo("a1", "a2", "a3", "b1", "b2", "b3", "oneway", 2, "UA1234", "$100", [1,2,3], "explore", "hello")
    #print a
    flight1 = FlightInfo("Chicago, IL (CHI - All Airports)", "6/26/2013", "a3", "Houston, TX (IAH - Intercontinental)", "b2", "b3",
                         "round_depart", 1, "UA4321", "$100", [1,2,3], "expolre")
    flight2 = FlightInfo("Houston, TX (IAH - Intercontinental)", "6/30/2013", "b3", "Chicago, IL (CHI - All Airports)", "6/26/2013", "a3",
                         "round_return", 1, "UA4312", "$100", [1,2,3], "expolre")

    b = FlightDB("united_db.db", "test5")
    b.insert(a)
    b.insert(flight1)
    b.insert(flight2)
    b.closeDB()





        




        
