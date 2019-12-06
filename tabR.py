#=========================================================================================
# IMPORTS
#=========================================================================================
import tkinter as tk
from tkinter import scrolledtext, ttk
from tkinter import messagebox as mBox
from tkinter import Canvas
from PIL import Image, ImageTk
from Resources import I18N, Fonts
from Functions import Functions
from SqLite import SqLite

#-----------------------------------------------------------------------------------------
#  ADD RECIPE
#-----------------------------------------------------------------------------------------

class tabR():
  def __init__(self, tabControl, win, language):
    # Instantiate the objects
    self.i18n = I18N(language)
    self.functions = Functions(self)
    self.fonts = Fonts()
    self.win = win
    self.sql = SqLite()

    # Creating the tab, adding it to the tabControl
    tabR = ttk.Frame(tabControl)
    tabControl.add(tabR, text=self.i18n.tabR)

    def handle_focus_in(_):
      self.search_entry.delete(0,tk.END)
      self.search_entry.config(fg='black')

    def handle_focus_out(_):
      self.search_entry.delete(0, tk.END)
      self.search_entry.config(fg='grey')
      self.search_entry.insert(0,self.i18n.searchRecipe)

    # Create the frame for add recipe api
    myAddrecipe_label = ttk.Label(tabR, text=self.i18n.myAddrecipe,
                                  font = self.fonts.FontHeader)
    self.myAddrecipe = ttk.LabelFrame(tabR, labelwidget=myAddrecipe_label)
    self.myAddrecipe.grid(column=0, row=0, pady=10, padx=4)

    # When focus on the tab, format the seach button
    self.myAddrecipe.bind("<FocusIn>", handle_focus_in)
    self.myAddrecipe.bind("<FocusOut>", handle_focus_out)

    # Textbox to search for recipe via API
    self.searchR = ttk.Label(self.myAddrecipe, text=self.i18n.searchRecipeAPI,
                             font = self.fonts.FontHeader2)
    self.searchR.grid(column=0,row=1)

    self.search_entry = tk.Entry(self.myAddrecipe, width=30, 
                                 font = self.fonts.FontHeader2)
    self.search_entry.grid(column=0,row=2,sticky="W")
    self.search_entry.config(fg='grey')
    self.search_entry.insert(0,self.i18n.searchRecipe)

    # Function to call the api, a popup box will be shown
    def get_search():
      import re
      self.search = self.search_entry.get()
      if self.search != self.i18n.searchRecipe:
        self.search = re.sub('[^a-zA-Z.\d\s]', '', self.search)
        if self.search != "":
          self.functions.api_search(language)
        else:
          pass
      else:
        pass

    self.search_button = tk.Button(self.myAddrecipe, text=self.i18n.searchButton,
                                   command=get_search)
    self.search_button.grid(column=1,row=2,sticky="W")

    # Creating a frame for the manual entry of a recipe.
    # This could use some reformatting. A TreeView could be used.
    self.manualAdd = ttk.LabelFrame(tabR, text = self.i18n.addrecipe)
    self.manualAdd.grid(column=0,row = 4,sticky="W")

    # Recipe name entry
    self.manualName_label = ttk.Label(self.manualAdd, text = self.i18n.recipeName+":")
    self.manualName_label.grid(row=0,column=0)
    self.manualName = ttk.Entry(self.manualAdd, width=30)
    self.manualName.grid(column=1,row=0 ,sticky="W")
    self.manualName.after(1, lambda: self.manualName.focus_force())

    # Ingrediences label
    self.manualIng_label = ttk.Label(self.manualAdd, text=self.i18n.ing)
    self.manualIng_label.grid(column=1,row=1)

    # Measurements label
    self.manualMea_label = ttk.Label(self.manualAdd, text=self.i18n.vol)
    self.manualMea_label.grid(column=2,row=1)

    for x in range(1,16):
      self.labels = ttk.Label(self.manualAdd, text = self.i18n.ing+" "+str(x)).grid(row=x+1)

    # Entries for the ingrediences
    ingWidth = 30
    self.manualIng1  = ttk.Entry(self.manualAdd, width=ingWidth)
    self.manualIng1.grid(column=1,row=2 ,sticky="W")
    self.manualIng2  = ttk.Entry(self.manualAdd, width=ingWidth)
    self.manualIng2.grid(column=1,row=3 ,sticky="W")
    self.manualIng3  = ttk.Entry(self.manualAdd, width=ingWidth)
    self.manualIng3.grid(column=1,row=4 ,sticky="W")
    self.manualIng4  = ttk.Entry(self.manualAdd, width=ingWidth)
    self.manualIng4.grid(column=1,row=5 ,sticky="W")
    self.manualIng5  = ttk.Entry(self.manualAdd, width=ingWidth)
    self.manualIng5.grid(column=1,row=6 ,sticky="W")
    self.manualIng6  = ttk.Entry(self.manualAdd, width=ingWidth)
    self.manualIng6.grid(column=1,row=7 ,sticky="W")
    self.manualIng7  = ttk.Entry(self.manualAdd, width=ingWidth)
    self.manualIng7.grid(column=1,row=8 ,sticky="W")
    self.manualIng8  = ttk.Entry(self.manualAdd, width=ingWidth)
    self.manualIng8.grid(column=1,row=9 ,sticky="W")
    self.manualIng9  = ttk.Entry(self.manualAdd, width=ingWidth)
    self.manualIng9.grid(column=1,row=10,sticky="W")
    self.manualIng10 = ttk.Entry(self.manualAdd, width=ingWidth)
    self.manualIng10.grid(column=1,row=11,sticky="W")
    self.manualIng11 = ttk.Entry(self.manualAdd, width=ingWidth)
    self.manualIng11.grid(column=1,row=12,sticky="W")
    self.manualIng12 = ttk.Entry(self.manualAdd, width=ingWidth)
    self.manualIng12.grid(column=1,row=13,sticky="W")
    self.manualIng13 = ttk.Entry(self.manualAdd, width=ingWidth)
    self.manualIng13.grid(column=1,row=14,sticky="W")
    self.manualIng14 = ttk.Entry(self.manualAdd, width=ingWidth)
    self.manualIng14.grid(column=1,row=15,sticky="W")
    self.manualIng15 = ttk.Entry(self.manualAdd, width=ingWidth)
    self.manualIng15.grid(column=1,row=16,sticky="W")

    # Entries for the measurements
    manWidth = 20
    self.manualMea1  = ttk.Entry(self.manualAdd, width=manWidth)
    self.manualMea1.grid(column=2,row=2 ,sticky="W")
    self.manualMea2  = ttk.Entry(self.manualAdd, width=manWidth)
    self.manualMea2.grid(column=2,row=3 ,sticky="W")
    self.manualMea3  = ttk.Entry(self.manualAdd, width=manWidth)
    self.manualMea3.grid(column=2,row=4 ,sticky="W")
    self.manualMea4  = ttk.Entry(self.manualAdd, width=manWidth)
    self.manualMea4.grid(column=2,row=5 ,sticky="W")
    self.manualMea5  = ttk.Entry(self.manualAdd, width=manWidth)
    self.manualMea5.grid(column=2,row=6 ,sticky="W")
    self.manualMea6  = ttk.Entry(self.manualAdd, width=manWidth)
    self.manualMea6.grid(column=2,row=7 ,sticky="W")
    self.manualMea7  = ttk.Entry(self.manualAdd, width=manWidth)
    self.manualMea7.grid(column=2,row=8 ,sticky="W")
    self.manualMea8  = ttk.Entry(self.manualAdd, width=manWidth)
    self.manualMea8.grid(column=2,row=9 ,sticky="W")
    self.manualMea9  = ttk.Entry(self.manualAdd, width=manWidth)
    self.manualMea9.grid(column=2,row=10,sticky="W")
    self.manualMea10 = ttk.Entry(self.manualAdd, width=manWidth)
    self.manualMea10.grid(column=2,row=11,sticky="W")
    self.manualMea11 = ttk.Entry(self.manualAdd, width=manWidth)
    self.manualMea11.grid(column=2,row=12,sticky="W")
    self.manualMea12 = ttk.Entry(self.manualAdd, width=manWidth)
    self.manualMea12.grid(column=2,row=13,sticky="W")
    self.manualMea13 = ttk.Entry(self.manualAdd, width=manWidth)
    self.manualMea13.grid(column=2,row=14,sticky="W")
    self.manualMea14 = ttk.Entry(self.manualAdd, width=manWidth)
    self.manualMea14.grid(column=2,row=15,sticky="W")
    self.manualMea15 = ttk.Entry(self.manualAdd, width=manWidth)
    self.manualMea15.grid(column=2,row=16,sticky="W")

    # Entries for the Instructions
    self.manualRecipe_label = ttk.Label(self.manualAdd, text = self.i18n.addInstructions)
    self.manualRecipe_label.grid(column=4,row=1, sticky="w")
    self.manualRecipe = scrolledtext.ScrolledText(self.manualAdd)
    self.manualRecipe.grid(column=4,row=1,rowspan=20, sticky="N")
    self.manualRecipe.configure(width=40,height=25)

    # Entries for the picture
    # This function opens a dialogbox for the recipe picture
    def browse_file():
      self.recipepic = self.functions.getFileName()
      image = Image.open(self.recipepic).resize((pHeight+10,pWidth+10),Image.ANTIALIAS)
      self.img = ImageTk.PhotoImage(image)
      self.canvas.create_image(0,0,anchor='nw',image=self.img)

    # Picture browse button
    self.pictureButton = tk.Button(self.manualAdd, text = self.i18n.findPicture,
                                   command=browse_file)
    self.pictureButton.grid(row=1,column=5)

    pHeight = 322; pWidth =  322
    self.canvas = Canvas(self.manualAdd)
    self.canvas.config(width = pWidth, height = pHeight, highlightthickness =0)
    self.canvas.grid(column=5,row=1,padx=8,pady=4,rowspan=20)

    for child in self.manualAdd.winfo_children():
      child.grid_configure(sticky = "e", padx=8, pady=4)

    # This function gets the entries of the recipe and adds it to the database
    def add_to_db():
      if self.manualName.get() != "":
        try: 
          # Get a list of ingrediences
          ingrediences = []
          ingrediences.append(self.manualIng1.get())
          ingrediences.append(self.manualIng2.get())
          ingrediences.append(self.manualIng3.get())
          ingrediences.append(self.manualIng4.get())
          ingrediences.append(self.manualIng5.get())
          ingrediences.append(self.manualIng6.get())
          ingrediences.append(self.manualIng7.get())
          ingrediences.append(self.manualIng8.get())
          ingrediences.append(self.manualIng9.get())
          ingrediences.append(self.manualIng10.get())
          ingrediences.append(self.manualIng11.get())
          ingrediences.append(self.manualIng12.get())
          ingrediences.append(self.manualIng13.get())
          ingrediences.append(self.manualIng14.get())
          ingrediences.append(self.manualIng15.get())
          ingrediences = list(filter(None, ingrediences))
          # Get a list of measurements
          measurements = []
          measurements.append(self.manualMea1.get())
          measurements.append(self.manualMea2.get())
          measurements.append(self.manualMea3.get())
          measurements.append(self.manualMea4.get())
          measurements.append(self.manualMea5.get())
          measurements.append(self.manualMea6.get())
          measurements.append(self.manualMea7.get())
          measurements.append(self.manualMea8.get())
          measurements.append(self.manualMea9.get())
          measurements.append(self.manualMea10.get())
          measurements.append(self.manualMea11.get())
          measurements.append(self.manualMea12.get())
          measurements.append(self.manualMea13.get())
          measurements.append(self.manualMea14.get())
          measurements.append(self.manualMea15.get())
          measurements = list(filter(None, measurements))
          # Get the instruction
          instructions = self.manualRecipe.get("1.0", tk.END)
          # Get the picture location
          picture = self.recipepic
          # Insert into database
          recipename = self.manualName.get()
          
          if len(ingrediences) == len(measurements):
            self.sql.insert_recipe(recipename,
                                   str(ingrediences), str(measurements),
                                   instructions, picture)
          else:
            mBox.showinfo(self.i18n.warning,self.i18n.checktext)
        except AttributeError:
          mBox.showinfo(self.i18n.warning,self.i18n.pictureWarning)
      else: 
        mBox.showinfo(self.i18n.warning,self.i18n.recipeWarning)

    self.addToDB = tk.Button(self.manualAdd, text = self.i18n.addtoDB,
                             font = self.fonts.FontHeader2,
                             command = add_to_db)
    self.addToDB.grid(row = 17, column=0, sticky="W", padx=10, pady=20)
    
    # Add some padding to all items
    for child in self.myAddrecipe.winfo_children():
      child.grid_configure(sticky = "w", padx=8, pady=4)
