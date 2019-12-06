#=========================================================================================
# IMPORTS
#=========================================================================================
import tkinter as tk
from tkinter import OptionMenu, StringVar, scrolledtext, ttk
from tkinter import Canvas
from PIL import Image, ImageTk
from Resources import I18N, Fonts
from Functions import Functions
from SqLite import SqLite

#-----------------------------------------------------------------------------------------
#  PLANNER
#-----------------------------------------------------------------------------------------

class tabD():
  def __init__(self, tabControl, win, language):
    # Instantiate the objects
    self.i18n = I18N(language)
    self.fonts = Fonts()
    self.functions = Functions(self)
    self.win = win
    self.sql = SqLite()

    # Creating the tab, adding it to the tabControl
    tabD = ttk.Frame(tabControl)
    tabControl.add(tabD, text=self.i18n.tabD)

    # Creating labelframes for the tab
    myPlanner_label = ttk.Label(text=self.i18n.myPlanner, font = self.fonts.FontHeader)
    self.myPlanner = ttk.LabelFrame(tabD, labelwidget=myPlanner_label)
    self.myPlanner.grid(column=0, row=0, pady=10)

    self.search_label = ttk.Label(text = self.i18n.search, font=self.fonts.FontHeader2)
    self.search = ttk.LabelFrame(self.myPlanner, labelwidget=self.search_label)
    self.search.grid(column=0,row=1, sticky = "W")

    def handle_focus_in(_):
      recipies = self.sql.select_recipes()
      try:
        self.selectDay = OptionMenu(self.search, self.recipe_list, *recipies)
        self.selectDay.grid(column=0, row=2, sticky ="W", padx=8,pady=4)
      except:
        pass

    # Get a list of recipes from the db
    recipies = self.sql.select_recipes()
    tabD.bind("<FocusIn>", handle_focus_in)

    # Searchbox
    self.recipe_list = StringVar(self.win)
    # On change dropdown value
    def change_dropdown(*args):
      self.recipe_list.get()
      recipies = self.sql.select_recipes()

    # link function to change dropdown
    self.recipe_list.trace('w', change_dropdown)
    self.recipe_list.set(self.i18n.selectrecipe)

    # This function formats the "JSON" recipe and shows the data
    def show_selected_recipe():
      try:
        selected_recipe_list = self.sql.show_recipe(self.recipe_list.get())
        selected_recipe_list = selected_recipe_list[0]
        RecipeName = selected_recipe_list[1]
        RecipeInstructions = selected_recipe_list[2]
        RecipePicture = selected_recipe_list[3]
        RecipeIngrediences = selected_recipe_list[4]
        RecipeMeasurements = selected_recipe_list[5]
        self.RecipeServings = selected_recipe_list[6]
  
        # The ast import is used to change a string formattet as a list to a list.
        import ast
        import re
        RecipeIngrediences = ast.literal_eval(RecipeIngrediences)
        RecipeMeasurements = ast.literal_eval(RecipeMeasurements)
  
        # The recipe ingrediences needs to be formattet into two lists, one for the volumes,
        # and one for the measurements. This is because the api for the recipes has strange 
        # formats.
        vol = []; mea = []
        # Going through the list of measurements checking for a number, else append 1
        for x in range(0,len(RecipeIngrediences)):
          try: 
            x = re.search("\d*\.\d+|\d+", RecipeMeasurements[x])
            vol.append(x.group())
          except:
            vol.append(1)
  
        # Going through the list of measurements for g,kg,oz..
        for x in range(0,len(RecipeMeasurements)):
          try:
            y = re.search("[a-zA-Z ]+", RecipeMeasurements[x])
            mea.append(y.group())
          except:
            pass
  
        # Setup the canvas for the image
        image = Image.open(RecipePicture) \
        .resize((pHeight+10,pWidth+10),Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(image)
        self.canvas.create_image(0,0,anchor='nw',image=self.img)
  
        self.RecipeMeasurements = [x.strip(' ') for x in RecipeMeasurements]
        self.RecipeMeasurements = list(filter(None, RecipeMeasurements))
        list_dict = list(zip(vol,mea))
        self.dict = dict(zip(RecipeIngrediences, list_dict))
        #print(self.diict)
  
        # Pandas creates a two dimentional datastructure.
        from pandas import DataFrame as df
        data = df.from_dict(self.dict, orient='index', 
                            columns = [self.i18n.number, self.i18n.value])
        self.myIngrediences.delete('1.0',tk.END)
        self.myIngrediences.insert(tk.END, data)
  
        self.myRecipe.delete('1.0',tk.END)
        self.myRecipe.insert(tk.END, RecipeInstructions)
        self.recipe_name.config(text = self.i18n.recipeName + ": " + RecipeName)
      except:
        pass

    self.search_button = tk.Button(self.search, text=self.i18n.search,
                                    command=show_selected_recipe)
    self.search_button.grid(column=1, row=2, sticky='W', padx=8,pady=4)

    # Label for the recipe name
    self.recipe_name = ttk.Label(self.myPlanner, font = self.fonts.FontHeader)
    self.recipe_name.grid(column = 0, row = 5,padx=8,pady=4, sticky = "W")

    # Ingrediences
    self.myIngrediences_label = ttk.Label(self.myPlanner, text=self.i18n.ingrediences,
                                          font=self.fonts.FontHeader2)
    self.myIngrediences_label.grid(column=0, row=6,sticky="NW",padx=8)
    self.myIngrediences = scrolledtext.ScrolledText(self.myPlanner,
                                                    width=60, height=20,
                                                    wrap=tk.WORD)
    self.myIngrediences.grid(column=0, row=7, padx=8, pady=4, sticky= "W")

    # Recipe
    self.recipe_label = ttk.Label(self.myPlanner, text=self.i18n.recipe,
                                  font=self.fonts.FontHeader2)
    self.recipe_label.grid(column=1, row=6, sticky="NW", padx=8)
    self.myRecipe = scrolledtext.ScrolledText(self.myPlanner,
                                              width=60, height=20,
                                              wrap=tk.WORD)
    self.myRecipe.grid(column=1, row=7, sticky="NW",padx=8, pady=4)

    # Recipe picture
    pHeight = 322; pWidth =  322
    self.recipepic_label = ttk.Label(self.myPlanner, text=self.i18n.recipePicture,
                                     font=self.fonts.FontHeader2)
    self.pictureFrame = ttk.LabelFrame(self.myPlanner, labelwidget=self.recipepic_label)
    self.pictureFrame.grid(column=3, row=6, sticky="NW", rowspan=10)
    self.canvas = Canvas(self.pictureFrame)
    self.canvas.config(width = pWidth, height = pHeight, highlightthickness =0)
    self.canvas.grid(column=0,row=0,padx=8,pady=4)

    # Dropdown menu
    self.add_recipe = ttk.Label(self.myPlanner, text = self.i18n.addrecipe,
                                font = self.fonts.FontHeader2)
    self.addRecipes = ttk.LabelFrame(self.myPlanner, labelwidget=self.add_recipe)
    self.addRecipes.grid(column=0,row=8, sticky = "w", columnspan=5)

    self.tkvar = StringVar(self.win)
    self.tkvar.set(self.i18n.selectDay)

    # on change dropdown value
    def change_dropdown(*args):
      self.tkvar.get()

    # link function to change dropdown
    self.tkvar.trace('w', change_dropdown)

    # Dictionary with options
    choices = (self.i18n.monday,
               self.i18n.tuesday,
               self.i18n.wednesday,
               self.i18n.thursday,
               self.i18n.friday,
               self.i18n.saturday,
               self.i18n.sunday)

    # Get planned recipe
    self.plan = self.sql.get_planned_meals()

    self.selectDay = OptionMenu(self.addRecipes, self.tkvar, *choices)
    self.selectDay.grid(column=0, row=0, padx=8,pady=4, sticky ="W")

    # This function adds the recipe to the selected day
    def add_recipe_function():
      selected_recipe = self.recipe_list.get()
      selected_day = self.tkvar.get()

      #print(selected_day,selected_recipe)
      self.functions.add_day(selected_recipe, selected_day, language)
      self.sql.add_recipe_to_meal_plan(selected_recipe,selected_day)

    # This function removes the recipe for the selected day
    def remove_recipe_function():
      selected_day = self.tkvar.get()
      self.functions.add_day("None",selected_day,language)
      self.sql.add_recipe_to_meal_plan("None",selected_day)

    # Add and delete button
    self.addButton = tk.Button(self.addRecipes, text = self.i18n.add,
                               command=add_recipe_function)
    self.addButton.grid(column=1,row=0)

    self.delButton = tk.Button(self.addRecipes, text = self.i18n.remove,
                               command=remove_recipe_function)
    self.delButton.grid(column=2,row=0)

    # Labelframe for the planned recipes
    # This could be reworked to create the labels in a loop
    self.recipe_overview = tk.LabelFrame(self.addRecipes)
    self.recipe_overview.grid(column=0,row=1, padx=8,pady=4, columnspan = 30, sticky="W")

    for x in range(len(choices)):
      self.test = ttk.Label(self.recipe_overview, text = choices[x],
                            font=self.fonts.FontHeader)
      self.test.grid(column=x, row = 1, padx=49, pady=4, sticky="W")

    word_len = 200
    self.monday_recipe = ttk.Label(self.recipe_overview, text = self.plan[0],
                           font=self.fonts.FontHeader2, wraplength=word_len)
    self.monday_recipe.grid(column=0,row=4)

    self.tuesday_recipe = ttk.Label(self.recipe_overview, text = self.plan[1],
                           font=self.fonts.FontHeader2, wraplength=word_len)
    self.tuesday_recipe.grid(column=1,row=4)

    self.wednsday_recipe = ttk.Label(self.recipe_overview, text = self.plan[2],
                           font=self.fonts.FontHeader2, wraplength=word_len)
    self.wednsday_recipe.grid(column=2,row=4)

    self.thursday_recipe = ttk.Label(self.recipe_overview, text = self.plan[3],
                           font=self.fonts.FontHeader2, wraplength=word_len)
    self.thursday_recipe.grid(column=3,row=4)

    self.friday_recipe = ttk.Label(self.recipe_overview, text = self.plan[4],
                                   font=self.fonts.FontHeader2, wraplength=word_len)
    self.friday_recipe.grid(column=4,row=4)

    self.saturday_recipe = ttk.Label(self.recipe_overview, text = self.plan[5],
                                     font=self.fonts.FontHeader2, wraplength=word_len)
    self.saturday_recipe .grid(column=5,row=4)

    self.sunday_recipe = ttk.Label(self.recipe_overview, text = self.plan[6],
                                   font=self.fonts.FontHeader2,wraplength=word_len)
    self.sunday_recipe.grid(column=6,row=4)