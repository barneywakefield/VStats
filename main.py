import urllib.request, json 
import json
import requests
from PIL import ImageTk, Image
from PIL import ImageFont
import os
import tkinter as tk
import tkinter.ttk as ttk 
from ttkthemes import ThemedStyle
import tkinter.font as tkFont
import random
import schedule
import time
#fetchdata (must be first)
from datafetch import Datafetch
from datafetch import APIData

#my imports
from graphing import Graphing
from stating import Stats
from personal import Personal
from common import Common
from genericstats import GenericStats
#f = open("data.txt", "w")
#response = requests.get("http://eu.data.vatsim.net/vatsim-data.json")
#data = response.json()

###############

#######
#MAIN WINDOW

class GUI:
    def __init__(self, window, ThemedStyle):

        def createFolder(directory):
            try:
                if os.path.exists(directory):
                    show = "main"
                if not os.path.exists(directory):
                    os.makedirs(directory)
                    show = "info" 
            except OSError:
                print ('Error: Creating directory. ' +  directory)
                show = "info" 
            return show
        show = "info" 
        show = createFolder('./Stats/')
        # Creates a folder in the current directory called Stats
        #initializing variables    
        self.validCID = False
        self.lastCID = None
        self.user = None
        self.page = None
        self.ICAO = ""
        self.callsign = ""


        #instantiating classes
        self.MyData = Datafetch()
        schedule.every(120).seconds.do(self.MyData.fetchjson3)
        self.MyStats = Stats(self.MyData)
        self.MyGraphing = Graphing(self.MyData)
        self.MyPersonal = Personal()
        self.MyGenericStats = GenericStats(self.MyData)

        #attempts to draw network statistics every 20 seconds
        schedule.every(15).seconds.do(self.networkstatisticsregenerate)
        
        self.window = window
        self.ThemedStyle = ThemedStyle

        style = ThemedStyle(window)
        style.set_theme("scidgrey")

        #configuring the main window
        window.maxsize(1000,700)
        window.configure(background="#464646")
        window.title("Stats")
        window.iconbitmap('icon.ico')
        window.rowconfigure(0, minsize=80, weight=1)
        window.columnconfigure(1, minsize=80, weight=1)

        #two standard fonts I can use        
        self.fontExample = tkFont.Font(family="Arial", size=16)
        self.fontSmall = tkFont.Font(family="Arial", size=10)
        self.greeting = "Hello, and welcome to your wall of stats:"

        #creates sidebar and then mainpage
        self.bar()
        if show == "main":
            self.generateMainpage()
        else:
            self.aboutPage()


    #NETWORKS STATISTICS
    def generateMainpage(self):

        self.page = "network statistics"
        #function to get and resize an image into a suitable size
        def getnewimage(self, mainpage, x, paths):
            path = paths[x]
            path = "Stats/" + path + ".png"
            #formatting images
            image = Image.open(path)
            new_image = image.resize((350, 250))
            return new_image
        x=0
        self.labels = []
        self.mainpage = tk.Frame(self.window) #new frame within the larger one
        #get the paths
        self.paths = (self.callrandomall(4,self.validCID))
        paths = self.paths
        self.mainpage.configure(background="#464646")
        rectangle_1 = tk.Label(self.mainpage, bg="#464646", fg="white", text = self.greeting, font = self.fontExample, pady = 10, )
        rectangle_1.grid(row=0, column=1, sticky="N", columnspan = 3)
        #creates grid
        for i in range(1,3):
            self.mainpage.columnconfigure(i, weight=1, minsize=50)
            self.mainpage.rowconfigure(i, weight=1, minsize=50)
            for j in range(1,3):
                frame = tk.Frame(
                    master=self.mainpage,
                    borderwidth=0,
                    highlightthickness=0
                )
                frame.grid(row=i, column=j, padx=5, pady=5)

                #getting the image
                new_image = getnewimage(self,self.mainpage, x, paths)
                img = ImageTk.PhotoImage((new_image), master = self.window)
                x = x + 1
                #putting the image in
                self.labels.append(tk.Label(master=frame, image = img))
                self.labels[x-1].photo = img
                self.labels[x-1].pack(padx=3, pady=3)
                self.mainpage.grid(row=0, column=1, sticky="nsew")
                
            #functions for double click
        self.labels[0].bind('<Double-Button-1>', self.imagedoubleclick0)
        self.labels[1].bind('<Double-Button-1>', self.imagedoubleclick1)            
        self.labels[2].bind('<Double-Button-1>', self.imagedoubleclick2)
        self.labels[3].bind('<Double-Button-1>', self.imagedoubleclick3)
        
    def imagedoubleclick0(self, event):
        singlepath = self.paths[0]
        self.generateImagepage(singlepath)
    def imagedoubleclick1(self, event):
        singlepath = self.paths[1]
        self.generateImagepage(singlepath)
    def imagedoubleclick2(self, event):
        singlepath = self.paths[2]
        self.generateImagepage(singlepath)
    def imagedoubleclick3(self, event):
        singlepath = self.paths[3]
        self.generateImagepage(singlepath)

    def generateImagepage(self, singlepath):
        #destroys all widgets currently on screen
        for widget in self.mainpage.winfo_children():
            widget.destroy()  
        self.mainpage.destroy()          
        #creates new page
        self.mainpage = tk.Frame(self.window) #new frame within the larger one
        self.mainpage.grid(row=0, column=1)
        self.mainpage.configure(background="#464646")
        self.page = "image page"        
        imageholder = tk.Frame(self.mainpage)
        imageholder.grid(row=0, column = 0, pady = 10, padx = 10)
        imageholder.rowconfigure(0)
        imageholder.columnconfigure(0)
        imageholder.configure(background="white")
        
        singlepath = "Stats/" + singlepath + ".png"

        image = Image.open(singlepath)
        image = image.resize((700, 500), Image.ANTIALIAS) ## The (250, 250) is (height, width)
        te = ImageTk.PhotoImage(image)

        label = tk.Label(imageholder, bg="white", image = te)
        label.photo= te
        label.grid(row=0, column=0, pady = 5, padx = 5)
        
        label.bind('<Double-Button-1>', self.networkstatisticsdouble)
    ###############

    def getfunctionsstats(self):
        #gets stats functions that aren't built in
        stats_list = [func for func in dir(self.MyStats) if callable(getattr(self.MyStats, func)) and not func.startswith("__") ]
        return stats_list
    def getfunctionsgraphs(self):
        #gets graphs functions that aren't built in
        graphs_list = [func for func in dir(Graphing) if callable(getattr(Graphing, func)) and not func.startswith("__")]
        return graphs_list
    def getfunctionspersonal(self):
        #gets graphs functions that aren't built in
        personal_list = [func for func in dir(Personal) if callable(getattr(Personal, func)) and not func.startswith("__")]
        return personal_list

    def callrandomall(self, number, validCID):
        stats_list = self.getfunctionsstats()
        graphs_list = self.getfunctionsgraphs()
            
        if validCID == False:
            available = stats_list + graphs_list
        else:
            personal_list = self.getfunctionspersonal()
            available = stats_list + graphs_list + personal_list
        #reduces list down to length of number passed
        #(randomly selects some functions)
        length_available = len(available)
        randoms = random.sample(range(0, length_available), number)
        functionstocall = []
        for x in randoms:
            adding = str(available[x])
            functionstocall.append(adding)
            
        #update in preperation
        self.MyStats.__updatedata__(self.MyData)
        self.MyGraphing.__updatedata__(self.MyData)
        if self.validCID == True:
            self.MyPersonal.__updatedata__(self.user, self.CID)
            
        #calls the randomly selected functions
        for y in functionstocall:
            if y in stats_list:
                x = "self.MyStats." + y
                eval(x+ "()")
            elif y in graphs_list:
                x = "self.MyGraphing." + y                
                eval(x+ "()")
            else:
                x = "self.MyPersonal." + y
                eval(x+ "()")
        #returns the function it calls        
        return functionstocall

    #####################

    #PERSONAL STATISTICS
    def generateSecondpage(self):
        
        self.page = "personal statistics"
        
        
        if self.validCID == True: #checks if a valid CID has been entered
            self.mainpage = tk.Frame(self.window) #new frame within the larger one
            self.mainpage.configure(background="#464646")
            self.mainpage.grid(row=0, column=1)
            #creates grid
            for i in range(0,1):
                self.mainpage.columnconfigure(i, weight=1, minsize=10)
            for i in range(1,2):    
                self.mainpage.rowconfigure(i, weight=1, minsize=10)
            
            welcome = tk.Label(self.mainpage, bg="#464646", fg="white", 
                               text = "Hello, and welcome to your personal statistics:", 
                               font = self.fontExample, pady = 10)  #defines text
            welcome.grid(row=0, column=0, sticky="N", columnspan=2) #places text

    #########
        #RATINGS
            self.topleft = tk.Frame(self.mainpage)
            self.topleft.grid(row=1,column=0)
            self.topleft.configure(background="#464646")
            
            #opens data
            with open('./Data/ratings.txt', 'r') as json_file:
                ratings = json.load(json_file)
            #find how long acount has been alive in days
            reg_date = (ratings["reg_date"])
            timealive = Common.timesince(reg_date)
            
            label = ttk.Label(master=self.topleft, text = "Personal Statistics")
            label.configure(anchor="center")
            label.grid(row=0, column=0, sticky = "N", pady = 10)
            
            #gets the data in a suitable format for display
            ratingsdisplay = [
            "User ID: " + (ratings["id"]),
            "Country/Area: " +str((ratings["division"])),
            "Region: " + (ratings["region"]),
            "Pilot Rating: " + str((ratings["pilotrating"])),
            "ATC Rating: " + str((ratings["rating"])),
            "Account Age: " + str(timealive) + " days"
            ]
            
            #displays data
            for i in range(1,7):
                rectangle_2 = tk.Label(self.topleft, bg="#464646", fg="white", text = ratingsdisplay[i-1], font = self.fontSmall,)
                rectangle_2.grid(row=i, column=0, pady = 5)
