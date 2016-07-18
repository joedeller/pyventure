import pymysql  # pip install pymysql
# Separating data and code example using mySQL as a flat file
# A true program would use the full relational database features
# This code only allows moving around for now
import textwrap

def fetchlocation(locationid):
    query = "SELECT idLocations, description,NorthExit,EastExit,SouthExit,WestExit,Fatal" \
            " FROM locations WHERE idLocations="
    query += locationid
    #print(query, "\n")
    cur.execute(query)
    locationdata = cur.fetchone()
    return locationdata


def showlocation(locationData):
    # show where we are, any items and return the possible exits from the location
    #locationid = str(locationData[0])
    query = "SELECT description,Fatal" \
            " FROM locations WHERE idLocations='1'"
#    query += str(locationData)
    #print(query, "\n")
    cur.execute(query)
    locationdata = cur.fetchone()
   # print(textwrap.fill ("{} {}".format("You are:", locationData[1])))  # Description of location
    # The N,E,S,W exits are in location data 2-5, copy these into an array of exits
        exitList = ""
        for exit in exits:
            if exit is not None:
                exitList = exitList +exit[0] +", "
        if (len(exitList)>0):
           exitList =exitList[:len(exitList)-2] + "."         
        print("{} {}".format("Possible exits are:", exitList))  #the item text without decoration
            #current_exits[0:3] = locationData[2:5]
    showItems(locationid)
    #return current_exits

def checkValidExit(locationid,direction):
    newLocation = 0
    query = "SELECT newLocationId FROM locationExits WHERE LocationId = " + locationid + " AND  shortName = " + direction
    cur.execute(query)
    exit = list(cur.fetchone())
    if ( cur.rowcount>0):
        newlocation = exit[0]
    return newlocation

def showItems(locationId):
    # each location can have no, one or two items, this query IS relational
    # It gets data from another table using our current location Id
    query = "SELECT Item FROM Items WHERE LocationId = " + locationId
    cur.execute(query)
    items = list(cur.fetchall())
    if ( cur.rowcount>0):
        for item in items:
            if item is not None:
                 print("{} {}".format("You can see:", item[0]))  #the item text without decoration


def whatnow():
    response = input("What now ? ")
    response = response[:1].capitalize()
    return response


print ('\n*******************************************************************************\n')
print("\nWelcome to the adventure. Hint: It doesn't end well for you :-(\n")
# Connect to the mySQL database, other databases are available
conn = pymysql.connect(host='localhost', database='mydb', user='joe', password='selectbne')
cur = conn.cursor()
showlocation(1)
#locationdata = fetchlocation("1")
#locationId = showlocation(locationdata)
#exitInfo = whichway()

action = whatnow()


while action != "Q":
    if action == "L":
        print("You look around...")
        # just show location again
        showlocation(locationId)
    else:
        locationId= checkValidExit(locationId,action)
        if (locationId!=0):
           showlocation(locationId)
        else:
            print("Sorry you cannot go that way.")
    isFatal = row[6]  # FIXME magic numbers are bad, get this data separately
    if isFatal is not None:
        print("Game Over.")
        exitInfo = ["Quit"]
    else:
        action= whatnow()
print("Goodbye....")
cur.close()
conn.close()