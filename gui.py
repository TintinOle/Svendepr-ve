#=========================================================================================
# IMPORTS
#=========================================================================================
import tkinter as tk
from tkinter import Menu,ttk
from PIL import Image, ImageTk
from Resources import I18N
from Functions import Functions


class SP():
  def __init__(self):
    import configparser
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    language = config['language']['language']

    # Initiate tkinter and the objects
    self.i18n = I18N(language)
    self.win = tk.Tk()
    self.win.attributes("-fullscreen", True)
    self.win.title(self.i18n.title)
    self.win.resizable(0,0)
    self.win.winfo_class()
    self.functions = Functions(self)
    self.createGUI(language)

  def createGUI(self, language):
    tabControl = ttk.Notebook(self.win)

    s = ttk.Style()

    s.configure('TNotebook.Tab', font=('Times','20','bold') )
    s.configure('TNotebook.Tab', padding=(10,10))

    # Objectify each tab in their own module
    # This Day
    from tabA import tabA
    tabA(tabControl, self.win, language)
    
    # This Week
    from tabB import tabB
    tabB(tabControl, self.win, language)
    
    # Inventory
    from tabC import tabC
    tabC(tabControl, self.win, language)
    
    # Planner
    from tabD import tabD
    tabD(tabControl, self.win, language)
    
    # Add Recipe
    from tabR import tabR
    tabR(tabControl, self.win, language)
    
    # Edit Recipe
    from tabS import tabS
    tabS(tabControl, self.win, language)

    # Pack to make visible
    tabControl.pack(expand=1, fill="both")

    # Adding menu bar to Notebook
    menu_bar = Menu(tabControl)
    self.win.config(menu=menu_bar)
    file_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label=self.i18n.file, menu=file_menu)
    file_menu.add_command(label=self.i18n.swaplanguage, command = self.functions.swap_language)
    file_menu.add_command(label=self.i18n.exit, command=self.functions._quit)


sp = SP()
sp.win.mainloop()