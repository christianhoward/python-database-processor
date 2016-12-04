# Python Database Processor

A database processor built using Python 2.7, PyQt4, and SQLite3.

## Requirements
- Python 2.7
- PyQt4
- SQLite3

## To Run
This program can be launched through command line or IDLE. In your terminal, navigate to the directory where the databaseprocessor.py file is located and enter the following command to run it:
```sh
python databaseprocessor.py
```

## Overview
Prior to launching the program, please check lines 174-177 to update the file path to the directory where your table .txt file can be found. A relative file path has been set for Mac users and there are comments within lines 174 and 177 that address absolute path and relative path for Windows and Mac users alike.

In the Graphic User Interface (GUI), you'll find a file loader at the top. In this first box, you'll enter the file name. It should be noted that there is placeholder text in each line edit in the program. For any line edit where an input is required, in this case Load File, Count Rows, Sum Revenue, and Execute SQL, you will need to clear the lines out before adding an input.

All “functions” in this program are actually methods within the defined Form class. Thus, all methods can be found below the initialization method. The Parse and Populate and Revenue Summary methods are executed by pushing their respective buttons. No text entry is needed in their respective line edits. For the Count Rows, Sum Revenue, and Execute SQL methods, you will need to enter words in their respective line edits. The results for the Count Rows and Sum Revenue methods will return in the GUI. The results for the Revenue Summary and Execute SQL methods will return in the IDLE/Terminal window. The Execute SQL method returns the results of your query as a tuple.

## Project Description
In this instance, the database processor program can be used to analyze revenue reports from regional car rental locations.

There are 5 tables within this database:
- Locations
- Cars
- Plans
- Rates
- Sales

There are 10 locations within the Locations table:
- Alexandria
- Annapolis
- Fairfax
- Hagerstown
- Richmond
- Rockville
- Rosslyn
- Taneytown
- Washington
- Westminster

There are 12 cars within the Cars table:
- Chevrolet Impala
- Chevrolet Malibu
- Chevrolet Spark
- Ford Fusion
- Fprd Escape (this typo was part of the dataset)
- Hundai Accent (this typo was part of the dataset)
- Hundai Sonata (this typo was part of the dataset)
- Kia Forte
- Nissan Versa
- Toyota Corolla
- Toyota RAV4
- Volkswagen Jetta

There are 10 plans within the Plans table (PID 1-10). Specifics can be found be querying the following in the SQL Execution box:
```sh
SELECT * FROM Plans ORDER BY PID ASC;
```

There are 4 rates within the Rates table (RLID 1-4). Specifics can be found be querying the following in the SQL Execution box:
```sh
SELECT * FROM Rates ORDER BY RLID ASC;
```

## Code Explanation
Lines 5 - 212 define the class Form. Within the class are multiple methods, including:
- __init__ (lines 6 - 45)
- parseDB (lines 46 - 139)
- CountRows (lines 140 - 147)
- SumRevenue (lines 148 - 156)
- RevSumReport (lines 157 - 164)
- SQLExecution (lines 165 - 171)
- button1Pressed (lines 173 - 186)
- button2Pressed (lines 187 - 190)
- button3Pressed (lines 191 - 195)
- button4Pressed (lines 196 - 200)
- button5Pressed (lines 201 - 204)
- button6Pressed (lines 205 - 209)
- buttonQuitPressed (lines 210 - 212)

#### __init__
The __init__ method creates the form, including all line edits and buttons. Additionally, it established all connections between buttons and their respective form methods (ie: pbutton1 and button1Pressed). 

#### parseDB
The parseDB method takes the .txt file that contains all the table data, in this case CarRental.txt, and breaks it up. Following Database Normalization, the table data is broken down into 5 respective tables: Locations, Cars, Plans, Rates, and Sales.

To break this .txt file up using Python, the program creates 5 lists and executes a for loop through each line. The for loop removes any punctuation and strips the line, and the splits the line up into a list called words. In each line, there are 18 entries in the words list. Then, each entry is assigned to a variable based on it's position in the list (ie: the first entry in words, words[0], is assigned to city). After each entry is assigned to a variable, new lists are created for 4 of the 5 tables: loc (locations), car (cars), plan (plans), rate (rates). 16 of the 18 variables are assigned to these new lists and conditional statements are executed to append the list into it's table list. This means the Locations, Cars, Plans, and Rates lists that are created in lines 47 - 50 contain nested lists inside them.

Once those lists are appended, ids need to be created for the locations, cars, and sales tables. To do this, the program uses for loops and incrementation to create an id for each nested list within our table lists for Locations and Cars. After these two tables are updated with their ids, the program fills the last table list, Sales. To do this, it uses a for loop. The for loop removes any punctuation and strips the line, and then splits the words up into a new list called words2. Variables are assigned to only certain indices within words2, since it is only focused on the Sales table list. Those variables are all put into a new list called sale and are all appended to each other. Finally, a for loop is used to create a transaction id for each list in the list.

The program has made all of the table lists and now connects to a newly created database (called CarRentals.db) and performs a many cursor execute statements. Using wildcard insert, the program is able to populate each table within the database. However, the Sales table does not have the newly created Locations id and Cars id, so the program uses two SQL Update statements to swap out 1 unique identifier (in this case Town and Model) for the new ids. Once this is finished, the program commits and closes the connection.

#### CountRows
The CountRows method will count all rows in any specified table. In the GUI, the user will enter a table name (Locations, Cars, Plans, Rates, Sales). Upon execution of the form method, the program will connect to the database and execute a SQL statement:
```sh
SELECT * FROM UserEnteredTableName;
```
Then the program will execute a for loop, where each row in the table is counted and added to the count variable, which starts at 0. The method then returns the count.

#### SumRevenue
The SumRevenue method will find the total revenue for a specific town. In the GUI, the user will enter the town name they want the revenue for. Upon execution of the form method, the program will connect to the database and execute a SQL statement:
```sh
SELECT Locations.Town, Locations.State. Sum(Revenue) FROM Locations, Sales WHERE Locations.LID = Sales.LID AND Town = UserEnteredLocationName;
```
Then the program prints out the results in the terminal/IDLE window, saves the total revenue as variable x, and returns x.

#### RevSumReport
The RevSumReport method will find the total and average revenue for each make and model at each location. Upon execution of the form method, the program will connect to the database and execute a SQL statement:
```sh
SELECT Locations.Town, Locations.State, Cars.Make, Cars.Model, sum(Revenue) AS TotalRev, Round(Avg(Revenue), 2) AS AvgRev FROM Locations, Cars, Sales WHERE Locations.LID = Sales.LID AND Cars.CID = Sales.CID GROUP BY Locations.Town, Cars.Make, Cars.Model;
```
Then the program will execute a for loop to print out each row of the report into the terminal/IDLE window.

#### SQLExecution
The SQLExecution method will execute any SQL statement the user enters into the line edit. Upon execution of the form method, the program will connect to the database and execute the user's inputed SQL statement. Each row of the SQL statement is returned as a tuple in the terminal/IDLE window.

#### Form Methods
Each form method (button1Pressed, button2Pressed, button3Pressed, button4Pressed, button5Pressed, button6Pressed, buttonQuitPressed) executes the specific method attached to it (ie: button2Pressed executes the parseDB method). Each form method outputs a specific set of text in regards to the method it executed.

## Questions??
If you have any questions, please feel free to contact me.
