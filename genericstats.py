import json
from common import Common
from datafetch import Datafetch
from datafetch import APIData

class GenericStats:
    def __init__(self, MyData):
        self.data = MyData.getdata()
        
    def __updatedata__(self, MyData):
        self.data = MyData.getdata()


    def generalstats(self, ICAO):
        flights = self.departures(ICAO)
        departurenum = len(flights)
        arrivals = self.arrivals(ICAO)
        arrivalnum = len(arrivals)
        for x in arrivals:
            flights.append(x)
        flightsnum = len(flights)
        callsigns = []

        flightsnum = "Total Flights: " + str(flightsnum)
        departurenum = "Number of Departures: " + str(departurenum)
        arrivalnum = "Number of Arrivals: " + str(arrivalnum)

        
        for x in flights:
            shortsign = str(x[0])[0:3]
            callsigns.append(shortsign)
            
        if len(callsigns) > 0:
            mostcommonairline = max(set(callsigns), key=callsigns.count)
            mostcommonairline = "Most Common Airline: " + str(mostcommonairline)
        else:
            mostcommonairline = "Most Common Airline: None"
            
        aircrafts = []
        for x in flights:
           aircrafts.append(str(x[2]))
        if len(aircrafts) > 0:
            maxaircrafts = max(set(aircrafts), key=aircrafts.count)
            maxaircrafts = "Most Common Aircraft: " + str(maxaircrafts)
        else:
            maxaircrafts = "Most Common Aircraft: None"
            
        return flightsnum, departurenum, arrivalnum, mostcommonairline, maxaircrafts 

    def departures(self, ICAO):
        flights = []
        for x in range(len(self.data["pilots"])):
            try:
                temp = (self.data["pilots"][x]["flight_plan"]["departure"])    
                if temp == ICAO:
                    flights.append(self.data["pilots"][x])
            except:
                None
                
        #for x in flights:
            #print(x["cid"])             
        departuresdisplay = []
        for x in flights:
            temp = []
            temp.append(x["callsign"])
            temp.append(x["flight_plan"]["arrival"])
            temp.append(x["flight_plan"]["aircraft_short"])
            temp.append(x["flight_plan"]["deptime"])            
            departuresdisplay.append(temp)
        flights = departuresdisplay
        return flights

    def arrivals(self, ICAO):
        flights = []
        for x in range(len(self.data["pilots"])):
            try:
                temp = (self.data["pilots"][x]["flight_plan"]["arrival"])    
                if temp == ICAO:
                    flights.append(self.data["pilots"][x])
            except:
                None
                
        arrivalsdisplay = []
        for x in flights:
            temp = []
            temp.append(x["callsign"])
            temp.append(x["flight_plan"]["departure"])
            temp.append(x["flight_plan"]["aircraft_short"])
            temp.append(x["flight_plan"]["deptime"])
            arrivalsdisplay.append(temp)
        flights = arrivalsdisplay
       
        return flights

    def aircraftstats(self, callsign):
        for x in range(len(self.data["pilots"])):
            if str(self.data["pilots"][x]["callsign"]) == callsign:
                          
                CID = "CID: " + str(self.data["pilots"][x]["cid"])
                name = "Name: "  + str(self.data["pilots"][x]["name"])
                aero = name[-4:]
                if not aero == aero.upper():
                    aero = "No Home Airport"
                else:
                    name = name[:-4]
                aero = "Home airport: " + str(aero)
                callsign = "Callsign: "+ self.data["pilots"][x]["callsign"]
                server = "Server: " + str(self.data["pilots"][x]["server"])
                pilotrating = "Pilot Rating: " + str(self.data["pilots"][x]["pilot_rating"])
                latitude = "Latitude: " + str(self.data["pilots"][x]["latitude"])
                longitude = "Longitude: " + str(self.data["pilots"][x]["longitude"])
                altitude = "Altitude: " + str(self.data["pilots"][x]["altitude"]) + "ft"
                groundspeed = "Groundspeed: " + str(self.data["pilots"][x]["groundspeed"]) + "kt"
                transponder = "Squawk: " + str(self.data["pilots"][x]["transponder"])
                heading = "Heading: " + str(self.data["pilots"][x]["heading"])      
                qnh_mb = "QNH: " + str(self.data["pilots"][x]["qnh_mb"])
                       
                return CID, name, aero, callsign, server, pilotrating, latitude, longitude, altitude, groundspeed, transponder, heading, qnh_mb 
    def flightplanstats(self, callsign):
        for x in range(len(self.data["pilots"])):
            if str(self.data["pilots"][x]["callsign"]) == callsign:
                try:
                    
                    flighttype = "Type of Flight: " + str(self.data["pilots"][x]["flight_plan"]["flight_rules"]) 
                    aircraft = "Aircraft: " + str(self.data["pilots"][x]["flight_plan"]["aircraft_short"])
                    departure = "Departure: " + str(self.data["pilots"][x]["flight_plan"]["departure"])
                    arrival = "Arrival: " + str(self.data["pilots"][x]["flight_plan"]["arrival"])
                    cruisespeed = "Cruise Speed: " + str(self.data["pilots"][x]["flight_plan"]["cruise_tas"]) + "kt"
                    altitude = self.data["pilots"][x]["flight_plan"]["altitude"]
                    if len(altitude) == 3:
                        altitude = altitude + "00"
                    altitude = "Cruise: " + str(altitude) + "ft"
                    deptime = "Departure Time: " + str(self.data["pilots"][x]["flight_plan"]["deptime"]) + "z"
                    enroute_time = "Enroute Time: " + str(self.data["pilots"][x]["flight_plan"]["enroute_time"]) + "z"
                    fuel_time = "Fuel Time: " + str(self.data["pilots"][x]["flight_plan"]["fuel_time"]) + "z"
                    route = str(self.data["pilots"][x]["flight_plan"]["route"])
                    remarks = str(self.data["pilots"][x]["flight_plan"]["remarks"])
                except:
                    flighttype = "No flightplan submitted"
                    aircraft = ""
                    departure = ""
                    arrival = ""
                    cruisespeed = ""
                    altitude = ""
                    deptime = ""
                    enroute_time = ""
                    fuel_time = ""
                    route = "Empty"
                    remarks = "Empty"                   
                
                return flighttype, aircraft, altitude, departure, arrival, cruisespeed, deptime, enroute_time, fuel_time, route, remarks
            
    def validatecallsign(self, callsign):
        for x in range(len(self.data["pilots"])):
            if str(self.data["pilots"][x]["callsign"]) == callsign:
                return True
        return False
    
    def airportslist(self):
        
        def stats(ICAO):
            
            deps = self.departures(ICAO)
            deps = len(deps)
            arrs = self.arrivals(ICAO)
            arrs = len(arrs)
            
            movements = deps + arrs
            return  deps, arrs, movements
        
        airports = []
        ICAOlist = []
        for x in range(len(self.data["pilots"])):
            try:
                temp = (self.data["pilots"][x]["flight_plan"]["arrival"])
                if temp not in ICAOlist:
                    ICAOlist.append(temp)

                    information = []
                    information.append(temp)
                    statistics = stats(temp)
                    for stat in statistics:
                        information.append(stat)
                    airports.append(information)
            except:
                None
            try:
                temp = (self.data["pilots"][x]["flight_plan"]["departure"])
                if temp not in ICAOlist:
                    ICAOlist.append(temp)

                    information = []
                    information.append(temp)
                    statistics = stats(temp)
                    for stat in statistics:
                        information.append(stat)
                    airports.append(information)
            except:
                None
                
        airports = sorted(airports, key=lambda x: x[3], reverse=True)
        
        return airports
    
    def aircraftlist(self):
        aircrafts = []
        for x in range(len(self.data["pilots"])):
                information = []

                temp = self.data["pilots"][x]["callsign"]
                information.append(temp)
                try:
                    temp = (self.data["pilots"][x]["flight_plan"]["departure"])
                    information.append(temp)   
                    temp = (self.data["pilots"][x]["flight_plan"]["arrival"])
                    information.append(temp)   
                    temp = (self.data["pilots"][x]["flight_plan"]["aircraft_short"])
                    information.append(temp)
                    aircraft.append(information)
                except:
                    None
                aircrafts.append(information)
        aircrafts = sorted(aircrafts)
            
        return aircrafts
        
if __name__ == "__main__":
    MyData = Datafetch()
    MyGenericStats = GenericStats(MyData)
    print(MyGenericStats.departures("EGCC"))
            
