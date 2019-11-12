import subprocess as sp
import pymysql , getpass
import pymysql.cursors


def insertionInDb(con,tab,fieldNames):
    cur = con.cursor()
    print("In Insertion" )
    print(cur)
    try:
        cols=""
        vals=""
        for i in fieldNames:
            cols +=  i + ","
            vals += "\'" + input("Please Input the value of " + i + " in your " + tab + " : ") +"\'" + ","

        query = "insert into " + tab + "(" + cols[:-1] + ") values(" + vals[:-1] + ");"
        print(query)
        cur.execute(query)
        con.commit()
    
    except Exception as e:
        con.rollback() #To undo the mistakes
        print("Oopsie Doopsie, There was an error")
        print("----->" , e)


def updateInDb(con,tab,fieldNames,whereFields,whereVals,whereRels):
    cur = con.cursor()
    try:
        vals=[]
        for i in fieldNames:
            vals.append(input("Value of " + i + " in your " + tab + " has to be updated to : "))

        query = "update " + tab

        query += " set "
        for i in range(len(fieldNames)):
            query += fieldNames[i]+"=\'"+vals[i]+"\' ,"
        query = query[:-1]

        for i in range(len(whereFields)):
            query += "where "+ whereFields[i] + whereRels[i] +"\'"+ whereVals[i] + "\'"
            if i != len(whereFields)-1:
                query += " AND "

        print(query)
        cur.execute(query)
        con.commit()
    
    except Exception as e:
        con.rollback() #To undo the mistakes
        print("Oopsie Doopsie, There was an error")
        print("----->" , e)


def deleteInDb(con,tab,whereFields,whereVals,whereRels):
    cur = con.cursor()
    try:
        
        query = "delete from " + tab

        for i in range(len(whereFields)):
            query += " where "+ whereFields[i] + whereRels[i] +"\'"+ whereVals[i] + "\'"
            if i != len(whereFields)-1:
                query += " AND "

        print(query)
        cur.execute(query)
        con.commit()
    
    except Exception as e:
        con.rollback() #To undo the mistakes
        print("Oopsie Doopsie, There was an error")
        print("----->" , e)

def agendaUser(con):
    cur = con.cursor()
    user_id = input("Insert the user ID whose report you want to generate: ")

    try:
        query="select event_name , building_name ,room_number , event_date , start_time , end_time from event join group_members on group_members.group_id = event.group_id where group_members.user_id = " + user_id + " order by event_date ;"
        cur.execute(query)
        print(cur.fetchall())

    except Exception as e:
        print("Error ----> " , e)

def eventsOfDay(con):
    cur = con.cursor()
    date = input("Insert the date (YYYY-MM-DD) ")

    try:
        query="select * from event where date = \'" + date + "\' ;"
        cur.execute(query)
        print(cur.fetchall())

    except Exception as e:
        print("Error ----> " , e)

def locIsFree(con):
    cur = con.cursor()
    building = input("Enter Building:")
    room = input("enter Room:")
    date = input("Insert the date (YYYY-MM-DD) ")
    start_time = input("Input the start time")
    end_time = input("Input the end time")

    try:
        query="""where building_name=\'"""+building+"""\' and room_number=\'"""+room +"""\' and event_date = \'"""+ date +"""\' and 
( 
    (start_time between \'"""+start_time+"""\' and \'"""+end_time+"""\' or end_time between \'"""+start_time+"""\' and \'"""+end_time+"""\')
    OR
    (start_time < \'"""+start_time+"""\' and end_time > \'"""+end_time+"""\' )
);"""
        cur.execute(query)
        print(cur.fetchall())

    except Exception as e:
        print("Error ----> " , e)

def groupInvited(con):
    event_name = input("Input the name of the event : ")
    group_name = input("Input the Group name: ")
    try: 
        query="select count(group_id) from user_group join event on user_group.group_id = event.group_id where event_name = \'" + event_name + "\' and user_group.name = \'" + group_name +"\';"
        cur.execute(query)
        print(cur.fetchall())

    except Exception as e:
        print("Error ---> ",e)
        


