#=========================================================================================
# IMPORTS
#=========================================================================================
import tkinter as tk
from tkinter import Text
from tkinter import ttk
from Resources import I18N, Fonts
from Functions import Functions
from SqLite import SqLite

#-----------------------------------------------------------------------------------------
#  INVENTORY
#-----------------------------------------------------------------------------------------

class tabC():
  def __init__(self, tabControl, win, language):
    # Instantiate the objects
    self.i18n = I18N(language)
    self.functions = Functions(self)
    self.fonts = Fonts()
    self.win = win
    self.sql = SqLite()

    # Creating the tab, adding it to the tabControl
    tabC = ttk.Frame(tabControl)
    tabControl.add(tabC, text=self.i18n.tabC)

    # Creating the labelframe for the tab
    self.myFridge_label = ttk.Label(tabC,text = self.i18n.myFridge, 
                                    font = self.fonts.FontHeader)
    self.myFridge = ttk.LabelFrame(tabC, labelwidget=self.myFridge_label)
    self.myFridge.grid(column=0,row=0)


    # Makeing a treeview for the fridge inventory. 
    tree=ttk.Treeview(self.myFridge, height=40)
    tree.grid(column=0,row=0, rowspan=50, padx=10, columnspan=2)
    tree.config(selectmode='browse')

    tree["columns"]=("one","two","three")
    tree.column("#0", width=200, stretch=False)
    tree.heading("#0",text=self.i18n.treeName,anchor="w")

    tree.column("one", width=50,stretch=False)
    tree.heading("one", text=self.i18n.treeVolume,anchor="w")

    tree.column("two", width=40,stretch=False)
    tree.heading("two", text=self.i18n.treeUnit,anchor="w")

    tree.column("three", width=80, stretch=False)
    tree.heading("three", text=self.i18n.treeExpiration,anchor="w")

    def handle_focus_in(_):
      # Collect what we have in the inventory
      try:
        inventory = self.sql.select_inventory()
        for n in inventory:
          tree.insert("", 0, n[0],text=n[0], values=((n)[1],n[2],n[3]))
      except IndexError:
        pass

    # This function enables the tree to be edited.
    # But this is only for the values, not the name
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

        entryedit = Text(self.myFridge,width=10,height = 1)
        entryedit.config(wrap='none')
        entryedit.place(x = x_pos, y=20+rn*20)
        entryedit.insert(0.0,item_text[cn-1:cn])
        entryedit.focus_force()

        # The new value will be saved when the Return button is pressed
        def saveedit(event):
          newvalue = entryedit.get(0.0,"end").strip()
          tree.set(item, column=column, value=newvalue)
          #set value in db
          name = tree.item(item,"text")
          values = tree.item(item,"values")
          self.sql.update_inventory(name, values[0], values[1], values[2])
          entryedit.destroy()
        entryedit.bind('<Return>',saveedit)
      except UnboundLocalError:
        pass

    def selectItem(event):
      curItem = tree.focus()
      selected_item = tree.item(curItem,"text")

    # Bind the function to a double click on a cell
    tree.bind('<Double-1>',set_cell_value)
    tree.bind('<ButtonRelease-1>', selectItem)

    # This function deletes the desired item from the database and treeview
    def del_from_db():
      try:
        curItem = tree.focus()
        selected_item = tree.item(curItem,"text")
        self.sql.delete_inventory(selected_item)
        tree.delete(selected_item)
      except:
        pass

    # This function adds the item to the database and treeview
    def add_to_db():
      try:
        new_item = entry_name.get(0.0,"end").strip()
        tree.insert("",'end', new_item, text=new_item, values=(0,0,0))
        self.sql.add_inventory(new_item,0,0,0)
      except:
        pass

    tabC.bind("<FocusIn>", handle_focus_in)
    # Label and text box to add or delete item in database.
    entry_label = ttk.Label(self.myFridge, text = self.i18n.addNewItem)
    entry_label.grid(column=2,row=0, sticky="w")

    entry_name = Text(self.myFridge,width=20,height=1)
    entry_name.config(wrap='none')
    entry_name.grid(column=2, row=1, sticky="w")

    add_button = tk.Button(self.myFridge, text = self.i18n.addNewItem, command=add_to_db)
    add_button.grid(column=2, row=2, sticky="w")

    del_button = tk.Button(self.myFridge, text = self.i18n.deleteItem, command=del_from_db)
    del_button.grid(column=2,row=3,sticky="w")

    # Initiate the calnderFrame by providing the tab name and the language.
    from calendarFrame import CalendarFrame
    self.calendar = CalendarFrame(tabC, language)