#########
        #TIMES
            self.MyPersonal.controllingflyingtimes()
            self.topright = tk.Frame(self.mainpage)
            #where frame is in relation to parent
            self.topright.grid(row=1, column=1,  padx=10)
            self.topright.configure(background="#464646")
            for i in range(2):
                #configuration of frame
                self.topright.rowconfigure(i, weight=1, minsize=15)
            self.topright.columnconfigure(0, minsize=20)

            label = ttk.Label(master=self.topright, text = "Personal Graph")
            label.configure(anchor="center")
            label.grid(row=0, column=0, sticky = "N", pady = 10)
            
            #formatting images
            path = "Stats/controllingflyingtimes.png"
            image = Image.open(path)
            new_image = image.resize((300, 200))
            new_image.save(path)
            
            img = ImageTk.PhotoImage(Image.open(path), master = self.window)
            #displaying
            rectangle_3 = tk.Label(self.topright, image = img)
            rectangle_3.photo = img
            rectangle_3.grid(row=1, column=0, pady = 5)

#########
        #FLIGHTS
            flightsdisplay = []
            connectionids1 = []
            with open('./Data/flightplans.txt', 'r') as json_file:
                flightplans = json.load(json_file)
            y = 0
            add = True
            #goes through flightplans and selects most recent 5 unique ones
            #tadd and add are there to make sure they're unique
            for x in flightplans["results"]:
                    add = True
                    toadd = (x["callsign"]) +" "+(x["flight_type"]) +" "+ str(x["aircraft"])[:4] +" "+ (x["dep"]) +"-" + (x["arr"])
                    for z in flightsdisplay:
                        if toadd == z:
                            add = False
                    if add == True:
                        flightsdisplay.append(toadd)
                        connectionids1.append(x["connection_id"])
                        y = y + 1
                
            ###
            self.bottomleft = tk.Frame(self.mainpage)
            #where frame is in relation to parent
            self.bottomleft.grid(row=2, column=0, padx = 10, pady = 30)
            self.bottomleft.configure(background="#464646")
            self.bottomleft.columnconfigure(0)

            #displaying the recent flights

            """
            for i in range(6):
                display = tk.Label(self.ratings, bg="grey", fg="white", text = flightsdisplay[i], font = self.fontSmall,)
                display.grid(row=i, column=0, sticky="n", pady = 5)
            """
            
            self.tree3 = ttk.Treeview(self.bottomleft, selectmode='browse')
            self.tree3.pack(side="left")

            vsb3 = ttk.Scrollbar(self.bottomleft, orient="vertical", command=self.tree3.yview)
            vsb3.pack(side='left', fill='y')

            self.tree3.configure(yscrollcommand=vsb3.set)

            self.tree3["columns"] = ("1", "2","3","4")
            self.tree3['show'] = "headings"
            for i in range(1,5):
                self.tree3.column(i, width=60, anchor='c')
            self.tree3.column(3, width = 50, anchor="c")
            self.tree3.column(4, width = 130, anchor="c")            
            self.tree3.heading("1", text="Callsign")
            self.tree3.heading("2", text="Flight Type")
            self.tree3.heading("3", text="Aircraft")
            self.tree3.heading("4", text="Departure/Arrival")
            
                    
            ids = 0 
            for x in flightsdisplay:
                self.tree3.insert("",'end',values=(x), tags = connectionids1[ids])
                ids = ids + 1
                
            def flightconnection(event, flightplans):
                item = self.tree3.identify('item',event.x,event.y)
                connectionID = self.tree3.item(item, "tags")

                for entry in flightplans["results"]:
                    if str(entry["connection_id"]) == connectionID[0]:
                        display = entry
                        break
                    
                
                for widget in self.mainpage.winfo_children():
                    widget.destroy()  
                self.mainpage.destroy()                  
                #creates new page
                self.mainpage = tk.Frame(self.window) #new frame within the larger one
                self.mainpage.grid(row=0, column=1, pady = 70, padx = 70)
                self.mainpage.configure(background="#464646")

                for x in range(16):
                    self.mainpage.rowconfigure(x, minsize = 10)
                
                rectangle_1 = tk.Label(self.mainpage, bg="#464646", fg="white",
                                       text = "        All Connection Information",
                                       font = self.fontExample, padx = 30, pady = 20)
                rectangle_1.grid(row=0, column=0, sticky="NEW", columnspan = 2)
                    
                row = 1
                column = 0


                for x in display:
                    if x == "route" or x == "rmks":
                         None
                    else:
                        if row > 10:
                            column = 1
                            row = row - 10
                        part1 = str(x)
                        part1 = part1.replace("_", " ")
                        part1 = part1.title()
                        part2 = str(display[x])
                        if part2 == "":
                            part2 = "None"
                        output = part1 + ": " + part2
                        rectangle_1 = tk.Label(self.mainpage, bg="#464646", fg="white", text = output, font = self.fontSmall)
                        rectangle_1.grid(row=row, column=column, sticky="N", columnspan = 1)
                        row = row + 1
                        
                label = ttk.Label(master=self.mainpage, text = "Route:")
                label.configure(anchor="center")
                label.grid(row=12, column=0, sticky = "EW", columnspan = 1)
                t1 = tk.Text(self.mainpage, height = 5, width = 52)
                t1.insert(tk.END, str(display["route"]))            
                t1.grid(row=13, column = 0, sticky = "EW", columnspan = 2)
                label = ttk.Label(master=self.mainpage, text = "Remarks:")
                label.configure(anchor="center")
                label.grid(row=14, column=0, sticky = "EW", columnspan = 1)
                t2 = tk.Text(self.mainpage, height = 5, width = 52)
                t2.insert(tk.END, str(display["rmks"]))
                t2.grid(row=15, column = 0, sticky = "EW", columnspan = 2)
                
                                
            self.tree3.bind("<Double-1>", lambda event, flightplans = flightplans: 
                            flightconnection(event, flightplans))

