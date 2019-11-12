import subprocess as sp
import pymysql , getpass
import pymysql.cursors

def insertionInDb(tab,fieldNames):
    try:
        cols=""
        vals=""
        for i in fieldNames:
            cols += "'" + i + "'" + ','
            vals += input("Please Input the value of " + i + "in your " + tab + " : ")

        query = "insert into " + tab + "("  + cols[:-1] + ") values(" + vals[:-1] + ");"
        print(query)
        cur.execute(query)
        con.commit()
    
    except Error as e:
        con.rollback() #To undo the mistakes
        print("Oopsie Doopsie, There was an error")
        print("----->" , e)


def updateInDb(tab,fieldNames,whereFields,whereVals,whereRels):
    try:
        vals=[]
        for i in fieldNames:
            vals.append(input("Value of " + i + "in your " + tab + "has to be updted to : "))

        query = "update " + tab

        for i in range(fieldNames.size()):
            query += "set "+fieldNames[i]+"='"+vals[i]+"' ,"
        query = query[:-1]

        for i in range(whereFields.size()):
            query += "where "+ whereFields[i] + whereRels[i] +"'"+ whereVals[i] + "'"
            if i != whereFields.size():
                query += " AND "

        print(query)
        cur.execute(query)
        con.commit()
    
    except Error as e:
        con.rollback() #To undo the mistakes
        print("Oopsie Doopsie, There was an error")
        print("----->" , e)






def hireAnEmployee():
    try:
        # Takes emplyee details as input
        row = {}
        print("Enter new employee's details: ")
        name = (input("Name (Fname Minit Lname): ")).split(' ')
        row["Fname"] = name[0]
        row["Minit"] = name[1]
        row["Lname"] = name[2]
        row["Ssn"] = input("SSN: ")
        row["Bdate"] = input("Birth Date (YYYY-MM-DD): ")
        row["Address"] = input("Address: ")
        row["Sex"] = input("Sex: ")
        row["Salary"] = float(input("Salary: "))
        row["Dno"] = int(input("Dno: "))

        """
        In addition to taking input, you are required to handle domain errors as well
        For example: the SSN should be only 9 characters long
        Sex should be only M or F
        If you choose to take Super_SSN, you need to make sure the foreign key constraint is satisfied
        HINT: Instead of handling all these errors yourself, you can make use of except clause to print the error returned to you by MySQL
        """

        query = "INSERT INTO EMPLOYEE(Fname, Minit, Lname, Ssn, Bdate, Address, Sex, Salary, Dno) VALUES('%s', '%c', '%s', '%s', '%s', '%s', '%c', %f, %d)" %(row["Fname"], row["Minit"], row["Lname"], row["Ssn"], row["Bdate"], row["Address"], row["Sex"], row["Salary"], row["Dno"])

        print(query)
        cur.execute(query)
        con.commit()

        print("Inserted Into Database")

    except Exception as e:
        con.rollback()
        print("Failed to insert into database")
        print (">>>>>>>>>>>>>", e)
        
    return

def dispatch(ch):
    """
    Function that maps helper functions to option entered
    """

    if(ch==1): 
        hireAnEmployee()
    elif(ch==2):
        fireAnEmployee()
    elif(ch==3):
        promoteEmployee()
    elif(ch==4):
        employeeStatistics()
    else:
        print("Error: Invalid Option")

# Global
while(1):
    tmp = sp.call('clear',shell=True)
    username = input("Username: ")
    password = getpass.getpass(prompt="Please input the password: ")

    try:
        con = pymysql.connect(host='localhost',
                user=username,
                password=password,
                db='COLLEGE',
                cursorclass=pymysql.cursors.DictCursor)
        tmp = sp.call('clear',shell=True)

        if(con.open):
            print("Connected")
        else:
            print("Failed to connect")
        tmp = input("Enter any key to CONTINUE>")

        with con:
            cur = con.cursor()
            while(1):
                tmp = sp.call('clear',shell=True)
                print("=========")
                print("Insert and Additions")
                print("=========")
                print("1. Add new User")
                print("2. Add new User Group")
                print("3. Add new Location")
                print("4. Add an event")
                print("5. Add new course")
                print("6. Add new club")
                print("7. Add User to Usergroup")
                print("8. Appoint new Club Coordinator")
                print("")

                print("=========")
                print("Update")
                print("=========")
                print("9. Change Event Location")
                print("10. Change Event Time")
                print("")

                print("=========")
                print("Delete and Removals")
                print("=========")
                print("11. Remove User from Group")
                print("12. Remove Coordinator of a Club")
                print("13. Delete Event")
                print("14. Delele User")
                print("15. Delete Locations")
                print("")

                ch = int(input("Enter choice> "))
                tmp = sp.call('clear',shell=True)
                if ch==5:
                    break
                else:
                    dispatch(ch)
                    tmp = input("Enter any key to CONTINUE>")



    except:
        tmp = sp.call('clear',shell=True)
        print("Connection Refused: Either username or password is incorrect or user doesn't have access to database")
        tmp = input("Enter any key to CONTINUE>")
    