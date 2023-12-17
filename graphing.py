import json
import matplotlib.pyplot as plt
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from common import Common
from datafetch import Datafetch
from datafetch import APIData

def getdata():
    global data
    with open('./Data/data.txt', 'r') as json_file:
        data = json.load(json_file)

class Graphing:
    def __init__(self, MyData):
        self.data = MyData.getdata()
        
    def __updatedata__(self, MyData):
        self.data = MyData.getdata()
        
    def planetype(self):
        aircraft_types = []
        #checks to see if aircraft is in array already and adds it if not
        for x in range(len(self.data["pilots"])):
            try:
                    temp = (self.data["pilots"][x]["flight_plan"]["aircraft"])
                    aircraft_types.append(temp)
            except:
                None
                
        #produces ICAO standard aircraft codes
        ICAO_aircraft_types = []
        heavy = 0
        light = 0
        medium = 0
        transport = 0
        counter = []
        no_var_aircraft_types = aircraft_types
        for p in aircraft_types:
            temp = str(p)
            #checking for heavies mediums and transports
            if temp[:2] == "H/":
                heavy = heavy + 1
                temp = temp[2:]
            if temp[:2] == "M/":
                medium = medium + 1
                temp = temp[2:]
            if temp[:2] == "L/":
                light = light + 1
                temp = temp[2:]
            if temp[:2] == "T/":
                transport = transport + 1
                temp = temp[2:]
            #standardises into 4 letter ICAO
            p = temp[:4]
            ICAO_aircraft_types.append(p)

        #gets rid of duplicate aircraft      
        ICAO_aircraft_types_short = list(dict.fromkeys(ICAO_aircraft_types))            
        #counting how many of each type
        ICAO_aircraft_types_weightings = []
        for p in ICAO_aircraft_types_short:
            ICAO_aircraft_types_weightings.append(ICAO_aircraft_types.count(p))
        #so now we have three useful variables the short list, the long list with duplicates and the counts

        #Now there are too many planes to make a useful plot so we're gonna get rid of the ones that are rarely flown otherwise the graph would be too big
        other = 0
        planes_to_plot = []
        p = 0
        cutoff = 20
        while p < len(ICAO_aircraft_types_weightings):
            if ICAO_aircraft_types_weightings[p] < cutoff:
                other = other + 1
                ICAO_aircraft_types_weightings.pop(p)
                ICAO_aircraft_types_short.pop(p)
                p = p -1
            p = p + 1
        ICAO_aircraft_types_short.append("Other")
        ICAO_aircraft_types_weightings.append(other)
        
        #double bubble sort
        Common.doublebubblesort(ICAO_aircraft_types_weightings,ICAO_aircraft_types_short)
        #now we draw the chart here
        
        plt.bar(ICAO_aircraft_types_short, ICAO_aircraft_types_weightings, label="Example two", color='grey',)
        plt.legend().remove()
        plt.xlabel('Aircraft Types (ICAO)')
        plt.ylabel('Number of Planes')
        plt.title('Planes on the VATSIM Network')
        plt.savefig(fname = "Stats/planetype.png")
        plt.close()
               
        #clienttype chart
    def clienttype(self):
        #checks to see if aircraft is in array already and adds it if not
        pilot = (len(self.data["pilots"]))
        atc = (len(self.data["controllers"]))
        #for p in data['clients']:
            #temp = p["clienttype"]
            #if temp == "PILOT":
                #pilot = pilot + 1
            #else:
                #atc = atc + 1

        #draws a pie chart and saves it

        labels = ["ATC's","Pilots"]
        sizes = [atc,pilot]

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.title('Stations on the VATSIM Network')
        fig1.patch.set_facecolor("grey")
        plt.savefig(fname = "Stats/clienttype.png")
        plt.close()

    def flighttype(self):
        #IFR AND VFR
        I = 0
        V = 0
        #parses JSON3
        for x in range(len(self.data["pilots"])):
            try:
                    temp = (self.data["pilots"][x]["flight_plan"]["flight_rules"])
                    if temp == "I":
                        I = I + 1
                    else:
                        V = V + 1
            except:
                None
        #drawing graph
        labels = ["IFR","VFR"]
        sizes = [I,V]
        
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)

        plt.title('Type of Flight')
        fig1.set_facecolor("grey")
        plt.savefig(fname = "Stats/flighttype.png")
        plt.close()

    def busiestairportsbarchart(self):
        airport = []
        for x in range(len(self.data["pilots"])):
            try:
                temp = (self.data["pilots"][x]["flight_plan"]["arrival"])
                airport.append(temp)              
            except:
                None
            try:
                temp = (self.data["pilots"][x]["flight_plan"]["departure"])
                airport.append(temp)              
            except:
                None
        #shortening
        airport_short = list(dict.fromkeys(airport))           
        #counting how many of each type
        airport_weightings = []
        for p in airport_short:
            airport_weightings.append(airport.count(p))
        Common.doublebubblesort(airport_weightings, airport_short)

        #Shortening:
        airport_weightings = airport_weightings[:9]
        airport_short = airport_short[:9]
        #plotting        
        plt.bar(airport_short,airport_weightings,label="Example two", color='grey',)
        plt.legend().remove()
        plt.xlabel('Airports (ICAO)')
        plt.ylabel('Number of Movements')
        plt.title('Busiest Airports By Movements')
        plt.savefig(fname = "Stats/busiestairportsbarchart.png")
        plt.close()
        
    def busiestairportsdeparturesbar(self):
        airport = []
        for x in range(len(self.data["pilots"])):
            try:
                temp = (self.data["pilots"][x]["flight_plan"]["departure"])
                airport.append(temp)              
            except:
                None
        #shortening
        airport_short = list(dict.fromkeys(airport))           
        #counting how many of each type
        airport_weightings = []
        for p in airport_short:
            airport_weightings.append(airport.count(p))
        Common.doublebubblesort(airport_weightings, airport_short)

        #Shortening:
        airport_weightings = airport_weightings[:9]
        airport_short = airport_short[:9]
        #plotting
        plt.bar(airport_short,airport_weightings,label="Example two", color="#ff7f0e")
        plt.legend().remove()
        plt.xlabel('Airports (ICAO)')
        plt.ylabel('Number of Departures')
        plt.title('Busiest Airports')
        plt.savefig(fname = "Stats/busiestairportsdeparturesbar.png")
        plt.close()        

    def busiestairportsarrivalsbar(self):
        airport = []
        for x in range(len(self.data["pilots"])):
            try:
                temp = (self.data["pilots"][x]["flight_plan"]["arrival"])
                airport.append(temp)              
            except:
                None
        #shortening
        airport_short = list(dict.fromkeys(airport))           
        #counting how many of each type
        airport_weightings = []
        for p in airport_short:
            airport_weightings.append(airport.count(p))
        Common.doublebubblesort(airport_weightings, airport_short)

        #Shortening:
        airport_weightings = airport_weightings[:9]
        airport_short = airport_short[:9]
        #plotting        
        plt.bar(airport_short,airport_weightings,label="Example two", color="#496d89")
        plt.legend().remove()
        plt.xlabel('Airports (ICAO)')
        plt.ylabel('Number of Arrivals')
        plt.title('Busiest Airports')
        plt.savefig(fname = "Stats/busiestairportsarrivalsbar.png")
        plt.close()



if __name__ == "__main__":
    MyData = Datafetch()
    MyGraphing = Graphing(MyData)
    MyGraphing.busiestairportsarrivalsbar()

    
            
