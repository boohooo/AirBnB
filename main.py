# Multi-frame tkinter application v2.3
import tkinter as tk  # python 3
from tkinter import font as tkfont
from tkinter import *
from datetime import date
from datetime import time
import datetime
from PIL import ImageTk
from PIL import Image
import webbrowser
from functions import *
from cleansing import *

#Import Python files    
try: #Sometimes, if the excel file is open, the program might not run. So this shows the user that the excel needs to be closed.
    
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    currentTime = datetime.datetime.now()
    current_hrmin = currentTime.strftime('%H:%M')
    current_day = currentTime.weekday() + 1
    
    
    class SampleApp(tk.Tk): 
        def __init__(self):
            tk.Tk.__init__(self)
            self._frame = None
            self.geometry("800x712+100+100") #sets the geometry size of app
            self.switch_frame(StartPage)
    
        def switch_frame(self, frame_class):
            """Destroys current frame and replaces it with a new one."""
            new_frame = frame_class(self)
            if self._frame is not None:
                self._frame.destroy()
            self._frame = new_frame
            self._frame.pack()
            
    
    
    class StartPage(tk.Frame): 
        def __init__(self, master):
            tk.Frame.__init__(self, master)
    
            # Must put the image codes above the rest
    
            canvas = Canvas(self, height=810, width=810)
            canvas.pack()
            logo = tk.PhotoImage(file="ntuappbg.gif")
            canvas.create_image(405, 360, image=logo)
            canvas.image = logo  # Reference to image
    
            today = datetime.datetime.now()
            todayFormatted = today.strftime("%A") + " " + today.strftime("%d/%m/%Y") + " " + today.strftime("%H:%M")
            # status = Label(self, text=todayFormatted, bd=1, relief=SUNKEN, anchor=N,
            #                font=("Yu Gothic UI Semibold", 15))
            canvas.create_text(420,10,text=todayFormatted,font=("Yu Gothic UI Semibold", 15), fill="white")
            canvas.create_text(420,80, text="Airbnb Recommendation System", font=("Franklin Gothic Medium Cond", 30), fill="white")
    
            # =============================================================================
            # Start date
            # =============================================================================
            canvas.create_text(160,150, text="1. Select start and end dates:", font=("Franklin Gothic Medium Cond", 20), fill="white")
            
            canvas.create_text(50,220, text="Start", font=("Franklin Gothic Medium Cond", 20), fill="white")            
            
            startMonth = list(range(1, 13))
            self.startmonth = StringVar()
            self.startmonth.set(startMonth[0])
            canvas.create_text(150,190,text="Month", fill="white")
            startmonthMenu = tk.OptionMenu(self, self.startmonth, *startMonth)
            startmonthMenu.config(width=15, height=1, bg ="grey")
            startmonthMenu_window = canvas.create_window(150,220,window=startmonthMenu)
            self.startmonth.trace('w', self.startmonthGetValue)
    
            startDay = list(range(1, 32))
            self.startday = StringVar()
            self.startday.set(startDay[0])
            canvas.create_text(300, 190, text="Day", fill="white")
            startdayMenu = tk.OptionMenu(self, self.startday, *startDay)
            startdayMenu.config(width=15, height=1, bg ="grey")
            startdayMenu_window = canvas.create_window(300,220,window=startdayMenu)
            self.startday.trace('w', self.startdayGetValue)
    
            startYear = list(range(2016, 2018))
            self.startyear = StringVar()
            self.startyear.set(startYear[0])
            canvas.create_text(450, 190, text="Year", fill="white")
            startyearMenu = tk.OptionMenu(self, self.startyear, *startYear)
            startyearMenu.config(width=15, height=1, bg ="grey")
            startyearMenu_window = canvas.create_window(450, 220, window=startyearMenu)
            self.startyear.trace('w', self.startyearGetValue)
    
            # =============================================================================
            # End date
            # =============================================================================
            canvas.create_text(50,300, text="End", font=("Franklin Gothic Medium Cond", 20), fill="white")
            
            endMonth = list(range(1, 13))
            self.endmonth = StringVar()
            self.endmonth.set(endMonth[0])
            canvas.create_text(150,270,text="Month", fill="white")
            endmonthMenu = tk.OptionMenu(self, self.endmonth, *endMonth)
            endmonthMenu.config(width=15, height=1, bg ="grey")
            endmonthMenu_window = canvas.create_window(150,300,window=endmonthMenu)
            self.endmonth.trace('w', self.endmonthGetValue)
                        
            endDay = list(range(1, 32))
            self.endday = StringVar()
            self.endday.set(endDay[0])
            canvas.create_text(300, 270, text="Day", fill="white")
            enddayMenu = tk.OptionMenu(self, self.endday, *endDay)
            enddayMenu.config(width=15, height=1, bg ="grey")
            enddayMenu_window = canvas.create_window(300,300,window=enddayMenu)
            self.endday.trace('w', self.enddayGetValue)
            
            endYear = list(range(2016, 2018))
            self.endyear = StringVar()
            self.endyear.set(endYear[0])
            canvas.create_text(450, 270, text="Year", fill="white")
            endyearMenu = tk.OptionMenu(self, self.endyear, *endYear)
            endyearMenu.config(width=15, height=1, bg ="grey")
            endyearMenu_window = canvas.create_window(450, 300, window=endyearMenu)
            self.endyear.trace('w', self.endyearGetValue)
 
            # =============================================================================
            # Algorithm Type: Cosine-Similarity or K-Nearest Neighbours
            # =============================================================================
            canvas.create_text(128,360, text="2. Select algorithm type", font=("Franklin Gothic Medium Cond", 20), fill="white")
            
            algoType = ["Cosine-Similarity", "K-Nearest Neighbour"]
            self.algoType = StringVar()
            self.algoType.set(algoType[0])
            algoTypeMenu = tk.OptionMenu(self, self.algoType, *algoType)
            algoTypeMenu.config(width=20, height=1, bg ="orange")
            algoTypeMenu_window = canvas.create_window(120, 400, window=algoTypeMenu)            
            self.algoType.trace('w', self.algoTypeGetValue)   # continuously trace the value of the selected items in the OptionMenu and update the var variable, using the function self.getValue

            # =============================================================================
            # Enter preferences
            # =============================================================================
            canvas.create_text(180, 460, text="3. Enter the preferences for a room:", font=("Franklin Gothic Medium Cond", 20), fill="white")
       
            self.preferences = StringVar()
            entry_box = tk.Entry(self, textvariable=self.preferences, width=100)
            entrybox_window = canvas.create_window(320, 490, window=entry_box)
            self.preferences.trace('w', self.preferencesGetValue)

            # =============================================================================
            # Confirm button           
            # =============================================================================
            confirmButton = Button(self, text="Confirm", width=25, height=2, bg="lightgreen", command=lambda: master.switch_frame(NextPage))
            confirmButton_window = canvas.create_window(400, 650, window=confirmButton)

        # =============================================================================
        # Redefine the value after every change to the Option menu - took me hours to figure this out   
        # =============================================================================
        def startmonthGetValue(self, *args):
            global user_startmonth
            if (int(self.startmonth.get()) <10):
                user_startmonth = "0"+str(self.startmonth.get())
            else:
                user_startmonth = str(self.startmonth.get())
            return(self.startmonth.get()) 
        
        def startdayGetValue(self, *args):
            global user_startday
            if (int(self.startday.get()) <10):
                user_startday = "0"+str(self.startday.get())
            else:
                user_startday = str(self.startday.get())
            return(self.startday.get()) 
        
        def startyearGetValue(self, *args):
            global user_startyear
            user_startyear = str(self.startyear.get())
            return(self.startyear.get()) 

        def endmonthGetValue(self, *args):
            global user_endmonth
            if (int(self.endmonth.get()) <10):
                user_endmonth = "0"+str(self.endmonth.get())
            else:
                user_endmonth = str(self.endmonth.get())
            return(self.endmonth.get())

        def enddayGetValue(self, *args):
            global user_endday
            if (int(self.endday.get()) <10):
                user_endday = "0"+str(self.endday.get())
            else:
                user_endday = str(self.endday.get())
            return(self.endday.get()) 
        
        def endyearGetValue(self, *args):
            global user_endyear
            user_endyear = str(self.endyear.get())
            return(self.endyear.get()) 

        def algoTypeGetValue(self, *args):
            global user_algoType
            user_algoType = str(self.algoType.get())
            return(self.algoType.get()) 
        
        def preferencesGetValue(self, *args):
            global user_preference 
            user_preference = str(self.preferences.get())
            return(self.preferences.get()) 
    
    
    class NextPage(tk.Frame): 
        def __init__(self, master):
            tk.Frame.__init__(self, master)

            # Must put the image codes above the rest
    
            canvas = Canvas(self, height=810, width=810)
            canvas.pack()
            logo = tk.PhotoImage(file="ntuappbg.gif")
            canvas.create_image(405, 360, image=logo)
            canvas.image = logo  # Reference to image
    
            today = datetime.datetime.now()
            todayFormatted = today.strftime("%A") + " " + today.strftime("%d/%m/%Y") + " " + today.strftime("%H:%M")

            canvas.create_text(420,10,text=todayFormatted,font=("Yu Gothic UI Semibold", 15), fill="white")
            
            # =============================================================================
            #  Concatenate the dates           
            # =============================================================================
            user_startDate = str(user_startyear) + "-" + str(user_startmonth) + "-" + str(user_startday)
            user_endDate = str(user_endyear) + "-" + str(user_endmonth) + "-" + str(user_endday) 
            
            # =============================================================================
            # Magic time            
            # =============================================================================
            calendarDF= filterCalendar(user_startDate, user_endDate)
            dataset = topListings(user_preference, user_algoType,calendarDF)
            googleMaps(dataset)
            calendarImg(dataset)
            dataset= dataset[['id','name','score']]
            
            # Change the datatype from object to numeric
            dataset["score"] = pd.to_numeric(dataset["score"])
            dataset['score'] = dataset['score'].round(2)
            dataset = dataset.rename(columns={"id": "ID", "name": "Name","score": "Score"})
            
            # =============================================================================
            # Display the ID, name, score on GUI
            # =============================================================================
            datasetID = (dataset['ID']).to_csv(index=False, header=True, sep='\n')
            canvas.create_text(60,260,text=datasetID,font=("Yu Gothic UI Semibold", 12), fill="white")

            datasetName = (dataset['Name']).to_csv(index=False, header=True, sep='\n')
            canvas.create_text(270,260,text=datasetName,font=("Yu Gothic UI Semibold", 12), fill="white")
            
            datasetScore = (dataset['Score']).to_csv(index=False, header=True, sep='\n')
            canvas.create_text(470,260,text=datasetScore,font=("Yu Gothic UI Semibold", 12), fill="white")
            
            # =============================================================================
            #  Display the calendar - can't find shortcuts, for loop is possible if all buttons are the same, 
            # =============================================================================
            imgList = ["img0.png","img1.png","img2.png","img3.png","img4.png"]
            
    
