class I18N():
  def __init__(self,language):
    if   language == 'en' : self.resourceLanguageEnglish()
    elif language == 'da' : self.resourceLanguageDanish()
    
  def resourceLanguageEnglish(self):
    self.title           = "My Fridge"
    self.tabA            = "This Day"
    self.tabB            = "This Week"
    self.tabC            = "Inventory"
    self.tabD            = "Planner"
    self.tabE            = "Config"
    self.tabR            = "Add recipe"
    self.tabS            = "Edit recipe"

    #tabA
    self.myDay           = "Todays recipe"
    self.number          = "Number"
    self.value           = "Value"
    self.ingrediences    = "Ingrediences"
    self.recipe          = "Recipe"
    self.recipePicture   = "Picture"
    self.shoppinglist    = "Shopping list"
    self.sendshopping    = "Send shopping..."
    self.addshopping     = "Add shopping..."
    self.emptymessage    = "Shopping list is empty"

    self.file            = "File"
    self.exit            = "Exit"
    self.ing             = "Ingredience"
    self.vol             = "Measurement"
    self.myWeek          = "This weeks recipes"
    self.reloadprogram   = "Please reload the software"
    self.swaplanguage    = "Swap language"

    #tabB
    self.monday          = "Monday"
    self.tuesday         = "Tuesday"
    self.wednesday       = "Wednesday"
    self.thursday        = "Thursday"
    self.friday          = "Friday"
    self.saturday        = "Saturday"
    self.sunday          = "Sunday"

    #tabC
    self.myFridge        = "Fridge inventory"
    self.treeName        = "Name"
    self.treeVolume      = "Volume"
    self.treeUnit        = "Unit"
    self.treeExpiration  = "Expiration"
    self.addNewItem      = "Add new item"
    self.deleteItem      = "Delete selected item"

    #tabD
    self.search          = "Select recipe"
    self.selectrecipe    = "Select a recipe.."
    self.numPeople       = "Number of people"
    self.adjust          = "Adjust"
    self.addrecipe       = "Add recipe"
    self.add             = "Add"
    self.remove          = "Remove"
    self.recipeName      = "Recipe name"
    self.selectDay       = "Select a day.."

    self.expiration      = "Expiration"
    self.myPlanner       = "Planner"
    self.myAddrecipe     = "Add recipe"
    self.addInstructions = "Add Instructions"
    self.warning         = "Warning"
    self.checktext       = "Please check all fields are entered"
    self.save            = "Save instructions"
    self.savePic         = "Save picture"

    #tabR
    self.searchRecipe    = "Search recipe.."
    self.searchRecipeAPI = "Search recipe (API)"
    self.searchButton    = "Search"
    self.findPicture     = "Browse picture"
    self.pictureWarning  = "Please select a picture"
    self.recipeWarning   = "Please write a recipe name"
    self.addtoDB         = "Add to DB"

    #Function recipe api
    self.recipeAPI       = "API RECIPE SEARCH"
    self.recipeAPIresult = "Search results"
    self.cancel          = "Cancel"

    #CalendarFrame
    self.countdown       = "Countdown minutes"
    self.settimer        = "Set timer:"
    self.timesup         = "Time's up!"
    self.start           = "Start"
    self.stop            = "Stop"

  def resourceLanguageDanish(self):
    self.title           = "Mit Køleskab"
    self.tabA            = "Min dag"
    self.tabB            = "Min uge"
    self.tabC            = "Indhold"
    self.tabD            = "Planlæg"
    self.tabE            = "Konfigurer"
    self.tabR            = "Tilføj opskrift"
    self.tabS            = "Rediger opskrift"

    #tabA
    self.myDay           = "Dagens opskrift"
    self.number          = "Mængde"
    self.value           = "Måleenhed"
    self.ingrediences    = "Ingredienser"
    self.recipe          = "Opskrift"
    self.recipePicture   = "Billede"
    self.shoppinglist    = "Indkøbsliste"
    self.sendshopping    = "Send indkøb..."
    self.addshopping     = "Tilføj indkøb..."
    self.emptymessage    = "Indkøbslisten er tom"

    self.file            = "Filer"
    self.exit            = "Exit"
    self.ing             = "Ingrediens"
    self.vol             = "Mængde"
    self.myWeek          = "Denne uges opskrifter"
    self.reloadprogram   = "Genstart softwaren for ændringer"
    self.swaplanguage    = "Skift sprog"

    #tabB
    self.monday          = "Mandag"
    self.tuesday         = "Tirsdag"
    self.wednesday       = "Onsdag"
    self.thursday        = "Torsdag"
    self.friday          = "Fredag"
    self.saturday        = "Lørdag"
    self.sunday          = "Søndag"

    #tabC
    self.myFridge        = "Køleskab indhold"
    self.treeName        = "Navn"
    self.treeVolume      = "Mængde"
    self.treeUnit        = "Enhed"
    self.treeExpiration  = "Holdbarhed"
    self.addNewItem      = "Tilføj ny vare"
    self.deleteItem      = "Slet valgte vare"

    #tabD
    self.search          = "Vælg opskrift"
    self.selectrecipe    = "Vælg en opskrift.."
    self.numPeople       = "Antal personer"
    self.adjust          = "Tilpas"
    self.addrecipe       = "Tilføj opskrift"
    self.add             = "Tilføj"
    self.remove          = "Fjern"
    self.recipeName      = "Opskrift navn"
    self.selectDay       = "Vælg en dag.."

    self.expiration      = "Holdbarhed"
    self.myPlanner       = "Planner"
    self.myAddrecipe     = "Tilføj opskrift"
    self.addInstructions = "Tilføj instruktioner"
    self.warning         = "Advarsel"
    self.checktext       = "Check at alle felter er skrevet korrekt"
    self.save            = "Gem instruktioner"
    self.savePic         = "Gem billede"

    #tabR
    self.searchRecipe    = "Søg opskrift.."
    self.searchRecipeAPI = "Søg opskrift (API)"
    self.searchButton    = "Søg"
    self.findPicture     = "Find billede"
    self.pictureWarning  = "Venligst vælg et billede"
    self.recipeWarning   = "Venligst skriv et navn til opskriften"
    self.addtoDB         = "Tilføj til databasen"

    #Function recipe api
    self.recipeAPI       = "API OPSKRIFT SØGNING"
    self.recipeAPIresult = "Søgeresultater"
    self.cancel          = "Afbryd"

    #CalendarFrame
    self.countdown       = "Nedtælling minutter"
    self.settimer        = "Sæt timer:"
    self.timesup         = "Tiden er gået!"
    self.start           = "Start"
    self.stop            = "Stop"

class Fonts():
  def __init__(self):
    self.Fonts()

  def Fonts(self):
    self.FontHeader      = ("Courier", 16, "bold")
    self.FontHeader2     = ("Courier", 12)
    self.Clock           = ("Calibri", 40, "bold")