#=========================================================================================
# IMPORTS
#=========================================================================================
import tkinter as tk
from tkinter import OptionMenu, StringVar, Text, scrolledtext, ttk
from tkinter import Canvas
from PIL import Image, ImageTk
from Resources import I18N, Fonts
from Functions import Functions
from SqLite import SqLite

#-----------------------------------------------------------------------------------------
#  EDIT RECIPE
#-----------------------------------------------------------------------------------------

class tabS():
  def __init__(self, tabControl, win, language):
    # Instantiate the objects
    self.i18n = I18N(language)
    self.functions = Functions(self)
    self.fonts = Fonts()
    self.win = win
    self.sql = SqLite()

    # Creating the tab, adding it to the tabControl
    tabS = ttk.Frame(tabControl)
    tabControl.add(tabS, text=self.i18n.tabS)

    # Create the recpie_name for the dropdown menu
    self.recipe_name = StringVar(self.win)
    self.recipe_name.set(self.i18n.selectrecipe)

    def handle_focus_in(_):
      recipe_list = self.sql.select_recipes()

      # DROPDOWN MENU ADD
      select_recipe = OptionMenu(recipe_list_frame, self.recipe_name, *recipe_list)
      select_recipe.grid(column=0, row=0, padx=8,pady=4, sticky ="W")

      # on change dropdown value
      def change_dropdown(*args):
        self.recipe_name.get()
        recipe_list = self.sql.select_recipes()

      # link function to change dropdown
      self.recipe_name.trace('w', change_dropdown)

    def get_recipe_name():
      self.selected_recipe = self.recipe_name.get()
      show_selected_recipe(self.selected_recipe)

    def show_selected_recipe(recipe_name):
      #Create treeview for recipe
      import ast
      import re
      recipe = self.sql.show_recipe(recipe_name)
      recipe_ingredient_name = ast.literal_eval(recipe[0][4])
      recipe_ingredient_vol = ast.literal_eval(recipe[0][5])

      # The recipe ingrediences needs to be formattet into two lists, one for the volumes,
      # and one for the measurements. This is because the api for the recipes has strange 
      # formats.
      vol = []; mea = []
      # Going through the list of measurements checking for a number, else append 1
      for x in range(0,len(recipe_ingredient_vol)):
        try: 
          a = re.search("\d*\.\d+|\d+", recipe_ingredient_vol[x])
          a = a.group()
          vol.append(a)
        except AttributeError:
          a = 1
          vol.append(a)
        try:
          b = re.search("[a-zA-Z ]+", recipe_ingredient_vol[x])
          b = b.group()
          mea.append(b)
        except:
          b = "stk"
          mea.append(b)

      # Create a treeview for the recipe ingrediences
      tree=ttk.Treeview(recipe_list_frame, height=15)
      tree.grid(column=0,row=1, rowspan=30, columnspan=3, padx=10, sticky="n")
      tree.config(selectmode='browse')

      # Setup treeframe columns
      tree["columns"]=("one","two")
      tree.column("#0", width=200, stretch=False)
      tree.heading("#0",text=self.i18n.treeName,anchor="w")

      tree.column("one", width=50,stretch=False)
      tree.heading("one", text=self.i18n.treeVolume,anchor="w")

      tree.column("two", width=150,stretch=False)
      tree.heading("two", text=self.i18n.treeUnit,anchor="w")

      # Insert data into treeframe
      for n in range(0,len(recipe_ingredient_name)):
        tree.insert("", 0, n, text= recipe_ingredient_name[n],\
                    values = (vol[n],mea[n]))

      # Enable treeview to be edited
      def set_cell_value(event): # Double click to enter the edit state
        try: 
          for item in tree.selection():
            item_text = tree.item(item, "values")
            #print(item_text[0:2]) # Output the value of the selected row
            column= tree.identify_column(event.x)# column
            row = tree.identify_row(event.y) #row
          #Placing the textbox
          cn = int(str(column).replace('#',''))
          rn = tree.index(tree.selection())
          if cn == 1:
            x_pos = 200
          if cn == 2:
            x_pos = 250
          if cn == 3:
            x_pos = 290

          entryedit = Text(recipe_list_frame,width=10,height = 1)
          entryedit.config(wrap='none')
          entryedit.place(x = x_pos, y=65+rn*20)
          entryedit.insert(0.0,item_text[cn-1:cn])
          entryedit.focus_force()

          # The new value will be saved when the Return button is pressed
          def saveedit(event):
            newvalue = entryedit.get(0.0,"end").strip()
            tree.set(item, column=column, value=newvalue)
            #set value in db
            names = tree.get_children()
            
            #Build list to be sent to db
            ingrediences = []
            for n in names:
              values = tree.item(n,"values")
              ingrediences.append(values[0]+" "+values[1])

            #Update the recipe measurements in db
            self.sql.update_recipe_measurement(recipe_name, ingrediences)
            entryedit.destroy()
          entryedit.bind('<Return>',saveedit)
        except UnboundLocalError:
          pass

      recipe_instructions = scrolledtext.ScrolledText(recipe_list_frame, 
                                                      width=60,height=20, wrap=tk.WORD)
      recipe_instructions.grid(column=4,row=1)
      recipe_instructions.delete('1.0',tk.END)
      recipe_instructions.insert(tk.END, recipe[0][2])

      def save_instructions():
        instructions = recipe_instructions.get(0.0,tk.END)
        self.sql.update_recipe_instructions(recipe_name, instructions)

      recipe_instructions_save = tk.Button(recipe_list_frame, text = self.i18n.save,
                                           command=save_instructions)
      recipe_instructions_save.grid(column=4,row=0, sticky="w")

      def browse_file():
        pHeight = 322; pWidth =  322
        self.recipepic = self.functions.getFileName()
        image = Image.open(self.recipepic).resize((pHeight+10,pWidth+10),Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(image)
        canvas.create_image(0,0,anchor='nw',image=self.img)

      def save_picture():
        try:
          self.sql.update_recipe_picture(recipe_name,self.recipepic)
        except AttributeError:
          pass

      #Browse to a new picture
      browse_new_pic = tk.Button(recipe_list_frame, text = self.i18n.findPicture,
                                 command = browse_file)
      browse_new_pic.grid(column=5,row=0, sticky="w")
      save_new_pic   = tk.Button(recipe_list_frame, text = self.i18n.savePic,
                                 command = save_picture)
      save_new_pic.grid(column=6,row=0, sticky="e")

      pHeight = 322; pWidth =  322
      canvas = Canvas(recipe_list_frame)
      canvas.config(width = pWidth, height = pHeight, highlightthickness =0)
      canvas.grid(column=5,row=1,columnspan=2)

      image = Image.open(recipe[0][3]) \
      .resize((pWidth+10,pHeight+10),Image.ANTIALIAS)
      self.img = ImageTk.PhotoImage(image)
      canvas.create_image(0,0,anchor='nw',image=self.img)

      tree.bind('<Double-1>',set_cell_value)


    recipe_list_label = ttk.Label(tabS, text = self.i18n.tabS,
                                  font = self.fonts.FontHeader2)
    recipe_list_frame = ttk.LabelFrame(tabS, labelwidget=recipe_list_label)
    recipe_list_frame.grid(column=0,row=0, sticky = "w", columnspan=5)

    get_recipe_button = tk.Button(recipe_list_frame, text=self.i18n.search,
                                  command=get_recipe_name)
    get_recipe_button.grid(column=1, row=0, sticky='W', padx=8,pady=4)

    tabS.bind("<FocusIn>", handle_focus_in)