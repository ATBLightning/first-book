from django.shortcuts import render,redirect
from .forms import TestForm,login_userForm,login_passwordForm,SelecttableForm
from django.contrib import messages
import mysql.connector

# Create your views here.

#global variable
username,password,table,mydb,status = '','','','','login'
columns = []
#---------------------------------------------------------------------------------------------------------
def index(request):
    myresult,columns = [],[]
    global username,mydb
    if username == "":
        return redirect('/login')
    if request.method == 'POST' and 'query1' in request.POST:
        mycursor = mydb.cursor()
        try:
            sql = request.POST['query1']
            mycursor.execute(sql)
            columns = mycursor.column_names
            myresult = mycursor.fetchall()
        except:
            myresult,columns = [],[]
    return render(request, 'index.html', {'myresult':myresult,'columns':columns,'name':username,'login':username,'logout':status})


#---------------------------------------------------------------------------------------------------------
def login(request):
    global mydb,username,password,status
    username = ""
    password = ""
    status = "login"
    if request.method == 'POST':
        username = request.POST['Username']
        password = request.POST['Password']
        try:
            mydb = mysql.connector.connect(
            host ="localhost",
            user = username,
            passwd = password,
            database = "book",
            auth_plugin='mysql_native_password'
            )
            status = "logout"
            return redirect('/index')
        except:
            username = ""
            messages.info(request, '!!! Login Error !!!')
    return render(request,'login.html', {'user':login_userForm,'pass':login_passwordForm,'login':username,'logout':status})

#---------------------------------------------------------------------------------------------------------
def database(request):
    myresult,columns = [],[]
    if username == "":
        return redirect('/login')
    if request.method == 'POST':
        table = request.POST['Select_Table']
        mydb = mysql.connector.connect(
        host ="localhost",
        user = 'user1',
        passwd = '1234',
        database ="book",
        auth_plugin='mysql_native_password'
        )
        mycursor = mydb.cursor()
        try:
            sql = "SELECT * FROM "+str(table)
            mycursor.execute(sql)
            columns = mycursor.column_names
            myresult = mycursor.fetchall()
        except:
            myresult,columns = [],[]

    return render(request, 'database.html', {'choice':SelecttableForm,'myresult':myresult,'columns':columns,'login':username,'logout':status})

#---------------------------------------------------------------------------------------------------------
def insert(request):
    global columns,table,username,password
    add_table,values,check,columns = "",[],False,[]
    if username == "":
        return redirect('/login')
    try:
        mydb = mysql.connector.connect(
        host ="localhost",
        user = username,
        passwd = password,
        database ="book",
        auth_plugin='mysql_native_password'
        )
        mycursor = mydb.cursor()
        mycursor.execute(("INSERT INTO cinsert (No, ID) VALUES (%s, %s)"),['1','1'])
        mydb.commit()
        mycursor.close()
        mydb.close()
        check = True
    except mysql.connector.errors.ProgrammingError:
        messages.info(request, '!!! User Error !!!')
    if request.method == 'POST' and 'table' in request.POST and check:
        table = request.POST['Select_Table']
        mydb = mysql.connector.connect(
        host ="localhost",
        user = username,
        passwd = password,
        database ="book",
        auth_plugin='mysql_native_password'
        )
        mycursor = mydb.cursor()
        sql = "SELECT * FROM "+str(table)+";"
        mycursor.execute(sql)
        columns = mycursor.column_names
    if request.method == 'POST' and 'insert' in request.POST :
        for column in columns:
            value = request.POST[column]
            values.append(value)
        if table == 'Books':
            add_table = ("INSERT INTO Books "
                        "(BookID, Title, No_of_Pages, Publish_No, Category,PubDate) "
                        "VALUES (%s, %s, %s, %s, %s, %s)")
        elif table == 'Authors':
            add_table = ("INSERT INTO Authors "
                        "(No, Fname, Lname) "
                        "VALUES (%s, %s, %s)")
        elif table == 'Locations':
            add_table = ("INSERT INTO Locations "
                        "(No, Location) "
                        "VALUES (%s, %s)")
        elif table == 'Publishers':
            add_table = ("INSERT INTO Publishers "
                        "(No, Publisher_Name, PhoneNo) "
                        "VALUES (%s, %s, %s)")
        elif table == 'Sent_to':
            add_table = ("INSERT INTO Sent_to "
                        "(Author_ID, Publisher_No) "
                        "VALUES (%s, %s)")
        elif table == 'Write_to':
            add_table = ("INSERT INTO Write_to "
                        "(Book_ID, Author_ID) "
                        "VALUES (%s, %s)")
        mydb = mysql.connector.connect(
        host ="localhost",
        user = username,
        passwd = password,
        database ="book",
        auth_plugin='mysql_native_password'
        )
        mycursor = mydb.cursor()
        mycursor.execute(add_table, values)
        mydb.commit()
        mycursor.close()
        mydb.close()
        columns = []
    return render(request,'insert.html',{'choice':SelecttableForm,'columns':columns,'login':username,'logout':status})

#---------------------------------------------------------------------------------------------------------
def home(request):
    global username
    return render(request,'home.html',({'login':username,'logout':status}))
#----------------------------------------------------------------------------------------------------------
def manage(request):
    global columns,table,username,password
    add_table,values,check,columns,myresult = "",[],False,[],[]
    if username == "":
        return redirect('/login')
    try:
        mydb = mysql.connector.connect(
        host ="localhost",
        user = username,
        passwd = password,
        database ="book",
        auth_plugin='mysql_native_password'
        )
        mycursor = mydb.cursor()
        mycursor.execute(("INSERT INTO cinsert (No, ID) VALUES (%s, %s)"),['1','1'])
        mydb.commit()
        mycursor.close()
        mydb.close()
        check = True
        print(check)
    except mysql.connector.errors.ProgrammingError:
        messages.info(request, '!!! User Error !!!')
    if request.method == 'POST' and check:
        table = request.POST['Select_Table']
        mydb = mysql.connector.connect(
        host ="localhost",
        user = username,
        passwd = password,
        database ="book",
        auth_plugin='mysql_native_password'
        )
        mycursor = mydb.cursor()
        try:
            sql = "SELECT * FROM "+str(table)
            mycursor.execute(sql)
            columns = mycursor.column_names
            columns = list(columns) + ['Edit','Delete']
            myresult = mycursor.fetchall()
        except:
            myresult,columns = [],[]
    return render(request,'manage.html',{'choice':SelecttableForm,'myresult':myresult,'columns':columns,'login':username,'logout':status})




