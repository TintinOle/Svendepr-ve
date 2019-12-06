#=========================================================================================
# IMPORTS
#=========================================================================================
import tkinter as tk
from tkinter import ttk
from tkinter import Canvas
from Resources import I18N
from Resources import Fonts
from Functions import Functions
import calendar
from datetime import datetime
import threading

class CalendarFrame():
  def __init__(self, tab, language):
    self.i18n = I18N(language)
    self.functions = Functions(self)
    self.fonts = Fonts()
    self.calendarframe(tab, language)
    
  def calendarframe(self, tab, language):
    # Making the calender frame
    calenderF = Canvas(tab)
    calenderF.grid(column=3, rowspan=10,row=0, padx=100, pady=20, sticky="NE")
    cH = 1000; cW = 600
    calenderF.config(height=cH,width=cW, highlightthickness =0)
    calenderF.create_rectangle(-10,-10,cW+5,cH+5,fill='#c2c0c0')

    # Showing a clock
    self.clock = ttk.Label(calenderF, font = self.fonts.Clock,
                           foreground = 'black',
                           borderwidth=2, relief="groove")
    self.clock.grid(column=0,row=0, padx=100, pady=10, sticky="N")
    # Starting the clock function in a thread
    threading.Thread(self.functions.tick()).start()

    # Showing the date
    self.date = ttk.Label(calenderF, width = 0, font = self.fonts.FontHeader ,
                          borderwidth=2, relief="groove")
    self.date.grid(column =0, row=10,padx=10,pady=10, sticky="N")
    # Starting the time thread
    threading.Thread(self.functions.get_time()).start()

    # Showing the calender
    thisdate = datetime.now()
    calender = ttk.Label(calenderF, width = 20, font = self.fonts.FontHeader,
                         borderwidth=2, relief="groove")
    calender.grid(column =0, row=11,columnspan=2, padx=10,pady=10, sticky="N")

    mycalender = calendar.TextCalendar(calendar.MONDAY)
    calender.config(text=mycalender.formatmonth(thisdate.year, thisdate.month))

    #Showing the timer
    countdown_label = ttk.Label(calenderF, font = self.fonts.FontHeader,
                          borderwidth=2, relief="groove",
                          text=self.i18n.countdown)
    countdown_labelframe = ttk.LabelFrame(calenderF,labelwidget=countdown_label)
    countdown_labelframe.grid(column=0,row=12, sticky="N", pady=10)
    
    countdown_entry_text = ttk.Label(countdown_labelframe, 
                                     text=self.i18n.settimer)
    countdown_entry_text.grid(column=0,row=13,sticky="N", padx=10)
    
    countdown_entry = tk.Spinbox(countdown_labelframe, width=4,
                                 font = self.fonts.FontHeader2,
                                 from_ = 0, to = 320)
    countdown_entry.grid(column=1,row=13,sticky="N")

    def countdown():
      self.remaining = int(countdown_entry.get())*60
      timer()

    def timer():
      import pygame.mixer
      minutes, seconds = divmod(self.remaining, 60)
      if self.remaining <= 0:
        countdown_display.configure(text="time's up!")
        #mBox.showinfo("Time is up!","Timer is done")
        pygame.mixer.init()
        pygame.mixer.music.load("/home/pi/Desktop/Projekt/countdown.mp3")
        pygame.mixer.music.play()
      else:
        countdown_display.configure(text="%d:%d" % (minutes, seconds))
        self.remaining = self.remaining - 1
        self.job = countdown_display.after(1000, timer)

    def stop():
      countdown_display.after_cancel(self.job)

    countdown_button = tk.Button(countdown_labelframe, text=self.i18n.start, 
                                 command=countdown)
    countdown_button.grid(column=2,row=13, sticky="N", padx=10)
    countdown_stop = tk.Button(countdown_labelframe, text=self.i18n.stop, 
                                 command=stop)
    countdown_stop.grid(column=3,row=13, sticky="N", padx=10)

    countdown_display = ttk.Label(countdown_labelframe,font=self.fonts.FontHeader2)
    countdown_display.grid(column=1,row=14, sticky = "WE", columnspan = 4)
    
    #Showing the temperature
    temperature_header = ttk.Label(calenderF, text = "Temperature")
    temperature_display = ttk.LabelFrame(calenderF, labelwidget=temperature_header)
    temperature_display.grid(column=0,row=16,sticky="N")
    
    self.temperature = ttk.Label(temperature_display, font = self.fonts.Clock)
    self.temperature.grid(row=0,column=1, padx=20,pady=1)
    threading.Thread(self.functions.get_temperature(), daemon=True).start()
    