import json
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from common import Common
import matplotlib.pyplot as plt

#Opening all the data we might need


def Draw(StatsName, text1, text2, text3):
    #this code draws an image
    W = 700 #width (pixels)
    H = 500 #height (pixels)
    textsize = 50   
    img = Image.new('RGB', (W, H), color = (73, 109, 137)) #background colour
    font = ImageFont.truetype("arial.ttf", textsize)       #creating two fonts
    font2 = ImageFont.truetype("arial.ttf", int(textsize *1.8))
    d = ImageDraw.Draw(img)
    w, h = d.textsize(text1, font=font2) #top line
    d.multiline_text(((W-w)/2,((H-h)/2) - textsize -20), text1, font=font2, fill=(255, 127, 14, 1))
    w, h = d.textsize(text2, font=font) #middle line
    d.multiline_text(((W-w)/2,(H-h)/2), text2, font=font, fill=(255, 255, 255))
    w, h = d.textsize(text3, font=font) #bottom line
    d.multiline_text(((W-w)/2,(((H-h)/2) + textsize)+7), text3, font=font, fill=(255, 255, 255))
    #saving it to file
    x = "Stats\\" + StatsName
    x = str(x)
    img.save(x + ".png")
    img.close()

class Personal():
    def __init__(self):
        self.ratings = None
        self.ratingtimes = None
        self.connections = None
        self.atcsessions = None
        self.flightplans = None
    
    def __updatedata__(self, user, CID):
        self.ratings, self.ratingtimes, self.connections, self.atcsessions, self.flightplans = user.getall()
        

    def controllingflyingtimes(self):
        #pie chart for flying vs time spent controlling
        labels = ["Pilot","ATC"]
        sizes = [self.ratingtimes["pilot"],self.ratingtimes["atc"]]

        if self.ratingtimes["pilot"] > 0 and self.ratingtimes["atc"] > 0:
            fig1, ax1 = plt.subplots()
            ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)

            plt.title('Time spent controlling/flying')
            fig1.set_facecolor("grey")
            plt.savefig(fname = "Stats/controllingflyingtimes.png")
            plt.close()
        if self.ratingtimes["pilot"] > 0 and self.ratingtimes["atc"] == 0:
            text1 = str(self.ratingtimes["pilot"])
            text2 = ("hours have been spent by this")
            text3 = ("user flying on VATSIM")
            Draw("controllingflyingtimes", text1, text2, text3)            
        if self.ratingtimes["pilot"] == 0 and self.ratingtimes["atc"] > 0:
            text1 = str(self.ratingtimes["atc"])
            text2 = ("hours have been spent by this")
            text3 = ("user controlling on VATSIM")
            Draw("controllingflyingtimes", text1, text2, text3)     
        if self.ratingtimes["pilot"] == 0 and self.ratingtimes["atc"] == 0:
            text1 = ""
            text2 = ("This user has spent no time")
            text3 = ("on the VATSIM Network")
            Draw("controllingflyingtimes", text1, text2, text3)
            
    def ratingtimings(self):
        usefulratings = [self.ratingtimes["s1"],self.ratingtimes["s2"],self.ratingtimes["s3"],
                 self.ratingtimes["c1"],self.ratingtimes["c2"],self.ratingtimes["c3"],
                 self.ratingtimes["i1"],self.ratingtimes["i2"],self.ratingtimes["i3"],
                 self.ratingtimes["sup"],self.ratingtimes["adm"]]
        labels = ["s1","s2","s3","c1","c2","c3","i1","i2","i3","sup","adm"]
        #here we remove ratings for which the user has no time on
        while True:
            try:
                index = usefulratings.index(0.0)
                usefulratings.pop(index)
                labels.pop(index)
            except:
                break
        sizes = usefulratings
        #useful ratings is a list of ratings the user has time on
        if len(usefulratings) > 1:    
            #if the length is greater than 1 we make a pie chart
            fig1, ax1 = plt.subplots()
            ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)

            plt.title('Time spent on each rating')
            fig1.set_facecolor("grey")
            plt.savefig(fname = "Stats/ratingtimings.png")
            plt.close()
        else:
            #if the length is just 1 we can make a message
            if len(usefulratings) == 1:
                text1 = str(self.ratingtimes["id"])
                text2 = ("you have spent " + str(sizes[0]))
                text3 = ("hours on the " + str(labels[0]) + " rating.")
                Draw("ratingtimings", text1, text2, text3)
            else:
           #if the length is 0 then we can make a different message
                text1 = "Currently"
                text2 = ("you have no ATC ratings. Sign")
                text3 = ("up for training to change that!")
                Draw("ratingtimings", text1, text2, text3)
                
    def mostusedcallsign(self):
        callsigns = []
        #gets list of all callsigns used
        for x in self.connections["results"]:
            callsigns.append(x["callsign"])
        #finds most used callsign and how many times it was used
        most_callsign = max(set(callsigns), key = callsigns.count)
        number = (callsigns.count(most_callsign))
        text1 = most_callsign
        text2 = "is your most used callsign"
        text3 = "with " + str(number) + " connections."
        Draw("mostusedcallsign", text1, text2, text3)
        
    def mostusedaircraft(self):
        aircraft = []
        #gets list of all aircraft used
        for x in self.flightplans["results"]:
            aircraft.append(x["aircraft"])
        #finds most used aircraft and how many times it was used    
        most_aircraft = max(set(aircraft), key = aircraft.count)
        number = (aircraft.count(most_aircraft))
        text1 = most_aircraft[:4]
        text2 = "is your most used aircraft"
        text3 = "with " + str(number) + " connections."
        Draw("mostusedaircraft", text1, text2, text3)

    def highestfiled(self):
        highest = 0
        #goes through all altitudes filed by the user
        for x in self.flightplans["results"]:
            #iterates through to find the highest altited
            if int(x["altitude"]) > int(highest):
                highest = x["altitude"]

        text1 = highest
        text2 = "is your highest filed altitude."
        text3 = ""
        Draw("highestfiled", text1, text2, text3)
                



if __name__ == "__main__":
    Personal.highestfiled()

