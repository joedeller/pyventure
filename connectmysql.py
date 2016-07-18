import pymysql
conn= pymysql.connect(host='localhost',database='mydb',user='joe',password='selectbne')
cur=conn.cursor()
cur.execute ("SELECT idLocations, description,NorthExit,EastExit,SouthExit,WestExit FROM locations")
#print (cur.description)
row = cur.fetchone()

while row is not None:
        exits=""
        print("{} {}".format("ID=", row[0])) # ID
        print ("{} {}".format("You are in :",row[1])) # Desc
        if row[2] is not None:
            exits = exits +"North "
        if row[3] is not None:
            exits+= " East"
        if row[4] is not None:
            exits = exits +"South "
        if row[5] is not None:
            exits+= " West"
        print ("You can go:" + exits)            
        row = cur.fetchone()
        print()
#for row in cur:
#    print (row)

cur.close()
conn.close()

