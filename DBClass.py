import mysql.connector

class DBClass:

    def __init__(self):
        self.commandDict = {}
        self.messagesDict = {}

    def dbConnect(self):
        self.mydb = mysql.connector.connect(
        host = "",
        user = "",
        passwd = "",
        database = ""
        )
        self.mycursor = self.mydb.cursor()

    def messagesFromDB(self):
        self.dbConnect()
        sqlQuery = "SELECT * FROM tblMessages"
        self.mycursor.execute(sqlQuery)
        sqlResult = self.mycursor.fetchall()
        self.mydb.close()
        for row in sqlResult:
            self.messagesDict[row[1]] = row[2]
        return self.messagesDict

    def commandFromDBParser(self):
        #Open connection to the DB
        self.dbConnect()
        #The query we want
        sqlQuery = "SELECT * FROM tblCommands"
        #Execute the query
        self.mycursor.execute(sqlQuery)
        #Get the results
        sqlResult = self.mycursor.fetchall()
        #We no longer need the open connection to the DB so we close it
        self.mydb.close()
        #Loop to put our results into a dictionary
        for row in sqlResult:
            self.commandDict[row[2]] = row[3]
        return self.commandDict
