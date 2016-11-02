import sys, os, string, sqlite3
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Form( QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.resize(425,75)
        self.lineedit1 = QLineEdit('Enter File Name')
        self.pbutton1 = QPushButton('Load File')
        self.lineedit2 = QLineEdit('Parse Data And Populate Database')
        self.pbutton2 = QPushButton("Parse and Populate")
        self.pbutton3 = QPushButton("Count Rows")
        self.lineedit3 = QLineEdit("Enter Table Name")
        self.pbutton4 = QPushButton("Sum Revenue")
        self.lineedit4 = QLineEdit("What location would you like the total revenue for?")
        self.pbutton5 = QPushButton("Revenue Summary")
        self.lineedit5 = QLineEdit('Summary')
        self.pbutton6 = QPushButton("Execute SQL")
        self.lineedit6 = QLineEdit("SQL Statement")
        self.pbuttonQuit = QPushButton("Quit")
        layout = QVBoxLayout()
        layout.addWidget(self.lineedit1)
        layout.addWidget(self.pbutton1)
        layout.addWidget(self.lineedit2)
        layout.addWidget(self.pbutton2)
        layout.addWidget(self.lineedit3)
        layout.addWidget(self.pbutton3)
        layout.addWidget(self.lineedit4)
        layout.addWidget(self.pbutton4)
        layout.addWidget(self.lineedit5)
        layout.addWidget(self.pbutton5)
        layout.addWidget(self.lineedit6)
        layout.addWidget(self.pbutton6)
        layout.addWidget(self.pbuttonQuit)
        self.setLayout(layout)
        self.lineedit1.setFocus()
        self.connect(self.pbutton1, SIGNAL("clicked()"),self.button1Pressed)
        self.connect(self.pbutton2, SIGNAL("clicked()"),self.button2Pressed)
        self.connect(self.pbutton3, SIGNAL("clicked()"),self.button3Pressed)
        self.connect(self.pbutton4, SIGNAL("clicked()"),self.button4Pressed)
        self.connect(self.pbutton5, SIGNAL("clicked()"),self.button5Pressed)
        self.connect(self.pbutton6, SIGNAL("clicked()"),self.button6Pressed)
        self.connect(self.pbuttonQuit, SIGNAL("clicked()"),self.buttonQuitPressed)
        self.setWindowTitle("Database Application")
    #break .txt file into the respective tables
    def parseDB(self):
        locations = []
        cars = []
        plans = []
        rates = []
        sales = []
        lid = 0
        cid = 0
        trxid = 0
        for line in self.lines:
            line = line.translate(None, string.punctuation)
            line = line.strip()
            words = line.split()
            city = words[0]
            state = words[1]
            density = words[2]
            lotsize = words[3]
            make = words[4]
            model = words[5]
            modelyear = words[6]
            ratelevel = words[7]
            pid = words[8]
            duration = words[9]
            discount = words[10]
            discounttype = words[11]
            rlid = words[12]
            daily = words[13]
            weekly = words[14]
            monthly = words[15]
            units = words[16]
            revenue = words[17]
            loc = [city, state, density, lotsize]
            car = [make, model, modelyear, ratelevel]
            plan = [pid, duration, discount, discounttype]
            rate = [rlid, daily, weekly, monthly]
            if loc not in locations:
                locations.append(loc)
            elif car not in cars:
                cars.append(car)
            elif plan not in plans:
                plans.append(plan)
            elif rate not in rates:
                rates.append(rate)
        for rowl in locations:
            lid = lid + 1
            if lid not in rowl:
                rowl.append(lid)
        for rowc in cars:
            cid = cid + 1
            if cid not in rowc:
                rowc.append(cid)
        for l2 in self.lines:
            l2 = l2.translate(None, string.punctuation)
            l2 = l2.strip()
            words2 = l2.split()
            city = words2[0]
            model = words2[5]
            pid = words2[8]
            rlid = words2[12]
            units = words2[16]
            revenue = words2[17]
            sale = [city, model, pid, rlid, units, revenue]
            sales.append(sale)
        for rowr in sales:
            trxid = trxid + 1
            if trxid not in rowr:
                rowr.append(trxid)
        conn = sqlite3.connect('CarRentals.db')
        cur = conn.cursor()
        #locations
        cur.execute("drop table if exists Locations")
        cur.execute("create table Locations (Town text, State text, Density text, 'Lot Size' int, LID int);")
        cur.executemany("INSERT INTO Locations VALUES(?, ?, ?, ?, ?)", locations)
        #cars
        cur.execute("drop table if exists Cars")
        cur.execute("create table Cars (Make text, Model text, 'Model Year' int, Rate Level int, CID int);")
        cur.executemany("INSERT INTO Cars VALUES(?, ?, ?, ?, ?)", cars)
        #plans
        cur.execute("drop table if exists Plans")
        cur.execute("create table Plans (PID int not null, Duration text, Discount int, 'Discount Type' text);")
        cur.executemany("INSERT INTO Plans VALUES(?, ?, ?, ?)", plans)
        #rates
        cur.execute("drop table if exists Rates")
        cur.execute("create table Rates (RLID int not null, Daily int, Weekly int, Monthly int);")
        cur.executemany("INSERT INTO Rates VALUES(?, ?, ?, ?)", rates)
        #sales
        cur.execute("drop table if exists Sales")
        cur.execute("create table Sales (LID int, CID int, PID int, RLID int, Units int, Revenue int, TrxId int);")
        cur.executemany("INSERT INTO Sales VALUES(?, ?, ?, ?, ?, ?, ?)", sales)
        cur.execute("UPDATE Sales SET LID = (SELECT Locations.LID FROM Locations WHERE Locations.Town = Sales.LID);")
        cur.execute("UPDATE Sales SET CID = (SELECT Cars.CID FROM Cars WHERE Cars.Model = Sales.CID);")
        conn.commit()
        print "Rows Inserted and Committed"
        conn.close()
    #Count number of rows in a specific table
    def CountRows(self, table):
        count = 0
        conn = sqlite3.connect('CarRentals.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM " + str(table) + ';')
        for row in cur:
            count = count + 1
        return count
    #provide total revenue for locations
    def SumRevenue(self, location):
        conn = sqlite3.connect('CarRentals.db')
        cur = conn.cursor()
        cur.execute("SELECT Locations.Town, Locations.State, sum(Revenue) FROM Locations, Sales WHERE Locations.LID = Sales.LID AND Town = " + "'"+str(location)+"'" + ";")
        print 'Town' + '\t' + 'State' + '\t' + 'Total Revenue'
        for row in cur:
            x = row[2]
            print str(row[0]) + '\t' + str(row[1]) + '\t' + str(row[2]) + '\n'
        return x
    #provide total and average revenue for locations broken down by car make and model
    def RevSumReport(self):
        conn = sqlite3.connect('CarRentals.db')
        cur = conn.cursor()
        cur.execute("SELECT Locations.Town, Locations.State, Cars.Make, Cars.Model, sum(Revenue) AS TotalRev, ROUND(Avg(Revenue),2) AS AvgRev FROM Locations, Cars, Sales WHERE Locations.LID = Sales.LID AND Cars.CID = Sales.CID GROUP BY Locations.Town, Cars.Make, Cars.Model;")
        print 'Location Revenue Summary Report'
        print 'Town' + '\t' + 'State' + '\t' + 'Make' + '\t' + 'Model' + '\t' + 'Total Revenue' + '\t' + 'Average Revenue'
        for row in cur:
            print str(row[0]) + '\t' + str(row[1]) + '\t' + str(row[2]) + '\t' + str(row[3]) + '\t' + str(row[4]) + '\t' + str(row[5])
    #run additional sql queries
    def SQLExecution(self, statement):
        conn = sqlite3.connect('CarRentals.db')
        cur = conn.cursor()
        cur.execute(str(statement))
        print "Results of SQL Query"
        for row in cur:
            print row
    # Form Methods
    def button1Pressed(self):
        #For Windows -- Update variable f to the absolute file path ('C:/Users/**INSERT FULL DIRECTORY HERE**') + g or relative file path '.\' + g
        #For Mac -- Update variable f to the absolute file path (/Users/**INSERT FULL DIRECTORY HERE**') + g or keep relative file path in line 177
        g = str(self.lineedit1.text())
        f = './' + g
        try:
            with open(f) as load: #opens file, sets load.readlines = self.lines, then closes program
                self.lines = load.readlines()
            outtext = 'The file ' + str(g) + ' has been loaded.'
            self.lineedit1.setText(outtext)
        except (ValueError, TypeError, IOError):
            outtext = 'Error: could not read file ' + g + '.'
            self.lineedit1.setText(outtext)
            self.lines = []
    def button2Pressed(self):
        p = self.parseDB()
        outtext = 'The file has been parsed and the database has been populated.'
        self.lineedit2.setText(outtext)
    def button3Pressed(self):
        r = str(self.lineedit3.text())
        rr = self.CountRows(r)
        outtext = 'The ' + str(r)+ "' table has " + str(rr) + ' rows.'
        self.lineedit3.setText(outtext)
    def button4Pressed(self):
        l = str(self.lineedit4.text())
        ll = self.SumRevenue(l)
        outtext = 'The ' + str(l) + ' location has $' + str(ll) + ' in total revenue.'
        self.lineedit4.setText(outtext)
    def button5Pressed(self):
        self.RevSumReport()
        outtext = 'Please see IDLE window for Location Revenue Summary Report.'
        self.lineedit5.setText(outtext)
    def button6Pressed(self):
        r = str(self.lineedit6.text())
        rr = self.SQLExecution(r)
        outtext = 'Please see IDLE window for the results of your SQL statement.'
        self.lineedit6.setText(outtext)
    def buttonQuitPressed(self):
        self.done(1)
        app.quit()

# End of Form Class Definition
app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()
