import mysql.connector as mycon

con = mycon.connect(host="localhost", user="root", passwd="shreyaas")
cur = con.cursor()


sql1 = "CREATE DATABASE IF NOT EXISTS projectfinale"
cur.execute(sql1)


sql2 = "USE projectfinale"
cur.execute(sql2)

sql3 = "CREATE TABLE IF NOT EXISTS MyShow (Movie_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY, MovieName VARCHAR(20), ShowTime VARCHAR(50), Date VARCHAR(20))"
cur.execute(sql3)


sql6 = """
CREATE TABLE IF NOT EXISTS Worker (
    Name VARCHAR(100),
    Work VARCHAR(100),  
    Salary VARCHAR(20)
)
"""
cur.execute(sql6)
sql7 = """
CREATE TABLE IF NOT EXISTS ticketing (
    Show_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Seat_No VARCHAR(5),
    Name VARCHAR(25),
    Tickets INT(5),
    Ticket_Amount FLOAT,
    Movie_ID INT,
    ShowTime VARCHAR(50),
    Date VARCHAR(20),
    FOREIGN KEY (Movie_ID) REFERENCES MyShow(Movie_ID) ON DELETE CASCADE
)
"""


cur.execute(sql7)

sql8 = """
CREATE TABLE IF NOT EXISTS food (
    Order_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(25),
    Order_amount FLOAT,
    Show_ID INT,
    FOREIGN KEY (Show_ID) REFERENCES ticketing(Show_ID) ON DELETE CASCADE
)
"""

cur.execute(sql8)
con.commit()





def signin():
    print("\n")
    print(" ----------------------->>>>>>>>>>>>>>>>Welcome, TDS MOVIES CINEMA <<<<<<<<<<<<<-----------------------")
    print("\n")
    p= input("Admin Password:")
    if p=="1234":
        options()
    else:
        signin()

def options():
    print("""
          1.   Add shows  
          2.   Book Ticket 
          3.   Delete Ticket
          4.   Add Worker
          5.   Display shows 
          6.   Display Booking 
          7.   Display Worker
          8.   EXIT
          """)
    choice= input("Select Option:")
    while True:
        if choice=='1':
            AddShows()
        elif choice=='2':
            Booking()
        elif choice=='3':
            del_tc()
        elif choice=='4':
            AddWorker()
        elif choice=='5':
            dShows()
        elif choice=='6':
            dBooking()
        elif choice=='7':
            dWorker()
        elif choice=='8':
            break
        else:
            print("Enter Again..............")
            options()
def AddShows():
    mn = input("Movie Name:")
    st = input("Show Time:")
    d = input("Date:")

    
    data = (mn, st, d)

    sql = 'INSERT INTO MyShow (MovieName, ShowTime, Date) VALUES (%s, %s, %s)'
    cur.execute(sql, data)
    con.commit()
    
    
    movie_id = cur.lastrowid
    
    print("Data Inserted Successfully")
    print(f"Movie ID: {movie_id}")  
    options()
def Booking():
    print("Currently Showing:")
    cur.execute("select*from MyShow")
    result=cur.fetchall()
    for row in result:
        print(row, '\n')
    book_tc()
    options()
def AddWorker():
    n= input("Name:")
    w= input("Work:")
    s= input("Slary:")
    data= (n,w,s)
    sql='insert into worker values(%s,%s,%s)'
    cur= con.cursor()
    cur.execute(sql,data)
    con.commit()
    print("Data Inserted Successfully")
    options()
def dShows():
    sd= input("Show Date:")
    sql= 'select* from MyShow'
    cur= con.cursor()
    cur.execute(sql)
    d= cur.fetchall()
    for i in d:
        if i[3]==sd:
            print(i)
    options()
def dBooking():
    sd = input("Show Date:")
    sql = 'SELECT * FROM ticketing WHERE Date = %s'  # Assuming Date is the column storing show dates
    cur = con.cursor()
    cur.execute(sql, (sd,))
    d = cur.fetchall()
    
    if len(d) > 0:
        for i in d:
            print("Show ID:", i[0])
            print("Seat No:", i[1])
            print("Name:", i[2])
            print("Tickets:", i[3])
            print("Ticket Amount:", i[4])
            print("Movie ID:", i[5])
            print("Date:", i[6])
            print("Show Timings:", i[7])
            print()
    else:
        print("No bookings found for the selected date.")

    options()

def dWorker():
    sql= 'select* from Worker'
    cur= con.cursor()
    cur.execute(sql)
    d=cur.fetchall()
    for i in d:
        print(i)
    options()






def cust_signin():
    print("\n")
    print(" ----------------------->>>>>>>>>>>>>>>>Welcome, THANKS FOR CHOOSING OUR SYSTEM <<<<<<<<<<<<<-----------------------")
    print("\n")
    choices()
def choices():
    print("""
          1.   Book movie tickets 
          2.   Add food to your order 
          3.   Cancel Tickets 
          4.   Display my booking details 
          5.   Exit 
          """)
    choice= input("Select Option:")
    while True:
        if choice=='1':
            print("Currently Showing:")
            cur.execute("select*from MyShow")
            result=cur.fetchall()
            for row in result:
                print(row, '\n')
            book_tc()
        elif choice=='2':
            show_menu()
            ch=input(" How can we help you today? (1/2/3/4/5)")
            if ch=='1':
                view_menu()
            elif ch=='2':
                place_order()
            elif ch=='3':
                update_order()
            elif ch=='4':
                delete_order()
            elif ch=='5':
                search_order()
            elif ch=='6':
                break
            else:
                print("Enter Again.............")
                show_menu()
        elif choice=='3':
            del_tc()
        elif choice=='4':
            display()
        elif choice=='5':
            break
        else:
             print("Enter Again.............")
             choices()
            








