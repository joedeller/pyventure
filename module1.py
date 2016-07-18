def whichwayold():
    # In a real system we would have a linked table containing exits
    # For this flat file demo, we have a kludge to work out if there
    # is a valid exit for the adventurer to go
    chosenExit = ["", None]
    response = input("Which way ? ")
    response = response[:1].capitalize()
    if response == "N":
        chosenExit = ["North", row[2]]
    elif response == "E":
        chosenExit = ["East", row[3]]
    elif response == "S":
        chosenExit = ["South", row[4]]
    elif response == "W":
        chosenExit = ["West", row[5]]
    elif response == "Q":
        chosenExit = ["Quit", None]
    elif response == "L":  # Look around which just shows current location
        chosenExit = ["L", None]
    print("You want to go:", chosenExit)
    print("current exits are:", row[2:6],'\n')
    return chosenExit

if (exitInfo[0]) == "":
        print("Sorry I don't understand. Parsey McParseFace is offline.")
    




while exitInfo[0] != "Quit":
    if (exitInfo[0]) == "":
        print("Sorry I don't understand. Parsey McParseFace is offline.")
    elif exitInfo[0] == "L":
        print("You look around...")
        # just show location again
        exits = showlocation(row)
    else:
        if exitInfo[1] is not None:
            row = fetchlocation(str(exitInfo[1]))
            exits = showlocation(row)
        else:
            print("Sorry you cannot go that way.")
    isFatal = row[6]  # FIXME magic numbers are bad, get this data separately
    if isFatal is not None:
        print("Game Over.")
        exitInfo = ["Quit"]
    else:
        exitInfo = whichway()
print("Goodbye....")
cur.close()
conn.close()