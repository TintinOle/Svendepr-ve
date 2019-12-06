#=========================================================================================
# IMPORTS
#=========================================================================================
import tkinter as tk
import time
from tkinter import scrolledtext, ttk
from datetime import datetime
from tkinter import Canvas
import time
#import smbus
import time
import threading

class Functions():
  def __init__(self, SP):
    self.sp = SP

  def _quit(self):
    #Function to nicely quit the program
    self.sp.win.quit()
    self.sp.win.destroy()
    exit()

  def get_time(self):
    #Function that gets the date
    global currentdate
    currentdate = ''
    currentnewdate = datetime.now()
    if currentnewdate.day != currentdate:
      currentdate = currentnewdate.day
      self.sp.date.config(text=str(currentnewdate.day)+"/"+str(currentnewdate.month))
    self.sp.date.after(5000, self.get_time)

  def tick(self):
    # this function enables the clock to be updated
    global time1
    time1 = ''
    time2 = time.strftime('%H:%M:%S')
    if time2 != time1:
      time1 = time2
      self.sp.clock.config(text=time2)
    self.sp.clock.after(200, self.tick)

  def add_day(self,selected_recipe,selected_day,language):
    #this function adds the recipe to the selected day in the database
    from Resources import I18N
    self.i18n = I18N(language)
    days = (self.i18n.monday,
            self.i18n.tuesday,
            self.i18n.wednesday,
            self.i18n.thursday,
            self.i18n.friday,
            self.i18n.saturday,
            self.i18n.sunday)
    a = int(days.index(selected_day))

    if (a == 0):
      self.sp.monday_recipe.config(text = selected_recipe)
    if (a == 1):
      self.sp.tuesday_recipe.config(text = selected_recipe)
    if (a == 2):
      self.sp.wednsday_recipe.config(text = selected_recipe)
    if (a == 3):
      self.sp.thursday_recipe.config(text = selected_recipe)
    if (a == 4):
      self.sp.friday_recipe.config(text = selected_recipe)
    if (a == 5):
      self.sp.saturday_recipe.config(text = selected_recipe)
    if (a == 6):
      self.sp.sunday_recipe.config(text = selected_recipe)

  def api_search(self, language):
    # This function calls the mealdb and adds the json object to the recipe database
    import requests
    from Resources import Fonts, I18N
    from PIL import Image, ImageTk

    self.fonts = Fonts()
    self.i18n = I18N(language)

    popup = tk.Toplevel()
    popup.winfo_class()
    popup.resizable(0,0)
    popup.geometry("1050x520+200+200")
    popup.wm_title(self.i18n.recipeAPI)

    label = ttk.Label(popup, text=self.i18n.recipeAPIresult)
    response = requests.get("https://www.themealdb.com/api/json/v1/1/search.php?s="\
                            +str(self.sp.search))
    recipe = response.json()
    recipe_dict = recipe["meals"][0]
    
    frame = ttk.LabelFrame(popup)
    frame.grid(column=0,row=0)
    
    label = ttk.Label(frame)
    label.grid(column=0, row=1)
    label.configure(text = recipe_dict["strMeal"],
                    font = self.fonts.FontHeader2)
    self.recipe_ingredience = []
    self.recipe_measurement = []
    for x in range(1,20):
      if (recipe_dict["strMeasure"+str(x)] == "None" \
        or recipe_dict["strMeasure"+str(x)] == None  \
        or recipe_dict["strMeasure"+str(x)] == ""    \
        or recipe_dict["strMeasure"+str(x)] == " "):
        pass
      else:
        self.recipe_ingredience.append(recipe_dict["strIngredient"+str(x)])
        self.recipe_measurement.append(recipe_dict["strMeasure"+str(x)])
        
    self.recipe_ingredience = list(filter(None, self.recipe_ingredience))
    self.recipe_measurement = list(filter(None, self.recipe_measurement))

    self.recipe_picture = recipe_dict["strMealThumb"]
    self.recipe_instructions = recipe_dict["strInstructions"]


    self.ingrediences = scrolledtext.ScrolledText(frame, width = 40)
    self.ingrediences.grid(column=0,row=2)

    dictst = {self.i18n.ing: self.recipe_ingredience, 
              self.i18n.vol: self.recipe_measurement}
    from pandas import DataFrame as df
    data = df.from_dict(dictst)

    self.ingrediences.insert(tk.END,data)

    self.instructions = scrolledtext.ScrolledText(frame, width = 40)
    self.instructions.grid(column=1,row=2)
    self.instructions.insert(tk.END,self.recipe_instructions)

    # RECIPE PICTURE
    pHeight = 322; pWidth =  322
    import urllib.request
    from os import path
    url = self.recipe_picture
    fDir   = path.dirname(__file__)
    urllib.request.urlretrieve(url, fDir+"/pictures/"+recipe_dict["strMeal"]+".jpg")

    self.canvas = Canvas(frame)
    self.canvas.config(width = pWidth, height = pHeight, highlightthickness =0)
    self.canvas.grid(column=2,row=2,padx=8,pady=4)

    image = Image.open(fDir+"/pictures/"+recipe_dict["strMeal"]+".jpg") \
    .resize((pHeight+10,pWidth+10),Image.ANTIALIAS)
    self.img = ImageTk.PhotoImage(image)
    self.canvas.create_image(0,0,anchor='nw',image=self.img)

    def save_to_db():
      self.sql.insert_recipe(recipename,
                          str(ingrediences), str(measurements),
                          instructions, picture)
      popup.destroy()

    B1 = tk.Button(frame, text=self.i18n.cancel,    command = popup.destroy)
    B1.grid(column=0,row=4)
    B2 = tk.Button(frame, text=self.i18n.addtoDB, command = save_to_db)
    B2.grid(column=0,row = 3)
    B2.config(font = self.fonts.FontHeader2)

    for child in frame.winfo_children():
      child.grid_configure(sticky = "w", padx=8, pady=4)

    from SqLite import SqLite
    self.sql = SqLite()

    recipename = recipe_dict["strMeal"]
    ingrediences = self.recipe_ingredience
    measurements = self.recipe_measurement
    instructions = self.recipe_instructions
    picture = fDir+"/pictures/"+recipe_dict["strMeal"]+".jpg"


    B1.after(1, lambda: B1.focus_force())
    popup.mainloop()

  def getFileName(self):
    from os import path
    from tkinter import filedialog as fd
    fDir = path.dirname(__file__)+"/pictures/"
    fName = fd.askopenfilename(initialdir=fDir)
    return fName
  
  def add_shopping_to_db(self,language, shoppinglist):
    from Resources import Fonts, I18N
    from SqLite import SqLite
    self.sql = SqLite()

    self.fonts = Fonts()
    self.i18n = I18N(language)
    addshopping = tk.Toplevel()
    addshopping.resizable(0,0)
    #addshopping.geometry("550x520+200+200")
    addshopping.wm_title("Add shopping to db")
    
    frame = ttk.LabelFrame(addshopping)
    frame.grid(column=0,row=0)
    
    shoppinglist_frame = ttk.LabelFrame(addshopping)
    shoppinglist_frame.grid(column=0,row=0)

    item_label = ttk.Label(shoppinglist_frame, text = self.i18n.treeName)
    item_label.grid(column=0, row=0)

    volume_label = ttk.Label(shoppinglist_frame, text = self.i18n.treeVolume)
    volume_label.grid(column=1, row=0)

    measurement_label = ttk.Label(shoppinglist_frame, text = self.i18n.treeUnit)
    measurement_label.grid(column=2, row=0)

    expiration_label = ttk.Label(shoppinglist_frame, text = self.i18n.treeExpiration+"\n(DD-MM-YYYY)")
    expiration_label.grid(column=3, row=0)

    volumes = []
    measurements = []
    expirations = []
    for n in shoppinglist:
      item = ttk.Label(shoppinglist_frame, text = str(n), font = self.fonts.FontHeader2)
      item.grid(column = 0, row = shoppinglist.index(n)+1, sticky="w")

      volume = ttk.Entry(shoppinglist_frame, width=20, font = self.fonts.FontHeader2)
      volume.grid(column = 1, row = shoppinglist.index(n)+1, sticky="w")
      volumes.append(volume)

      measurement = ttk.Entry(shoppinglist_frame, width=5, font = self.fonts.FontHeader2)
      measurement.grid(column = 2, row = shoppinglist.index(n)+1, sticky="w")
      measurements.append(measurement)

      expiration = ttk.Entry(shoppinglist_frame, width=10, font = self.fonts.FontHeader2)
      expiration.grid(column = 3, row = shoppinglist.index(n)+1, sticky="w")
      expirations.append(expiration)

    def show_shoppings():
      db_shoppinglist = []

      def check_list():
        #This function checks if every item on shopping list is filled correctly
        #If not, then we can't send to inventory db 
        r = True
        for n in range(0,len(shoppinglist)):
          if volumes[n].get() == "" or volumes[n].get() == "!!":
            volumes[n].delete(0, tk.END)
            volumes[n].insert(0, "!!")
            r = False
          if measurements[n].get() == "" or measurements[n].get() == "!!":
            measurements[n].delete(0, tk.END)
            measurements[n].insert(0, "!!")
            r = False
          if expirations[n].get() == "" or expirations[n].get() == "!!":
            expirations[n].delete(0, tk.END)
            expirations[n].insert(0, "!!")
            r = False
        return r

      test = check_list()
      if test == True:
        for n in range(0,len(shoppinglist)):
          self.sql.add_inventory( shoppinglist[n],
                                  volumes[n].get(),
                                  measurements[n].get(),
                                  expirations[n].get() )

    addbutton = tk.Button(addshopping, text= self.i18n.addshopping, command=show_shoppings)
    addbutton.grid(column=0,row=1)

    addbutton.after(1, lambda: addbutton.focus_force())
    addshopping.mainloop()
    
  def get_temperature(self):
    # Get I2C bus
    bus = smbus.SMBus(1)
    time.sleep(0.3)
    try:
        bus.write_byte(0x40, 0xF3)
    except OSError:
        pass
    time.sleep(0.3)
    # SI7021 address, 0x40 Read data 2 bytes, Temperature
    data0 = bus.read_byte(0x40)
    data1 = bus.read_byte(0x40)
    # Convert the data and output it
    global celsTemp
    celsTemp = ((data0 * 256 + data1) * 175.72 / 65536.0) - 46.85
    
    self.sp.temperature.config(text=str(int(celsTemp)) + "°C")
    self.sp.temperature.after(200, lambda: threading.Thread(target=self.get_temperature, daemon=True).start())
    #print("Temperature in Celsius is : %.2f C" %celsTemp)
  
  def swap_language(self):
    from Resources import I18N
    import configparser
    from tkinter import messagebox as mBox

    config = configparser.ConfigParser()
    config.read('config.ini')
    language = config['language']['language']

    self.i18n = I18N(language)

    if language == "en":
      config['language']['language'] = "da"
    if language == "da":
      config['language']['language'] = "en"
      
    with open('config.ini', 'w') as configfile:
      config.write(configfile)
      
    mBox.showinfo(self.i18n.warning, self.i18n.reloadprogram)