def book_tc():
    m=int(input("enter movie id  "))
    n=input("Enter your name")
    num=int(input("Enter the number of tickets you would like to book: "))
    price=300*num
    for s in range(num):
        row=input("Select row (A/B/C/D/E/F)")
        seat=input("Enter seat number (1-20)")
        sn=row+seat
        q=("Select * from ticketing")
        cur.execute(q)
        data=cur.fetchall()
        if sn not in data:
            seat_no=sn
        else:
            print("Seat is booked")
    fetch_showtime_date_query = "SELECT ShowTime, Date FROM MyShow WHERE Movie_ID = %s"
    cur.execute(fetch_showtime_date_query, (m,))
    show_time, date = cur.fetchone()

    query = ("INSERT INTO ticketing (Seat_No, Name, Tickets, Ticket_Amount, Movie_ID, ShowTime, Date) "
             "VALUES ('{}', '{}', {}, {}, {}, '{}', '{}')".format(seat_no, n, num, price, m, show_time, date))

    cur.execute(query)
    show_id = cur.lastrowid
    print(f"Ticket booked successfully! Your Show ID is: {show_id}")
    con.commit()
    choices()

def del_tc():
    show_id=int(input("Enter your show ID"))
    query=("delete from ticketing where show_ID={}".format(show_id))
    cur.execute(query)
    con.commit()
    choices()

def display():
    show_id=int(input("Enter your show ID"))
    query=("Select * from ticketing where Show_ID='{}'".format(show_id))
    cur.execute(query)
    data=cur.fetchall()
    if len(data):
        for rec in data:
            for val in rec:
                print(val,end=' ')
            print()
    else:
        print("No record found")
    choices()
def show_menu():
    print("Welcome to the Theatre Food Counter!")
    print("1. View Menu")
    print("2. Place Order")
    print("3. Update Order")
    print("4. Delete Order")
    print("5. Search order")
    print("6. Exit")

def view_menu():
    menu = {'Popcorn': 200, 'Soda': 70, 'Hot Dog': 250, 'Nachos': 150, 'Candy': 30}
    print("Menu:")
    for item, price in menu.items():
        print(item + ": Rs. " + str(price))
    '''show_menu()'''

def place_order():
    menu = {'Popcorn': 200, 'Soda': 70, 'Hot Dog': 250, 'Nachos': 150, 'Candy': 30}

    order = []
    while True:
        item_name = input("Enter the name of the item (or 'done' to finish): ")
        if item_name.lower() == 'done':
            break
        if item_name in menu:
            item_quantity = int(input("Enter the quantity: "))
            order.append((item_name, item_quantity))
        else:
            print("Invalid item. Please try again.")
    

    total_price = 0.0
    print("Order:")
    for item, quantity in order:
        price = menu[item] * quantity
        formatted_menu_price = str(menu[item])
        formatted_price = str(price)
        print(item + ": " + str(quantity) + " x Rs. " + formatted_menu_price + " = Rs. " + formatted_price)
        total_price += price
    
    n = input("Enter your name: ")
    show_id = int(input("Enter the show ID: "))

    query = "INSERT INTO food (Name, Order_amount, SHOW_ID) VALUES (%s, %s, %s)"
    values = (n, total_price, show_id)
    cur.execute(query, values)
    Order_ID = cur.lastrowid
    print(f"Ticket booked successfully! Your Order ID is: {Order_ID}")
    con.commit()

    formatted_total_price = str(total_price)
    print("Total Price: Rs. ", formatted_total_price)
    print("Enjoy your food!")
    '''show_menu()'''
def update_order():
    order_id = int(input("Enter the order ID to update: "))
    item_name = input("Enter the updated item name: ")
    item_quantity = int(input("Enter the updated quantity: "))

    query = "UPDATE food SET Name = %s, Order_amount = %s WHERE Order_ID = %s"
    values = (item_name, item_quantity, order_id)
    cur.execute(query, values)

    con.commit()

    print("Order updated successfully!")
    '''show_menu()'''

def delete_order():
    order_id = int(input("Enter the order ID to delete: "))

    query = "DELETE FROM food WHERE Order_ID = %s"
    values = (order_id,)
    cur.execute(query, values)

    con.commit()

    print("Order deleted successfully!")
    '''show_menu()'''
def search_order():
    order_id = int(input("Enter the order ID to search: "))
    query = "SELECT * FROM food WHERE Order_ID = %s"
    values = (order_id,)
    cur.execute(query, values)
    
   
    result = cur.fetchall()
    if result:
        for row in result:
            print(row)
    else:
        print("Order not found.")
    
    

    '''show_menu()'''
print( "1.ADMIN")
print("2.USER")
print('3.EXIT')
ch= input("Enter your field:")
while True:
    if ch=='1':
        
        signin()
    elif ch=='2':
        cust_signin()
    elif ch=='3':
        exit




























