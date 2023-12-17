import json
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from common import Common
from datafetch import Datafetch
from datafetch import APIData

    
def Draw(StatsName, text1, text2, text3):
    W = 700
    H = 500
    textsize = 50
    img = Image.new('RGB', (W, H), color = (73, 109, 137))
    font = ImageFont.truetype("arial.ttf", textsize)       
    font2 = ImageFont.truetype("arial.ttf", int(textsize * 1.8))
    d = ImageDraw.Draw(img)
    w, h = d.textsize(text1, font=font2)
    d.multiline_text(((W-w)/2,((H-h)/2) - textsize -20), text1, font=font2, fill=(255, 127, 14, 1))
    w, h = d.textsize(text2, font=font)
    d.multiline_text(((W-w)/2,(H-h)/2), text2, font=font, fill=(255, 255, 255))
    w, h = d.textsize(text3, font=font)
    d.multiline_text(((W-w)/2,(((H-h)/2) + textsize)+7), text3, font=font, fill=(255, 255, 255))
    x = "Stats\\" + StatsName
    x = str(x)
    img.save(x + ".png")
    img.close()

        
class Stats:
    def __init__(self, MyData):
        self.data = MyData.getdata()
            
    def __updatedata__(self, MyData):
        self.data = MyData.getdata()
        
    def ATIS(self):

        for p in self.data["controllers"]:
            #checks facilitytype is terminal control
            facilitytype = p["facility"]
            if facilitytype == 2 or facilitytype == 3 or facilitytype == 4 or facilitytype == 5:
                comp = p["callsign"]
                possible = comp
                comp = comp[:4]
                if comp[3] == "_": #Reformats American callsigns
                    comp = comp[:3]
                    comp = "K" + comp 
                ATIS = False
                for x in self.data["atis"]: #goes through all ATIS's currently up
                    comp2 = x["callsign"]
                    comp2 = comp2[:4] #shorten to 4 letter airport ICAO code
                    if comp2 == comp: #compares location of controller to location of ATIS
                        ATIS = True #There is an ATIS where the controller is
                if ATIS == False:
                    text1 = str(comp)
                    text2 = ("does not have their ATIS up.")
                    text3 = ("Tut tut tut.")
                    break
        try:
            Draw("ATIS", text1, text2, text3)
        except:
                text1 = ("All controllers")
                text2 = ("have their ATIS up.")
                text3 = ("Yay!")
    def controllers(self):
        controllers = 0
        for p in self.data["controllers"]:
            controllers = controllers + 1
        controllers = str(controllers)
        text1 = (controllers)
        text2 = ("of VATSIM's finest controllers")
        text3 = ("are online.")
        Draw("controllers", text1, text2, text3) 

    def pilots(self):
        pilots = 0
        for p in self.data["pilots"]:
            pilots = pilots + 1
        pilots = str(pilots)
        text1 = (pilots)
        text2 = ("pilots are currently")
        text3 = ("experiencing the joys of flight.")
        Draw("pilots", text1, text2, text3)
        
    def mostdepartures(self):
        airport_deps = []
        for x in range(len(self.data["pilots"])):
            try:
                temp = (self.data["pilots"][x]["flight_plan"]["departure"])
                airport_deps.append(temp)
            except:
                None
                  
        #finding max
                
        most_deps = max(set(airport_deps), key = airport_deps.count)
        number = (airport_deps.count(most_deps))
        text1 = most_deps
        text2 = "has the most outbound traffic"
        text3 = "with " + str(number) + " departures."
        Draw("mostdepartures", text1, text2, text3)

    def mostarrivals(self):
        airport_arrs = []
        for x in range(len(self.data["pilots"])):
            try:
                temp = (self.data["pilots"][x]["flight_plan"]["arrival"])
                airport_arrs.append(temp)
            except:
                None
        #finding max
                
        most_arrs = max(set(airport_arrs), key = airport_arrs.count)
        number = (airport_arrs.count(most_arrs))
        text1 = most_arrs
        text2 = "has the most inbound traffic"
        text3 = "with " + str(number) + " arrivals."
        Draw("mostarrivals", text1, text2, text3)
        
    def busiestairport(self):
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
        #finding max
                
        most = max(set(airport), key = airport.count)
        number = (airport.count(most))
        text1 = most
        text2 = "has the most overall traffic"
        text3 = "with " + str(number) + " movements."
        Draw("busiestairport", text1, text2, text3)
        
    def busiestroute(self):
        airport = []
        for x in range(len(self.data["pilots"])):
            try:
                temp1 = (self.data["pilots"][x]["flight_plan"]["arrival"])           
                temp2 = (self.data["pilots"][x]["flight_plan"]["departure"])
                temp3 = temp1 + "-" + temp2
                airport.append(temp3)
                        
            except:
                None
        #finding max
        print(airport)
        most = max(set(airport), key = airport.count)
        number = (airport.count(most))
        text1 = most
        text2 = "is the busiest route"
        text3 = "with " + str(number) + " flights."
        Draw("busiestroute", text1, text2, text3)
        
    def highestaltitude(self):
        highest = 0
        for x in range(len(self.data["pilots"])):
                temp = (self.data["pilots"][x]["altitude"])
                if temp > highest:
                    highest = temp
                    callsign = self.data["pilots"][x]["callsign"]
                    

        text1 = str(callsign)
        text2 = "has the highest altitude"
        text3 = "on VATSIM at " + str(highest) + " feet."
        Draw("highestaltitude", text1, text2, text3)
        
    def fastestspeed(self):
        highest = 0
        for x in range(len(self.data["pilots"])):
                temp = (self.data["pilots"][x]["groundspeed"])
                if temp > highest:
                    highest = temp
                    callsign = self.data["pilots"][x]["callsign"]
                    



        text1 = str(callsign)
        text2 = "has the fastest groundspeed"
        text3 = "on VATSIM at " + str(highest) + " knots."
        Draw("fastestspeed", text1, text2, text3)
        
    def pilotlongesttime(self):
        highest = 0
        time = (self.data["pilots"][0]["logon_time"])
        callsign = (self.data["pilots"][0]["callsign"])
        time = time[:19]
        time = Common.secondssince(time)
        time = time/60
        time = int(time)
        time = str(time)
        text1 = str(callsign)
        text2 = "has been on the network"
        text3 =  time + " minutes."
        Draw("pilotlongesttime", text1, text2, text3)
        
    def atclongesttime(self):
        highest = 0
        time = (self.data["controllers"][0]["logon_time"])
        callsign = (self.data["controllers"][0]["callsign"])
        time = time[:19]
        time = Common.secondssince(time)
        time = time/60
        time = int(time)
        time = str(time)
        text1 = str(callsign)
        text2 = "has been on the network"
        text3 =  time + " minutes."
        Draw("atclongesttime", text1, text2, text3) 

if __name__ == "__main__":
    MyData = Datafetch()
    MyStats = Stats(MyData)
    MyStats.atclongesttime()


                
        
            
