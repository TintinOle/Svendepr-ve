#=========================================================================================
# IMPORTS
#=========================================================================================
import tkinter as tk
from tkinter import scrolledtext, ttk
from tkinter import messagebox as mBox
from tkinter import Canvas
from PIL import Image, ImageTk
from os import path
from Resources import I18N
from Resources import Fonts
from Functions import Functions
from datetime import datetime
from SqLite import SqLite

#-----------------------------------------------------------------------------------------
#  THIS DAY
#-----------------------------------------------------------------------------------------

class tabA():
  def __init__(self, tabControl, win, language):
    # Instantiate the objects
    self.i18n = I18N(language)
    self.functions = Functions(self)
    self.fonts = Fonts()
    self.win = win
    self.sql = SqLite()

    # Creating the tab, adding it to the tabControl
    tabA = ttk.Frame(tabControl)
    tabControl.add(tabA, text=self.i18n.tabA)

    # Creating the labelframe for the tab
    myDay_label = ttk.Label(text=self.i18n.myDay, font = self.fonts.FontHeader)
    self.myDay = ttk.LabelFrame(tabA, labelwidget=myDay_label)
    self.myDay.grid(column=0, row=0, pady=10)

    # This function is run when tabA is in focus. 
    # It collects the planned recipe for the current day, if any exists.
    # Else we do nothing.
    def handle_focus_in(_):
      self.recipename = self.sql.get_planned_meal(datetime.today().strftime('%A'))[0][0]
      try:
        self.recipe = self.sql.show_recipe(self.recipename)[0]
        self.recipeinstructions = self.recipe[2]
        self.recipepicture = self.recipe[3]
        self.recipeingrediences = self.recipe[4]
        self.recipemeasurements = self.recipe[5]

        if self.recipename != "None":
          show_recipe(self.recipename, self.recipe,
            self.recipeinstructions, self.recipepicture,
            self.recipeingrediences, self.recipemeasurements)
        if self.recipename == "None":
          self.ingredienceT.delete('1.0',tk.END)
          self.recipeT.delete('1.0',tk.END)
          myDay_label.config(text = self.i18n.myDay+": ")
          self.canvas.delete('all')
      except:
        pass

    tabA.bind("<FocusIn>", handle_focus_in)

    # This function formats the "JSON" recipe and shows the data
    def show_recipe(recipename, recipe, recipeinstructions, recipepicture, recipeingrediences, recipemeasurements):
      # The ast import is used to change a string formattet as a list to a list.
      import ast
      import re
      self.recipeingrediences = ast.literal_eval(self.recipeingrediences)
      self.recipemeasurements = ast.literal_eval(self.recipemeasurements)

      # The recipe ingrediences needs to be formattet into two lists, one for the volumes,
      # and one for the measurements. This is because the api for the recipes has strange 
      # formats.
      vol = []; mea = []
      # Going through the list of measurements checking for a number, else append 1
      for x in range(0,len(self.recipeingrediences)):
        try: 
          x = re.search("\d*\.\d+|\d+", self.recipemeasurements[x])
          vol.append(x.group())
        except:
          vol.append(1)
      # Going through the list of measurements for g,kg,oz..
      for x in range(0,len(self.recipemeasurements)):
        try:
          y = re.search("[a-zA-Z ]+", self.recipemeasurements[x])
          mea.append(y.group())
        except:
          pass

      # Setup the canvas for the image
      pHeight = 340; pWidth =  340
      image = Image.open(self.recipepicture) \
      .resize((pHeight+10,pWidth+10),Image.ANTIALIAS)
      self.img = ImageTk.PhotoImage(image)
      self.canvas.create_image(0,0,anchor='nw',image=self.img)

      # Create a dictionary for the volumes and measurements
      list_dict = list(zip(vol,mea))
      self.dict = dict(zip(self.recipeingrediences, list_dict))
      #print(self.diict)

      # Pandas creates a two dimentional datastructure.
      from pandas import DataFrame as df
      data = df.from_dict(self.dict, orient='index',
                          columns = [self.i18n.number, self.i18n.value])
      #Insert the data in the ingredienceT scrolled text
      self.ingredienceT.delete('1.0',tk.END)
      self.ingredienceT.insert(tk.END, data)

      #Insert the recipe instructions into recipeT scrolled text
      self.recipeT.delete('1.0',tk.END)
      self.recipeT.insert(tk.END, self.recipeinstructions)
      myDay_label.config(text = self.i18n.myDay+": "+self.recipename)

    # Making the Ingrediences textbox, first with a labelframe
    ingredienceF_label = ttk.Label(text=self.i18n.ingrediences,
                                   font = self.fonts.FontHeader2)
    ingredienceF = ttk.LabelFrame(self.myDay, labelwidget = ingredienceF_label)
    ingredienceF.grid(column=0, row=1, padx=10, sticky="NW")

    # The ingredienceT contains the ingrediences
    self.ingredienceT = scrolledtext.ScrolledText(ingredienceF,
                                                  width=60, height=20, wrap=tk.WORD)
    self.ingredienceT.grid(column=0, row=1, sticky="NW")

    # Making the recipe textbox
    recipeF_label = ttk.Label(text=self.i18n.recipe, font = self.fonts.FontHeader2)
    self.recipeF = ttk.LabelFrame(self.myDay, labelwidget=recipeF_label)
    self.recipeF.grid(column=0, row=2, padx=10, sticky="NW")

    # The recipeT contains the instructions
    self.recipeT = scrolledtext.ScrolledText(self.recipeF, width=60, height=20, wrap=tk.WORD)
    self.recipeT.grid(column=0, row=1, sticky="NW")

    # Making the Recipe picture canvas
    pHeight = 340; pWidth =  340
    label = ttk.Label(text=self.i18n.recipePicture, font = self.fonts.FontHeader2)
    self.pictureFrame = ttk.LabelFrame(self.myDay,labelwidget=label)
    self.pictureFrame.grid(column=1, row=1, padx=8, pady=4, sticky="NW",rowspan=10)
    self.canvas = Canvas(self.pictureFrame)
    self.canvas.config( width = pWidth, height = pHeight, highlightthickness =0)
    self.canvas.grid(column=0,row=0)

    # Show the recipe for the day, this is only used when the program is initiated
    try:
      self.recipename = self.sql.get_planned_meal(datetime.today().strftime('%A'))[0][0]
      self.recipe = self.sql.show_recipe(self.recipename)[0]
      self.recipeinstructions = self.recipe[2]
      self.recipepicture = self.recipe[3]
      self.recipeingrediences = self.recipe[4]
      self.recipemeasurements = self.recipe[5]
      show_recipe(self.recipename, self.recipe,
                  self.recipeinstructions, self.recipepicture,
                  self.recipeingrediences, self.recipemeasurements)
    except:
      pass

    # This function sends the shopping list to the user.
    # Right now, it only shows a message box, but could be improved with an email or other.
    def send_shopping_list():
      shoppinglist=[]
      try:
        for i in range(0,len(self.recipeingrediences)):
          shoppinglist.append(self.recipeingrediences[i]+" "+self.recipemeasurements[i])
        message = "\n".join(shoppinglist)
        mBox.showinfo(self.i18n.shoppinglist,
                      message)
      except:
        mBox.showinfo(self.i18n.shoppinglist,
                      self.i18n.emptymessage)
      #print(*shoppinglist, sep='\n')
    
    # This function opens a dialog box to help the user add shoppings to the inventory.
    def add_shopping_to_db():
      #self.sql.add_inventory("Pasta","1000","g","")
      try:
        self.functions.add_shopping_to_db(language,self.recipeingrediences)
      except:
        mBox.showinfo(self.i18n.shoppinglist,
                      self.i18n.emptymessage)

    # Button to send the shopping list
    self.send_shopping_list_button = tk.Button(self.myDay,text=self.i18n.sendshopping,
                                               command=send_shopping_list)
    self.send_shopping_list_button.grid(column=0, row=3, sticky="W", padx=8, pady=4)

    # Button to add the shopping to the db
    self.add_shopping_to_db_button = tk.Button(self.myDay, text= self.i18n.addshopping,
                                               command=add_shopping_to_db)
    self.add_shopping_to_db_button.grid(column=0, row=4, sticky="W", padx=8, pady=4)

    # Initiate the calnderFrame by providing the tab name and the language.
    from calendarFrame import CalendarFrame
    self.calendar = CalendarFrame(self.myDay, language)