def addUser(con):
    insertionInDb(con,'student',['user_id','user_name','DOB','gender','hostel','year_of_admission','program_name'])

def addGroup(con):
    insertionInDb(con,'user_group',['group_id','name','type'])

def addLocation(con):
    insertionInDb(con,'location',['building_name','room_number','room_name'])

def addEvent(con):
    insertionInDb(con,'event',['event_name','building_name','room_number','group_id','start_time','end_time','event_date'])

def addCourse(con):
    insertionInDb(con,'course',['course_id','course_name','department_id'])

def addUserToGroup(con):
    insertionInDb(con,'group_members',['user_id','group_id'])

def addClubCo(con):
    insertionInDb(con,'club_co',['group_id','user_id'])

def changeLocation(con):
    name=input("What is the name of the event whose location you want to change?: ")
    updateInDb(con,'event',['building_name','room_number'],['event_name'],[name],["="])

def changeTime(con):
    name=input("What is the name of the event whose time you want to change?: ")
    updateInDb(con,'event',['start_time','end_time'],['event_name'],[name],["="])

def delUserFromGroup(con):
    user_id=input("What is the ID of the user you wanna remove?:")
    group_id=input("What is the ID of the group you want to remove the user from? :")
    deleteInDb(con,'group_members',['user_id','group_id'],[user_id,group_id],["=","="])

def delLocation(con):
    room=input("What is the room number which you want to delete?")
    buil=input("What is the building you want to delte the room from?")
    deleteInDb(con,'location',['building_name','room_number'],[buil,room],["=","="])

def delEvent(con):
    name=input("What is the name of the Event(s) you want to delete?: ")
    deleteInDb(con,'event',['event_name'],[name],["="])

def delUser(con):
    user_id=input("What is the ID of the student you wanna remove?: ")
    deleteInDb(con,'student',['user_id'],[user_id],["="])

def delClubCo(con):
    user_id=input("What is the ID of Coordinator ? ")
    group_id=input("What is the ID of the group you want to remove the coordinator of? :")
    deleteInDb(con,'club_co',['user_id','group_id'],[user_id,group_id],["=","="])


def dispatch(con,ch):
    """
    Function that maps helper functions to option entered
    """

    if(ch=='1'): 
        addUser(con)
    elif(ch=='2'):
        addGroup(con)
    elif(ch=='3'):
        addLocation(con)
    elif(ch=='4'):
        addEvent(con)
    elif(ch=='5'):
        addCourse(con)
    elif(ch=='7'):
        addUserToGroup(con)
    elif(ch=='8'):
        addClubCo(con)
    elif(ch=='9'):
        changeLocation(con)
    elif(ch=='10'):
        changeTime(con)
    elif(ch=='11'):
        delUserFromGroup(con)
    elif(ch=='12'):
        delClubCo(con)
    elif(ch=='13'):
        delEvent(con)
    elif(ch=='15'):
        delLocation(con)
    elif(ch=='14'):
        delUser(con)
    elif(ch=='16'):
        agendaUser(con)
    elif(ch=='17'):
        eventsOfDay(con)
    elif(ch=='18'):
        groupInvited(con)
    elif(ch=='19'):
        locIsFree(con)
    elif(ch=="e"):
        exit()
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
                db='CALENDAR',
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
                print("14. Delete User")
                print("15. Delete Location")
                print("")


                print("=========")
                print("Report Generation")
                print("=========")
                print("16.Agenda of a particular User")
                print("17. All the events on a particular day")
                print("18. Check if a particular user group is invited to an event")
                print("19. Check if a location is free at a particular time slot")

                print("q to Quit to login and e to Exit application")

                ch = input("Enter choice> ")
                tmp = sp.call('clear',shell=True)
                if ch=='q':
                    break
                else:
                    dispatch(con,ch)
                    tmp = input("Enter any key to CONTINUE>")



    except Exception as e:
        tmp = sp.call('clear',shell=True)
        print("Connection Refused: Either username or password is incorrect or user doesn't have access to database")
        print("Error Code: " , e)
        tmp = input("Enter any key to CONTINUE>")
    