#########
        #ATCsessions
            atcdisplay = []
            connectionids = []
            with open('./Data/atcsessions.txt', 'r') as json_file:
                atcsessions = json.load(json_file)
            y = 0
            add = True
            #goes through atc sessions and selects most recent 5 unique ones
            #tadd and add are there to make sure they're unique
            for x in atcsessions["results"]: #gets a list of recent ATC connections
                    add = True   #when add is true, it is added to the list, if add is not true, it is not a unique connection
                    toadd = (x["callsign"]) +" "+str((x["aircraftseen"])) +" "+ str(x["squawksassigned"]) +" "+ str(int(float((x["minutes_on_callsign"]))))
                    for z in atcdisplay:
                        if toadd == z:
                            add = False
                    if add == True:
                        connectionids.append(x["connection_id"])
                        atcdisplay.append(toadd)
                        y = y + 1


            ###
                
            self.bottomright = tk.Frame(self.mainpage)
            #where frame is in relation to parent
            self.bottomright.grid(row=2, column=1, padx=10)
            self.bottomright.configure(background="#464646")

            """
            #displaying the recent flights
            for i in range(6):
                display = tk.Label(self.ratings4, bg="grey", fg="white", text = atcdisplay[i], font = self.fontSmall,)
                display.grid(row=i, column=0, sticky="n", pady = 5)
            """
            self.tree2 = ttk.Treeview(self.bottomright, selectmode='browse')
            self.tree2.pack(side="left")

            vsb2 = ttk.Scrollbar(self.bottomright, orient="vertical", command=self.tree2.yview)
            vsb2.pack(side='left', fill='y')

            self.tree2.configure(yscrollcommand=vsb2.set)

            self.tree2["columns"] = ("1", "2","3","4")
            self.tree2['show'] = 'headings'
            for i in range(1,5):
                self.tree2.column(i, width=80, anchor='c')           
            self.tree2.heading("1", text="Station")
            self.tree2.heading("2", text="Planes Seen")
            self.tree2.heading("3", text="Squawks Assigned")
            self.tree2.heading("4", text="Time Online")
            self.tree2.bind("<Double-1>", self.OnDoubleClick2)

            ids = 0 
            for x in atcdisplay:
                self.tree2.insert("",'end',values=(x), tags = connectionids[ids])
                ids = ids + 1

            def atcconnection(event, atcsessions):
                item = self.tree2.identify('item',event.x,event.y)
                connectionID = self.tree2.item(item, "tags")
                print(connectionID[0])
                for entry in atcsessions["results"]:
                    if str(entry["connection_id"]) == str(connectionID[0]):
                        display = entry
                        break
                    
                for widget in self.mainpage.winfo_children():
                    widget.destroy()  
                self.mainpage.destroy()                  
                #creates new page
                self.mainpage = tk.Frame(self.window) #new frame within the larger one
                self.mainpage.grid(row=0, column=1, pady = 70, padx = 70)
                self.mainpage.configure(background="#464646")
                
                rectangle_1 = tk.Label(self.mainpage, bg="#464646", fg="white",
                                       text = "        All Connection Information",
                                       font = self.fontExample, padx = 30, pady = 20)
                rectangle_1.grid(row=0, column=0, sticky="NEW", columnspan = 2)
                    
                row = 1
                column = 0
                
                for x in display:
                    if row > 15:
                        column = 1
                        row = row - 15
                    part1 = str(x)
                    part1 = part1.replace("_", " ")
                    part1 = part1.title()
                    part2 = str(display[x])
                    output = part1 + ": " + part2
                    rectangle_1 = tk.Label(self.mainpage, bg="#464646", fg="white", text = output, font = self.fontSmall)
                    rectangle_1.grid(row=row, column=column, sticky="N", columnspan = 1)
                    row = row + 1
                
            self.tree2.bind("<Double-1>", lambda event, atcsessions = atcsessions: 
                            atcconnection(event, atcsessions))
            
    #########running it all

    ######### if there is no CID entered
        else:
            #code just displays message saying to please enter a valid CID
            self.mainpage = tk.Frame(self.window)
            self.mainpage.configure(background="#464646")
            self.mainpage.grid(row=0, column=1, padx=40)
            welcome = tk.Label(self.mainpage, bg="#464646", fg="white",
            text = "Please enter a valid VATSIM CID to see this page", font = self.fontExample, pady = 10)
            welcome.grid(row=0, column=0, sticky="N", columnspan=2)
            
    ###############Airport Statistics
    def generateThirdpage(self):
        
        self.page = "airport statistics"     
        self.MyGenericStats.__updatedata__(self.MyData)
        

        if self.ICAO == "":

            treedata = self.MyGenericStats.airportslist()
            
            self.mainpage = tk.Frame(self.window)
            for i in range(2):
                self.mainpage.columnconfigure(i, weight=1, minsize=50)
                self.mainpage.rowconfigure(i, weight=1, minsize=50)
            self.mainpage.grid(row=0, column=1, padx=60, pady =40)
            self.mainpage.configure(background="#464646")
            
            welcome = tk.Label(self.mainpage, bg="#464646", fg="white", 
                           text = "Airport Statistics", 
                           font = self.fontExample, pady = 10)  #defines text
            welcome.grid(row=0, column=0, sticky="ew", columnspan=2) #places text
            
            entry_2 = tk.Entry(self.mainpage)
            entry_2.grid(row=1,column=0, sticky="ew", padx=5, pady=5)
            btn_5 = ttk.Button(self.mainpage, text="Submit Airport (ICAO)", command=lambda: self.entering_ICAO(entry_2))
            btn_5.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

            label = ttk.Label(master=self.mainpage, text = "Double click to select airport from table")
            label.configure(anchor="s")
            label.grid(row=2, column=0, columnspan = 2)

            treeframe = tk.Frame(self.mainpage)
            treeframe.grid(row=3,column=0, columnspan = 2)
            self.airporttree = ttk.Treeview(treeframe, selectmode='browse')
            self.airporttree.pack(side="left")

        
            vsb = ttk.Scrollbar(treeframe, orient="vertical", command=self.airporttree.yview)
            vsb.pack(side='left', fill='y')

            self.airporttree.configure(yscrollcommand=vsb.set)

            self.airporttree["columns"] = ("1", "2","3","4")
            self.airporttree['show'] = "headings"
            for i in range(1,5):
                self.airporttree.column(i, width=75, anchor='c')            
            self.airporttree.heading("1", text="Airport")
            self.airporttree.heading("2", text="Departures")
            self.airporttree.heading("3", text="Arrivals")
            self.airporttree.heading("4", text="Total")
            
            for x in treedata:
                self.airporttree.insert("",'end',values=(x))
            self.airporttree.bind("<Double-1>", self.airportsdoubleclick)

        else:

            departures = self.MyGenericStats.departures(self.ICAO)
                
            arrivals = self.MyGenericStats.arrivals(self.ICAO)

            statsdisplay = self.MyGenericStats.generalstats(self.ICAO)
        
            greeting = "Statistics about " +str(self.ICAO) + ":" 

            self.mainpage = tk.Frame(self.window) #new frame within the larger one
            self.mainpage.configure(background="#464646")
            self.mainpage.grid(row=0, column=1)
            #creates grid
            for i in range(0,2):
                self.mainpage.columnconfigure(i, weight=1, minsize=30)
            for i in range(2,3):    
                self.mainpage.rowconfigure(i, weight=1, minsize=30)

            rectangle_1 = tk.Label(self.mainpage, bg="#464646", fg="white", text = greeting , font = self.fontExample)
            rectangle_1.grid(row=0, column=0, columnspan = 2)
            
            #putting text in
            self.stats = tk.Frame(self.mainpage)
                #where frame is in relation to parent
            self.stats.grid(row=2, column=0, padx=10, pady=10)
            self.stats.configure(background="#464646")
            for i in range(0,6):    
                self.stats.rowconfigure(i, weight=1, minsize=10)
            self.stats.columnconfigure(0, weight=1, minsize=10)
            
            label = ttk.Label(master=self.stats, text = "Airport Statistics:")
            label.configure(anchor="center")
            label.grid(row=0, column=0)

            for i in range(1,6):
                display = tk.Label(self.stats, bg="#464646", fg="white", text = statsdisplay[i-1], font = self.fontSmall,)
                display.grid(row=i, column=0, sticky="n", pady = 5)
                
            ####################
            self.frame = tk.Frame(self.mainpage)
            #where frame is in relation to parent
            self.frame.grid(row=2, column=1, padx=10, pady=10)
            self.frame.configure(background="#464646")
            for i in range(0,4):    
                self.frame.rowconfigure(i, weight=1, minsize=10)
            self.frame.columnconfigure(0, weight=1, minsize=10)
            entry_2 = tk.Entry(self.frame)     
            entry_2.grid(row=1,column=0, padx=5, pady=10, sticky = "S")
            
            btn_5 = ttk.Button(self.frame, text="Submit New Airport Code (ICAO)", command=lambda: self.entering_ICAO(entry_2), width = 40)
            btn_5.grid(row=2, column=0, padx=5, pady=5)            

            
            ####################
            self.departures = tk.Frame(self.mainpage)
            #where frame is in relation to parent
            self.departures.grid(row=3, column=0, padx=10, pady=10)
            self.departures.configure(background="#464646")
            for i in range(0,5):    
                self.departures.rowconfigure(i, weight=1, minsize=10)
            self.departures.columnconfigure(0, weight=1, minsize=10)           
            
            label = ttk.Label(master=self.departures, text = "Departure Board:")
            label.configure(anchor="center")
            label.grid(row = 0, column = 0)
            
            self.treeframe = tk.Frame(self.departures)
            
            #where frame is in relation to parent
            self.treeframe.grid(row=1, column=0, padx=10, pady=10, sticky = "NSWE")
            self.treeframe.configure(background="#464646")
            for i in range(0,1):    
                self.departures.rowconfigure(i, weight=1, minsize=10)
            self.departures.columnconfigure(0, weight=1, minsize=10)      
            
            self.tree = ttk.Treeview(self.treeframe, selectmode='browse')
            self.tree.pack(side="left")

            vsb = ttk.Scrollbar(self.treeframe, orient="vertical", command=self.tree.yview)
            vsb.pack(side='left', fill='y')

            self.tree.configure(yscrollcommand=vsb.set)

            self.tree["columns"] = ("1", "2","3","4")
            self.tree['show'] = "headings"
            self.tree.bind("<Double-1>", self.OnDoubleClick)
            for i in range(1,5):
                self.tree.column(i, width=100, anchor='c')
            self.tree.column(3, width = 50, anchor="c")
            self.tree.column(4, width = 130, anchor="c")            
            self.tree.heading("1", text="Callsign")
            self.tree.heading("2", text="Destination")
            self.tree.heading("3", text="Aircraft")
            self.tree.heading("4", text="Departure Time (GMT)")

            
            for x in departures:
                self.tree.insert("",'end',values=(x))


    
 ############################


            self.departures = tk.Frame(self.mainpage)
            #where frame is in relation to parent
            self.departures.grid(row=3, column=1, padx=10, pady=10, sticky = "NSWE")
            self.departures.configure(background="#464646")
            for i in range(0,5):    
                self.departures.rowconfigure(i, weight=1, minsize=10)
            self.departures.columnconfigure(0, weight=1, minsize=10)           
            
            label = ttk.Label(master=self.departures, text = "Arrival Board:")
            label.configure(anchor="center")
            label.grid(row = 0, column = 0)
            
            self.treeframe = tk.Frame(self.departures)
            
            #where frame is in relation to parent
            self.treeframe.grid(row=1, column=0, padx=10, pady=10, sticky = "NSWE")
            self.treeframe.configure(background="#464646")
            for i in range(0,1):    
                self.departures.rowconfigure(i, weight=1, minsize=10)
            self.departures.columnconfigure(0, weight=1, minsize=10)      
            
            self.tree2 = ttk.Treeview(self.treeframe, selectmode='browse')
            self.tree2.pack(side="left")

            vsb2 = ttk.Scrollbar(self.treeframe, orient="vertical", command=self.tree2.yview)
            vsb2.pack(side='left', fill='y')

            self.tree2.configure(yscrollcommand=vsb2.set)

            self.tree2["columns"] = ("1", "2","3","4")
            self.tree2['show'] = 'headings'
            for i in range(1,5):
                self.tree2.column(i, width=100, anchor='c')
            self.tree2.column(3, width = 50, anchor="c")
            self.tree2.column(4, width = 130, anchor="c")            
            self.tree2.heading("1", text="Callsign")
            self.tree2.heading("2", text="Arriving From")
            self.tree2.heading("3", text="Aircraft")
            self.tree2.heading("4", text="Departure Time (GMT)")
            self.tree2.bind("<Double-1>", self.OnDoubleClick2)
            
            for x in arrivals:
                self.tree2.insert("",'end',values=(x))  


    def OnDoubleClick(self, event):
        item = self.tree.identify('item',event.x,event.y)
        self.callsign = (self.tree.item(item,"values"))
        self.callsign = self.callsign[0]
        self.aircraftstatistics()
        
    def OnDoubleClick2(self, event):
        item = self.tree2.identify('item',event.x,event.y)
        self.callsign = (self.tree2.item(item,"values"))
        self.callsign = self.callsign[0]
        self.aircraftstatistics()

    def airportsdoubleclick(self,event):
        item = self.airporttree.identify('item',event.x,event.y)
        self.ICAO = (self.airporttree.item(item,"values"))
        self.ICAO = self.ICAO[0]
        self.airportstatistics()
        
    def generateFourthpage(self):
        
        self.page = "airport statistics"     
        self.MyGenericStats.__updatedata__(self.MyData)
        

        if self.callsign == "":

            treedata = self.MyGenericStats.aircraftlist()
            
            self.mainpage = tk.Frame(self.window)
            for i in range(2):
                self.mainpage.columnconfigure(i, weight=1, minsize=50)
                self.mainpage.rowconfigure(i, weight=1, minsize=50)
                
            self.mainpage.grid(row=0, column=1, padx=60, pady=40)
            self.mainpage.configure(background="#464646")
            
            welcome = tk.Label(self.mainpage, bg="#464646", fg="white", 
                           text = "Flight Statistics", 
                           font = self.fontExample, pady = 10)  #defines text
            welcome.grid(row=0, column=0, sticky="ew", columnspan=2) #places text
            
            entry_3 = tk.Entry(self.mainpage)
            entry_3.grid(row=1,column=0, sticky="ew", padx=5, pady=5)
            btn_6 = ttk.Button(self.mainpage, text="Submit Aircraft Callsign", command=lambda: self.entering_callsign(entry_3))
            btn_6.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

            label = ttk.Label(master=self.mainpage, text = "Double click to select callsign from table")
            label.configure(anchor="s")
            label.grid(row=2, column=0, columnspan = 2)
            
            treeframe = tk.Frame(self.mainpage)
            treeframe.grid(row=3,column=0, columnspan = 2)
            self.aircrafttree = ttk.Treeview(treeframe, selectmode='browse')
            self.aircrafttree.pack(side="left")


            vsb = ttk.Scrollbar(treeframe, orient="vertical", command=self.aircrafttree.yview)
            vsb.pack(side='left', fill='y')

            self.aircrafttree.configure(yscrollcommand=vsb.set)

            self.aircrafttree["columns"] = ("1", "2","3","4")
            self.aircrafttree['show'] = "headings"
            for i in range(1,5):
                self.aircrafttree.column(i, width=75, anchor='c')            
            self.aircrafttree.heading("1", text="Callsign")
            self.aircrafttree.heading("2", text="Departure")
            self.aircrafttree.heading("3", text="Arrival")
            self.aircrafttree.heading("4", text="Aircraft")
            
            for x in treedata:
                self.aircrafttree.insert("",'end',values=(x))
            self.aircrafttree.bind("<Double-1>", self.aircraftsdoubleclick)

        else:
            
            statsdisplay = self.MyGenericStats.aircraftstats(self.callsign)
            flightplandisplay = self.MyGenericStats.flightplanstats(self.callsign)
            
            print(statsdisplay)
            self.mainpage = tk.Frame(self.window)
            self.mainpage.grid(row=0, column=1, padx=40)
            self.mainpage.configure(background="#464646")
            for i in range(0,1):
                self.mainpage.columnconfigure(i, weight=1, minsize=30)
                
            title = tk.Frame(self.mainpage)
            title.grid(row = 0, column = 0, columnspan = 2)
            title.configure(background="#464646")
            
            label = tk.Label(master=title, text = " Flight Information:", bg="#464646", fg="white", font = self.fontExample)
            label.configure(anchor="center")
            label.grid(row=0, column=0, columnspan = 2, pady= 15)
            
            self.stats = tk.Frame(self.mainpage)
            self.stats.grid(row = 1, column = 0)
            self.stats.configure(background="#464646")
            self.inputs = tk.Frame(self.mainpage)
            self.inputs.grid(row = 1, column = 1)
            self.inputs.configure(background="#464646")
            
            self.flightplan = tk.Frame(self.mainpage)            
            self.flightplan.grid(row = 2, column = 0, columnspan = 2, sticky ="N")            
            self.flightplan.configure(background="#464646")
            
            for i in range(0,2):
                self.flightplan.columnconfigure(i, weight=1, minsize=10)
            
            label = ttk.Label(master=self.stats, text = "Aircraft Statistics:")
            label.configure(anchor="center")
            label.grid(row=0, column=0, sticky = "EW", pady = 10)
            
            label = ttk.Label(master=self.flightplan, text = "Filed Flightplan:")
            label.configure(anchor="center")
            label.grid(row=0, column=0, sticky = "EWN", columnspan = 3)

            label = ttk.Label(master=self.inputs, text = "Further Information:")
            label.configure(background="#464646")                
            label.grid(row=0,column=0, pady = 5, sticky = "N")
            
            for i in range(2,15):
                display = tk.Label(self.stats, bg="#464646", fg="white", text = statsdisplay[i-2], font = self.fontSmall,)
                display.grid(row=(i-1), column=0, sticky="wn")
            for i in range(0,3):
                display = tk.Label(self.flightplan, bg="#464646", fg="white", text = flightplandisplay[i], font = self.fontSmall,)
                display.grid(row=i+1, column=0, sticky="wn", padx=5)                       
            for i in range(0,3):
                display = tk.Label(self.flightplan, bg="#464646", fg="white", text = flightplandisplay[i+3], font = self.fontSmall,)
                display.grid(row=i+1, column=1, sticky="wn", padx=5)             
            for i in range(0,3):
                display = tk.Label(self.flightplan, bg="#464646", fg="white", text = flightplandisplay[i+6], font = self.fontSmall,)
                display.grid(row=i+1, column=2, sticky="wn", padx=5)
                                
            entry_3 = tk.Entry(self.inputs)
            entry_3.grid(row=1,column=0, sticky="ew", padx=5, pady=5)
            btn_6 = ttk.Button(self.inputs, text="Submit New Aircraft Callsign", command=lambda: self.entering_callsign(entry_3))
            btn_6.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
            placeholder = tk.Label(master=self.inputs, text = "")
            placeholder.configure(background="#464646")                
            placeholder.grid(row=3,column=0)
            btn_8 = ttk.Button(self.inputs, text="View This User's Personal Stats", command=lambda: self.entering_CID(statsdisplay[0], False))
            btn_8.grid(row=4, column=0, sticky="ew", padx=5, pady=5)
            btn_9 = ttk.Button(self.inputs, text="View Destination Information", command=lambda: self.airportinfo(flightplandisplay[4]))
            btn_9.grid(row=7, column=0, sticky="ew", padx=5, pady=5)
            btn_10 = ttk.Button(self.inputs, text="View Origin Information", command=lambda: self.airportinfo(flightplandisplay[3]))
            btn_10.grid(row=8, column=0, sticky="ew", padx=5, pady=5)

            label = ttk.Label(master=self.flightplan, text = "Route:")
            label.configure(anchor="center")
            label.grid(row=10, column=0, sticky = "EW", columnspan = 1)
            t1 = tk.Text(self.flightplan, height = 5, width = 52)
            t1.insert(tk.END, str(flightplandisplay[9]))            
            t1.grid(row=11, column = 0, sticky = "EW", columnspan = 3)
            label = ttk.Label(master=self.flightplan, text = "Remarks:")
            label.configure(anchor="center")
            label.grid(row=12, column=0, sticky = "EW", columnspan = 1)
            t2 = tk.Text(self.flightplan, height = 5, width = 52)
            t2.insert(tk.END, str(flightplandisplay[10]))
            t2.grid(row=13, column = 0, sticky = "EW", columnspan = 3)
            label = ttk.Label(master=self.flightplan, text = "")
            label.configure(anchor="center")
            label.grid(row=14, column=0, sticky = "EW", columnspan = 3)
            
    def aircraftsdoubleclick(self,event):
        item = self.aircrafttree.identify('item',event.x,event.y)
        self.callsign = (self.aircrafttree.item(item,"values"))
        self.callsign = self.callsign[0]
        self.aircraftstatistics()
        
    def airportinfo(self, ICAO):
        self.ICAO = ICAO[-4:]
        self.airportstatistics()
        
    def aboutPage(self):
        #destroys all widgets currently on screen     
        self.page = "about"
        self.mainpage = tk.Frame(self.window)    
        self.mainpage.grid(row=0, column=1, padx=50, pady=30)
        self.mainpage.configure(background="#464646")
        info = ["Hello and welcome to my little program which attempts to create statistics and graphs based on activity on the VATSIM Network!",
                "",
                "Most things in the application are clickable, or double clickable. As a rule of thumb if something isn't text then try double",
                "clicking it. For example; you can double click on all the tables in the program and the images on the Network Statistics page",
                "get enlarged if you double click them.",
                "",
                "If you don't know much about flightsimming you might not understand everything on here but that's fine! I doubt this program will",
                "convince you but the VATSIM Network is great for learning about aviation and having fun. A few things it might be helpful to know:",
                "",
                "- VATSIM is a nonprofit organization that operates an online flight-simulation network where members can fly as pilots or direct",
                "   traffic as air traffic controllers participating in a close approximation of real-life aviation procedures.",
                "- An ICAO code is a unique, 4 character code, that every airport has e.g. Heathrow is EGLL",
                "- A callsign is a unique combination of numbers and letters that every flight has, sometimes the starting letters are the airline",
                "   e.g. Lufthansa is DLH so DLH17MC is a Lufthansa flight. In other cases, callsigns are the same as an aircraft's tail number.",
                "- This program generally shortens aircraft types into their ICAO Aircraft type designators. e.g. Boeing 737-800s are B738",    
                "- If you're wondering what ICAO/Callsign are what airport/callsign you can just google it, they're all on Wikipedia!",
                "- A CID is a unique code given to every VATSIM member. You can view any VATSIM member's information on this program.",
                "",
                "There are other things you might not understand like Squawk codes, why all the times are in GMT, and what an ATIS is.",
                "Unfortunately I'm running out of text space here, but everything is on the web so bing it if you must...",
                "",
                "Feel free to do whatever you want with this program, or message me for the source code, it's written (incredibly badly)",
                "in Python.",
                "",
                "",
                "- Barney Wakefield (No Rights Reserved)"
                ]
        
        row = 0
        for text in info:
            label = ttk.Label(self.mainpage, text = text)
            label.grid(row=row, column=0, sticky = "w")
            row = row + 1
    
    #BUTTONS AND NAVIGATIONAL BAR
    def bar(self):
        fr_buttons = tk.Frame(self.window, bd=0)
        #styling buttons
        style = ttk.Style(fr_buttons)
        style.theme_use("equilux")
        style.configure('TButton', background='#496d89')
        style.configure("TButton", focuscolor=style.configure(".")["background"])
        #defining buttions
        btn_1 = ttk.Button(fr_buttons, text="Network Statistics", command=lambda: self.networkstatistics())
        btn_2 = ttk.Button(fr_buttons, text="Personal Statistics", command=lambda: self.personalstatistics())
        btn_4 = ttk.Button(fr_buttons, text="Airport Statistics", command=lambda: self.airportstatisticsbar())
        btn_7 = ttk.Button(fr_buttons, text="Flight Statistics", command=lambda: self.aircraftstatisticsbar())
        btn_11 = tk.Button(fr_buttons, text="About", command=lambda: self.aboutPage(), bd = 0, bg = "#496d89", fg = "white", activebackground = "#496d89", font=('Arial', 8,))
        entry_1 = tk.Entry(fr_buttons)
        text_1 = tk.Label(fr_buttons, bg="#496d89", fg="white", text = "Enter CID here:")
        place = tk.Label(fr_buttons, bg="#496d89")
        btn_3 = ttk.Button(fr_buttons, text="Submit CID", command=lambda: self.entering_CID(entry_1, True))
        rectangle_1 = tk.Label(fr_buttons, text="VStats", bg="#496d89", fg="white", font = ("Arial", 17))
        #placing buttons
        rectangle_1.grid(row=1, column=0, sticky="ew", padx=5, pady=40)
        rectangle_1.bind('<Button-1>', self.aboutPagegenerate)
        btn_1.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        btn_2.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
        btn_4.grid(row=4, column=0, sticky="ew", padx=5, pady=5)
        btn_7.grid(row=5, column=0, sticky="ew", padx=5, pady=5)
        #btn_11.grid(row=6, column=0, sticky = "s", padx=5, pady=0)
        
        #Moves submit CID to the bottom
        place.grid(row=7,column=0, sticky="ew", padx=5, pady=5)
        text_1.grid(row=8,column=0, sticky="ew", padx=5, pady=5)
        entry_1.grid(row=9,column=0, sticky="ew", padx=5, pady=5)
        btn_3.grid(row=10, column=0, sticky="ew", padx=5, pady=5)
        
        
        fr_buttons.grid(row=0, column=0, sticky="ns")
        fr_buttons.configure(background="#496d89")
        
    def aboutPagegenerate(self,event):
        #destroys all widgets currently on screen
        for widget in self.mainpage.winfo_children():
            widget.destroy()
        #creates new page
        self.mainpage.destroy()
        self.aboutPage()
        
    def networkstatistics(self):
        #destroys all widgets currently on screen
        for widget in self.mainpage.winfo_children():
            widget.destroy()
        #creates new page
        self.mainpage.destroy()
        self.generateMainpage()
        
    def networkstatisticsregenerate(self):
        if self.page == "network statistics":
            #destroys all widgets currently on screen
            for widget in self.mainpage.winfo_children():
                widget.destroy()
            #creates new page
            self.mainpage.destroy()
            self.generateMainpage()
    def networkstatisticsdouble(self,event):
        self.networkstatistics()
    def personalstatistics(self):
        #destroys all widgets currently on screen
        for widget in self.mainpage.winfo_children():
            widget.destroy()
        #creates new page
        self.mainpage.destroy()
        self.generateSecondpage()
        
    def airportstatisticsbar(self):
        self.ICAO = ""
        self.airportstatistics()
        
    def aircraftstatisticsbar(self):
        self.callsign = ""
        self.aircraftstatistics()
        
    def airportstatistics(self):
        #destroys all widgets currently on screen
        for widget in self.mainpage.winfo_children():
            widget.destroy()
        #creates new page
        self.mainpage.destroy()
        self.generateThirdpage()

    def aircraftstatistics(self):
        #destroys all widgets currently on screen
        for widget in self.mainpage.winfo_children():
            widget.destroy()
        #creates new page
        self.mainpage.destroy()
        self.generateFourthpage()
        
    def entering_ICAO(self, entry_2):
        self.ICAO = entry_2.get()
        self.ICAO = self.ICAO.upper()
        self.airportstatistics()
        
    def entering_callsign(self, entry_3):
        self.callsign = entry_3.get()
        self.callsign = self.callsign.upper()        
        if self.MyGenericStats.validatecallsign(self.callsign) == True:                        
            self.aircraftstatistics()
        else:
            self.callsign = ""
            self.aircraftstatistics()
        
    #CHECKS WHAT ACTION NEEDS TO BE TAKEN BASED ON CID ENTERED.
    def entering_CID(self, entry_1, where):
        if where == True:
            possCID = entry_1.get()
        else:
            possCID = entry_1[5:]
        try:
            with open('./Data/ratings.txt', 'r') as json_file:
                ratings = json.load(json_file)
                time = (ratings["timestamp"])
                time = time[:19]
                time = Common.secondssince(time)
                rate = ratings["id"]
        except:
            #exception handling 
            time = 0
            rate = ""
        #get old time and do current time check
        print(time)
        print(rate)
        if possCID == rate and time < 1300:
            #checks if we already have the data
            print("success")
            self.validCID = True
            self.CID = possCID
            user = APIData(possCID)
            self.user = user
            self.MyPersonal.__updatedata__(self.user, self.CID)
            self.personalstatistics()
    
        #else:
            #if self.lastCID == possCID:
                #print("repetition")
        else:
            check = requests.get("https://api.vatsim.net/api/ratings/" + str(possCID) + "/")
            print(check)
            #gets rid of now out of date graphs/charts
            todelete = self.getfunctionspersonal()
            print(todelete)
            for x in todelete:
                try:
                    os.remove("Stats/"+ x +".png")
                except:
                    None
            if str(check) == "<Response [200]>":#checks for good response            
                user = APIData(possCID)
                self.user = user
                self.validCID = True
                self.CID = possCID
                self.MyPersonal.__updatedata__(self.user, self.CID)
                self.personalstatistics()
                print("API")
            else: #if bad response 
                print("DID NOT API")
                self.validCID = False
                self.personalstatistics()


if __name__ == "__main__":
    window = tk.Tk()
    MyGui = GUI(window, ThemedStyle)
    def runs():
        schedule.run_pending()
        window.after(500, runs)
    runs()
    while True:
        schedule.run_pending()

        window.mainloop()



