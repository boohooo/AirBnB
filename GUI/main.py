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
            canvas.create_text(420,80, text="Airbnb Recommendation App", font=("Franklin Gothic Medium Cond", 30), fill="white")
    
            # =============================================================================
            # Start
            # =============================================================================
            canvas.create_text(160,150, text="1. Select start and end dates:", font=("Franklin Gothic Medium Cond", 20), fill="white")
            
            canvas.create_text(50,220, text="Start", font=("Franklin Gothic Medium Cond", 20), fill="white")
            
            startMonth = list(range(1, 13))
            self.startmonth = StringVar()
            self.startmonth.set(startMonth[0])
            canvas.create_text(150,190,text="Month", fill="white")
            startmonthMenu = OptionMenu(self, self.startmonth, *startMonth)
            startmonthMenu.config(width=15, height=1, bg ="grey")
            startmonthMenu_window = canvas.create_window(150,220,window=startmonthMenu)
    
            startDay = list(range(1, 32))
            self.startday = StringVar()
            self.startday.set(startDay[0])
            canvas.create_text(300, 190, text="Day", fill="white")
            startdayMenu = OptionMenu(self, self.startday, *startDay)
            startdayMenu.config(width=15, height=1, bg ="grey")
            startdayMenu_window = canvas.create_window(300,220,window=startdayMenu)
    
            startYear = list(range(2016, 2018))
            self.startyear = StringVar()
            self.startyear.set(startYear[0])
            canvas.create_text(450, 190, text="Year", fill="white")
            startyearMenu = OptionMenu(self, self.startyear, *startYear)
            startyearMenu.config(width=15, height=1, bg ="grey")
            startyearMenu_window = canvas.create_window(450, 220, window=startyearMenu)
    
            # =============================================================================
            # End
            # =============================================================================
            canvas.create_text(50,320, text="End", font=("Franklin Gothic Medium Cond", 20), fill="white")
            
            endMonth = list(range(1, 13))
            self.endmonth = StringVar()
            self.endmonth.set(endMonth[0])
            canvas.create_text(150,290,text="Month", fill="white")
            endmonthMenu = OptionMenu(self, self.endmonth, *endMonth)
            endmonthMenu.config(width=15, height=1, bg ="grey")
            endmonthMenu_window = canvas.create_window(150,320,window=endmonthMenu)
    
            endDay = list(range(1, 32))
            self.endday = StringVar()
            self.endday.set(endDay[0])
            canvas.create_text(300, 290, text="Day", fill="white")
            enddayMenu = OptionMenu(self, self.endday, *endDay)
            enddayMenu.config(width=15, height=1, bg ="grey")
            enddayMenu_window = canvas.create_window(300,320,window=enddayMenu)
    
            endYear = list(range(2016, 2018))
            self.endyear = StringVar()
            self.endyear.set(endYear[0])
            canvas.create_text(450, 290, text="Year", fill="white")
            endyearMenu = OptionMenu(self, self.endyear, *endYear)
            endyearMenu.config(width=15, height=1, bg ="grey")
            endyearMenu_window = canvas.create_window(450, 320, window=endyearMenu)

            # =============================================================================
            # Enter preferences
            # =============================================================================
            canvas.create_text(180, 460, text="2. Enter the preferences for a room:", font=("Franklin Gothic Medium Cond", 20), fill="white")
            self.preferences = StringVar()
            entry_box = Entry(self, textvariable=self.preferences, width=100)
            entrybox_window = canvas.create_window(320, 490, window=entry_box)
            
            currenttime = datetime.datetime.now()
            user_startDate = currenttime.replace(year=int(self.startyear.get()), month=int(self.startmonth.get()),
                                                day=int(self.startday.get()))
            
            currenttime = datetime.datetime.now()
            user_endDate = currenttime.replace(year=int(self.endyear.get()), month=int(self.endmonth.get()),
                                                day=int(self.endday.get()))  
            
            #checkAvailability= available(user_startDate, user_endDate)
            # =============================================================================
            # Confirm button           
            # =============================================================================
            confirmButton = Button(self, text="Confirm", width=25, height=2, bg="lightgreen", command=lambda: master.switch_frame(NextPage))
            confirmButton_window = canvas.create_window(400, 650, window=confirmButton)

    
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
            

            # check date first then EDA_description
            # if listingid not in date, remove motherfuckers
            
            
            

            webButton = tk.Button(self,text="View the listingsID on the map", width=25, height=1, bg="orange",command = self.wbbrowser)
            webButton_window = canvas.create_window(400, 550, window=webButton)
            
            backButton = tk.Button(self, text="Back", width=25, height=2, bg="lightblue",command=lambda: master.switch_frame(StartPage))
            backButton_window = canvas.create_window(400, 650, window=backButton)
            
        def wbbrowser(self):
            webbrowser.open_new_tab('map.html')
                
    if __name__ == "__main__":
        app = SampleApp()
        app.mainloop()
except:
    print ("Please close the excel file!" )        