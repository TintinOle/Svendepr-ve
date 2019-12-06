#=========================================================================================
# IMPORTS
#=========================================================================================
import sqlite3
import re
from pprint import pprint
from sqlite3 import Error

class SqLite():
  def __init__(self):
    self.conn, self.cursor = self.connect()
    #self.showconn()
    self.create_recipe_table()
    self.create_mealplan_table()
    self.create_inventory_table()

  def connect(self):
    # Connect to the database
    from os import path
    from tkinter import filedialog as fd
    fDir = path.dirname(__file__)+"/database/"
    conn = sqlite3.connect(fDir+"/GUI.db")
    cursor = conn.cursor()
    return conn, cursor

  def showconn(self):
    # Print statement to show the connection. Used in debugging
    print(self.conn)

  def close(self):
    # Close connection to the database
    self.cursor.close()
    self.conn.close()

  def create_mealplan_table(self):
    # Creating the table for the mealplan
    try :
      # Creating the books table,
      self.cursor.execute("Create table Mealplan ( \
        Meal_Day varchar(300),                     \
        Recipe_Name varchar(1000)                  \
      )")
    except Error as e:
      if ( re.match("table \w+ already exists", str(e)) is not None ):
        pass
      else:
        print(e)

    days = ["Monday", "Tuesday","Wednsday","Thursday","Friday","Saturday","Sunday"]
    for x in range(0,(len(days))):
      self.cursor.execute("INSERT INTO Mealplan (Meal_Day) VALUES (?)",(days[x],))
      self.conn.commit()

  def create_recipe_table(self):
    # Create the table for the recipes. Recipe_ID is not nessesary, only for debug
    try :
      self.cursor.execute("Create table Recipe (                \
        Recipe_ID INTEGER not null PRIMARY KEY autoincrement,   \
        Recipe_Name varchar(300) not null,                      \
        Recipe_Instructions varchar(1000) not null,             \
        Recipe_Picture varchar(300) not null,                   \
        Recipe_Ingrediences varchar(5000) not null,             \
        Recipe_Measurement varchar(5000) not null,              \
        Recipe_Servings int,                                    \
        Recipe_Language varchar(5)                              \
      )")
    except Error as e:
      if ( re.match("table \w+ already exists", str(e)) is not None ):
        pass
      else:
        print(e)

  def create_inventory_table(self):
    # Create the invenyory table
    try :
      self.cursor.execute("Create table Inventory (   \
        Inventory_Name varchar(500),                  \
        Inventory_Volume varchar(300) not null,       \
        Inventory_Measurement varchar(20) not null,   \
        Inventory_Expiration varchar(20)              \
      )")
    except Error as e:
      if ( re.match("table \w+ already exists", str(e)) is not None ):
        pass
      else:
        print(e)

  def insert_recipe(self, recipename, ingrediences, measurements, instructions, picture):
    # Inserts a recipe into the database if it does not exist
    self.conn, self.cursor = self.connect()
    #test if recipe exists
    self.cursor.execute("select * from Recipe where Recipe_Name like (?)", (recipename,))
    test = self.cursor.fetchall()
    if (test):
      return False 
    else:
      # insert data
      self.cursor.execute("INSERT INTO Recipe (Recipe_Name,Recipe_Ingrediences,Recipe_Measurement,Recipe_Instructions,Recipe_Picture,Recipe_Servings) VALUES (?,?,?,?,?,?)",(recipename, ingrediences, measurements, instructions, picture,4,))
      # last inserted auto increment value
      keyID = self.cursor.lastrowid 
      #print(keyID)
      self.conn.commit()
      print("Insert OK")
      self.close()

  def select_recipes(self):
    # This function returns all recipes in the database
    self.conn, self.cursor = self.connect()
    self.cursor.execute("Select Recipe_Name from Recipe")
    allRecipes = [i[0] for i in self.cursor.fetchall()]
    #pprint(allRecipes)
    self.close()
    return allRecipes

  def show_recipe(self, recipename):
    # This function returns the recipe in a list format
    self.conn, self.cursor = self.connect()
    self.conn.row_factory = sqlite3.Row
    self.cursor.execute("Select * from Recipe where Recipe_Name like (?)", (recipename,))
    try:
      recipe = self.cursor.fetchall()
      self.close()
      return(recipe)
    except:
      self.close()
      return("None")

  def get_planned_meals(self):
    # This function returns a list of all the planned meals
    self.conn, self.cursor = self.connect()

    self.cursor.execute("select * from Mealplan")
    plan = self.cursor.fetchall()

    list = []
    for x in range(0,len(plan)):
      list.append(plan[int(x)][1])
    return(list)

  def add_recipe_to_meal_plan(self,selected_recipe,selected_day):
    # This function updates the mealplan with the recipe and day selected
    self.conn, self.cursor = self.connect()
    self.cursor.execute("UPDATE Mealplan SET Recipe_Name = (?) WHERE Meal_Day = (?) ",(selected_recipe,selected_day))
    self.conn.commit()
    self.close()

  def update_recipe_measurement(self,recipename, list):
    self.conn, self.cursor = self.connect()
    self.cursor.execute("UPDATE Recipe SET Recipe_Measurement = (?) WHERE Recipe_Name = (?) ",(str(list),recipename))
    self.conn.commit()
    self.close()

  def update_recipe_instructions(self, recipename, instructions):
    self.conn, self.cursor = self.connect()
    self.cursor.execute("UPDATE Recipe SET Recipe_Instructions = (?) WHERE Recipe_Name = (?) ",(instructions,recipename))
    self.conn.commit()
    self.close()

  def update_recipe_picture(self, recipename, picture):
    self.conn, self.cursor = self.connect()
    self.cursor.execute("UPDATE Recipe SET Recipe_Picture = (?) WHERE Recipe_Name = (?) ",(picture, recipename))
    self.conn.commit()
    self.close()

  def get_planned_meal(self,day):
    self.conn, self.cursor = self.connect()
    try:
      self.cursor.execute("Select Recipe_Name from Mealplan where Meal_Day like (?)", (day,))
      recipename = self.cursor.fetchall()
      return(recipename)
    except:
      return("None")

  def select_inventory(self):
    #This function returns a list of items in the inventory
    self.conn, self.cursor = self.connect()

    self.cursor.execute("select * from Inventory order by Inventory_Name desc")
    inventory = self.cursor.fetchall()
    if inventory == []:
      self.close()
      return ("inventory is empty")
    else:
      self.close()
      return(inventory)

  def add_inventory(self,item,volume,measurement,expiration):
    self.conn, self.cursor = self.connect()
    # insert data
    self.cursor.execute("INSERT INTO Inventory (Inventory_Name,Inventory_Volume,Inventory_Measurement,Inventory_Expiration) VALUES (?,?,?,?)",(item, volume, measurement, expiration))
    self.conn.commit()
    self.close()

  def delete_inventory(self,name):
    self.conn, self.cursor = self.connect()
    self.cursor.execute("Delete from Inventory where Inventory_Name = (?)", (name,))
    self.conn.commit()
    self.close()

  def update_inventory(self,item,volume,measurement,expiration):
    self.conn, self.cursor = self.connect()
    # insert data
    query = "UPDATE Inventory                  \
             SET Inventory_Volume = (?),       \
                  Inventory_Measurement = (?), \
                  Inventory_Expiration = (?)   \
             WHERE Inventory_Name = (?)"
    values = (volume, measurement, expiration, item)
    self.cursor.execute(query, values)
    self.conn.commit()
    self.close()