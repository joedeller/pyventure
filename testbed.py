import pymysql  # pip install pymysql
# Separating data and code example using mySQL
# This code only allows moving around for now
# Each location has a unique number that is used to keep
# track of where we are, what the exits are and what items are there
import textwrap # Helps with formating text to fit in the console
from contextlib import closing # helps us clean up database cursors

def showLocation(locationId):
    # show where we are, any items and return the possible exits from the location
    with closing(db.cursor()) as cur:
        query = "SELECT description,Fatal FROM locations WHERE idLocations=" + str(locationId)
        cur.execute(query)
        locationdata = cur.fetchone()
        print(textwrap.fill ("{} {}".format("You are:", locationdata[0])))  # the item text without decoration
        showItems(locationId)
        showExits(locationId)
        showMonsters(locationId)
        isFatal = locationdata[1] # Some locations are fatal to enter
        return isFatal

def showItems(locationId):
    # Fetch a list of items at the location, if any
    with closing(db.cursor()) as cur:
        query = "SELECT Item FROM items WHERE LocationId = " + str(locationId)
        cur.execute(query)
        items = list(cur.fetchall()) # we might have several items
        if (cur.rowcount > 0):
            for item in items:
                if item is not None:
                    print("{} {}".format("You can see:", item[0]))  # the item text without decoration


def showExits(locationId):
    # Get a list of visible exits for the location
    with closing(db.cursor()) as cur:
        exitList = ''
        query = "SELECT exitName FROM locationexits WHERE locationId = " + str(locationId) + " AND isHidden = 0"
        cur.execute(query)
        exits = list(cur.fetchall())
        for exit in exits:
            if exit is not None:
                exitList = exitList + exit[0] + ", "
        if (len(exitList) > 0):
            exitList = exitList[:len(exitList) - 2] + "."
            print("{} {}".format("Possible exits are:", exitList))



def checkValidExit(locationid, direction):
    newlocation = 0
    with closing(db.cursor()) as cur:
        query = "SELECT newLocationId FROM locationexits WHERE LocationId = " + str(
            locationid) + " AND  shortName = '" + direction + "'"
        isValid = cur.execute(query)# did we get any results back, i.e. can we go that way?
        if (isValid != 0):
            exit = list(cur.fetchone())
            if (cur.rowcount > 0):
                newlocation = exit[0]
        else:
            print("You cannot go " + direction)
            newlocation = locationId
        return newlocation

def showMonsters(locationId):
    # Fetch a list of items at the location, if any
    with closing(db.cursor()) as cur:
        query = "SELECT Description, weapon FROM monsters WHERE LocationId = " + str(locationId)
        cur.execute(query)
        monsters = list(cur.fetchall()) # we might have several items
        if (cur.rowcount > 0):
            for monster in monsters:
                if monster is not None:
                    print("{} {} armed with {}".format("Oh Oh! You can see a:", monster[0], monster[1]))

def whatnow():
    response = input("What now ? ")
    response = response[:1].capitalize()#For now only look at the first letter of what we typed
    print()
    return response

# DOCKER VERSION
db = pymysql.connect(host='192.168.99.100', port = 32778,database='mydb', user='joe', password='selectbne')
# LOCALHOST VERSION
#db = pymysql.connect(host='localhost', database='mydb', user='joe', password='selectbne')
print ('\n*******************************************************************************\n')
print("\nWelcome to the adventure. Hint: It doesn't end well for you :-(\n")
locationId = 1
showLocation(locationId)
action = whatnow()

while action != "Q":
    if action == "L":
        print("You look around...")
        # just show location again
        showLocation(locationId)
    else:
        newlocationId = checkValidExit(locationId, action)
        if (newlocationId != locationId):
            locationId = newlocationId
            isFatal = showLocation(locationId)
            if isFatal is not None:
                print("Game Over.")
                action = "Q"
    if (action != "Q"):
        action = whatnow()

print("Goodbye !")
db.close()
