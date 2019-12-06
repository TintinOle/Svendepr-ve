#=========================================================================================
# IMPORTS
#=========================================================================================
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from Resources import I18N
from Resources import Fonts
from Functions import Functions
from SqLite import SqLite

#-----------------------------------------------------------------------------------------
#  THIS WEEK
#-----------------------------------------------------------------------------------------

class tabB():
  def __init__(self, tabControl, win, language):
    # Instantiate the objects
    self.i18n = I18N(language)
    self.functions = Functions(self)
    self.fonts = Fonts()
    self.win = win
    self.sql = SqLite()

    # Creating the tab, adding it to the tabControl
    tabB = ttk.Frame(tabControl)
    tabControl.add(tabB, text=self.i18n.tabB)

    # Creating the labelframe for the tab
    myWeek_label = ttk.Label(text=self.i18n.myWeek, font = self.fonts.FontHeader)
    self.myWeek = ttk.LabelFrame(tabB, labelwidget=myWeek_label)
    self.myWeek.grid(column=0, row=0, pady=10)

    # This function collect the planned meals from the db when the tab gets focus
    # We also populate the textboxes with the data.
    def handle_focus_in(_):
      self.planned_meals = self.sql.get_planned_meals()
      self.planned_meals = [f'{e}' for e in self.planned_meals]
      for child in self.myWeek.winfo_children():
        if isinstance(child, tk.Text):
          child.config(state="normal")
          child.delete('1.0', tk.END)
          child.insert('1.0', self.planned_meals[0])
          self.planned_meals.pop(0)

    tabB.bind("<FocusIn>", handle_focus_in)

    # Setup the label and textbox for the planned week
    # This could be refactored later. 
    self.monday = ttk.Label(self.myWeek, text = self.i18n.monday,
                            font = self.fonts.FontHeader2)
    self.monday.grid(column=0, row=2)
    self.monday_recipe = tk.Text(self.myWeek, height=1, width=50)
    self.monday_recipe.grid(row = 3)


    self.tuesday = ttk.Label(self.myWeek, text = self.i18n.tuesday,
                             font = self.fonts.FontHeader2)
    self.tuesday.grid(column=0, row=4)
    self.tuesday_recipe = tk.Text(self.myWeek, height=1, width=50)
    self.tuesday_recipe.grid(row = 5)


    self.wednsday = ttk.Label(self.myWeek, text = self.i18n.wednesday,
                              font = self.fonts.FontHeader2)
    self.wednsday.grid(column=0, row=6)
    self.wednsday_recipe = tk.Text(self.myWeek, height=1, width=50)
    self.wednsday_recipe.grid(row = 7)


    self.thursday = ttk.Label(self.myWeek, text = self.i18n.thursday,
                              font = self.fonts.FontHeader2)
    self.thursday.grid(column=0, row=8)
    self.thursday_recipe = tk.Text(self.myWeek, height=1, width=50)
    self.thursday_recipe.grid(row = 9)


    self.friday = ttk.Label(self.myWeek, text = self.i18n.friday,
                            font = self.fonts.FontHeader2)
    self.friday.grid(column=0, row=10)
    self.friday_recipe = tk.Text(self.myWeek, height=1, width=50)
    self.friday_recipe.grid(row = 11)


    self.saturday = ttk.Label(self.myWeek, text = self.i18n.saturday,
                              font = self.fonts.FontHeader2)
    self.saturday.grid(column=0, row=12)
    self.saturday_recipe = tk.Text(self.myWeek, height=1, width=50)
    self.saturday_recipe.grid(row = 13)


    self.sunday = ttk.Label(self.myWeek, text = self.i18n.sunday,
                            font = self.fonts.FontHeader2)
    self.sunday.grid(column=0, row=14)
    self.sunday_recipe = tk.Text(self.myWeek, height=1, width=50)
    self.sunday_recipe.grid(row = 15)


    for child in self.myWeek.winfo_children():
      child.grid_configure(sticky = "W", padx=8, pady=4)
      child.config(state="disabled")

    from calendarFrame import CalendarFrame
    self.calendar = CalendarFrame(tabB, language)