#            for num, png in enumerate(imgList):    
##                imgButton = tk.Button(self,text="Open", width=10, height=1, bg="cyan",command = self.wbcalendar)
#                imgButton = tk.Button(self,text="Open", width=10, height=1, bg="cyan",command = webbrowser.open_new_tab(png))   
#                imgButton_window = canvas.create_window(580, 180+xAxis, window=imgButton)
#                xAxis += 40
     
            imgButton = tk.Button(self,text="Calendar", width=10, height=1, bg="cyan",command = self.wbcalendar0)
            imgButton_window = canvas.create_window(580, 180, window=imgButton)
   
            imgButton = tk.Button(self,text="Calendar", width=10, height=1, bg="cyan",command = self.wbcalendar1)
            imgButton_window = canvas.create_window(580, 220, window=imgButton)
 
            imgButton = tk.Button(self,text="Calendar", width=10, height=1, bg="cyan",command = self.wbcalendar2)
            imgButton_window = canvas.create_window(580, 260, window=imgButton)
 
            imgButton = tk.Button(self,text="Calendar", width=10, height=1, bg="cyan",command = self.wbcalendar3)
            imgButton_window = canvas.create_window(580, 300, window=imgButton)
  
            imgButton = tk.Button(self,text="Calendar", width=10, height=1, bg="cyan",command = self.wbcalendar4)
            imgButton_window = canvas.create_window(580, 340, window=imgButton)

            # =============================================================================
            # Website
            # =============================================================================
            webButton = tk.Button(self,text="View the listingsID on the map", width=25, height=1, bg="orange",command = self.wbbrowser)
            webButton_window = canvas.create_window(400, 550, window=webButton)
            
            backButton = tk.Button(self, text="Back", width=25, height=2, bg="lightblue",command=lambda: master.switch_frame(StartPage))
            backButton_window = canvas.create_window(400, 650, window=backButton)
            
        def wbbrowser(self):
            webbrowser.open_new_tab('map.html')
        
        def wbcalendar0(self):
            webbrowser.open_new_tab('img0.png')
        
        def wbcalendar1(self):
            webbrowser.open_new_tab('img1.png')
            
        def wbcalendar2(self):
            webbrowser.open_new_tab('img2.png')
            
        def wbcalendar3(self):
            webbrowser.open_new_tab('img3.png')
            
        def wbcalendar4(self):
            webbrowser.open_new_tab('img4.png')
                
    if __name__ == "__main__":
        app = SampleApp()
        app.mainloop()
except:
    print ("Main.py got issue!" )        