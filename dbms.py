#http://127.0.0.1:5000/

from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import random
app = Flask(__name__)


#change it to connect to your mysql data base!!
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = <PASSWORD>
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_DB'] = 'hotel_management'

mysql = MySQL(app)

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/')
def options():
    return render_template('options.html')

#Aishwarya
@app.route('/create_user/',methods = ['POST', 'GET'])
def create_user():
    cur = mysql.connection.cursor()
    try:
        cur.execute("CREATE TABLE User (ID VARCHAR(5) NOT NULL PRIMARY KEY, staff BOOLEAN DEFAULT false , firstName  VARCHAR(40),lastName VARCHAR(20), address VARCHAR(20), contactNo BIGINT(10), email VARCHAR(40),cost INT(6) DEFAULT 2000)")
    except:
        print("Already exists!")
    if request.method == 'POST':
        uid=random.randint(1000, 2000)
        f_name = request.form['Name']
        l_name = request.form['LastName']
        try:
            request.form['Staff']
            staff = 1
        except:
            staff = 0
        address = request.form['Address']
        contact_no = request.form['Number']
        email_id = request.form['Email']
        cur.execute(f"INSERT INTO User VALUES('{uid}','{staff}','{f_name}','{l_name}','{address}','{contact_no}','{email_id}','0')")
        mysql.connection.commit()
        cur.close()
        return redirect('/get_users/')
    else:
        return render_template('Users/CreateUser.html')


@app.route('/update_user/',methods = ['POST', 'GET'])
def update_user():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        uid = request.form['ID']
        f_name = request.form['Name']
        l_name = request.form['LastName']
        try:
            staff_temp = request.form['Staff']
        except:
            staff_temp = 'off'
        if staff_temp == 'on':
            staff = 1
        else:
            staff = 0
        address = request.form['Address']
        contact_no = request.form['Number']
        email_id = request.form['Email']
        cur.execute(f"UPDATE User SET staff ='{staff}', firstName = '{f_name}',lastName = '{l_name}', address= '{address}',contactNo='{contact_no}',email='{email_id}',cost='0' WHERE ID='{uid}'")
        mysql.connection.commit()
        cur.close()
        return redirect('/get_users/')
    else:
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT * FROM User")
        rv = cur.fetchall()
        data = rv
        mysql.connection.commit()
        cur.close()
        return render_template('Users/UpdateUser.html',data=data)

@app.route('/delete/', methods = ['GET','POST'])
def delete_user():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        uid = request.form['ID']
        cur.execute(f"DELETE FROM User WHERE ID='{uid}'")
        mysql.connection.commit()
        cur.close()
        return redirect('/get_users/')
    else:
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT * FROM User")
        rv = cur.fetchall()
        data = rv
        mysql.connection.commit()
        cur.close()
        return render_template('Users/Delete.html',data=data)

@app.route('/get_users_with_rooms/')
def retrieve_with_room():
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT User.ID,User.Staff,User.firstName,User.lastName,User.address,User.contactNo,User.email,User.cost, Rooms.room_number,Rooms.room_type FROM User INNER JOIN Rooms ON User.ID=Rooms.ID")
    rv = cur.fetchall()
    data = rv
    mysql.connection.commit()
    cur.close()
    return render_template('Users/GetUsersWithRooms.html',data=data)

@app.route('/get_users/')
def retrieve_all():
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM User")
    rv = cur.fetchall()
    data = rv
    mysql.connection.commit()
    cur.close()
    return render_template('Users/GetUsers.html',data=data)

#Taniya
@app.route('/get_services/', methods = ['GET','POST'])
def retrieve_services():
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM Services")
    rv = cur.fetchall()
    data = rv
    mysql.connection.commit()
    cur.close()
    return render_template('Services/GetServices.html',data=data)

@app.route('/services/', methods = ['GET','POST'])
def create_services():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        try:
            cur.execute("CREATE TABLE Services(ServiceID VARCHAR(5) NOT NULL, ID VARCHAR(5), services VARCHAR(50), Cost INT(10) DEFAULT 0, PRIMARY KEY (ServiceID), FOREIGN KEY (ID) REFERENCES User(ID))")
        except:
            print("Already exists")
        service_id = random.randint(1000, 2000)
        user_id = request.form['ID']
        services = request.form['Service']
        cost = request.form['Cost']
        cur.execute(f"INSERT INTO Services VALUES('{service_id}','{user_id}','{services}','{cost}')")
        mysql.connection.commit()
        cur.close()
        return redirect('/get_services/')
    else:
        return render_template('Services/CreateService.html')

@app.route('/update_services/', methods = ['GET','POST'])
def update_services():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        service_id = request.form['ServiceID']
        user_id = request.form['ID']
        services = request.form['Service']
        cost = request.form['Cost']
        cur.execute(f"UPDATE Services SET ID='{user_id}', services='{services}', Cost='{cost}' WHERE ServiceID='{service_id}'")
        mysql.connection.commit()
        cur.close()
        return redirect('/get_services/')
    else:
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT * FROM Services")
        rv = cur.fetchall()
        data = rv
        mysql.connection.commit()
        cur.close()
        return render_template('Services/UpdateService.html',data=data)

@app.route('/delete_service/', methods = ['GET','POST'])
def delete_service():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        uid = request.form['ID']
        cur.execute(f"DELETE FROM Services WHERE ServiceID='{uid}'")
        mysql.connection.commit()
        cur.close()
        return redirect('/get_services/')
    else:
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT * FROM Services")
        rv = cur.fetchall()
        data = rv
        mysql.connection.commit()
        cur.close()
        return render_template('Services/DeleteService.html',data=data)

#Sanika
@app.route('/create_room/', methods = ['GET','POST'])
def create_room():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        try:
            cur.execute("CREATE TABLE Rooms(room_number INT(5) NOT NULL, room_type VARCHAR(40),services BOOLEAN, ID VARCHAR(5), PRIMARY KEY (room_number),FOREIGN KEY (ID) REFERENCES User(ID) )")
        except:
            print("Already exists")
        rno = request.form['RoomNo']
        u_id = request.form['ID']
        rtype = request.form['RoomType']
        try:
            s_availed_temp = request.form['Services']
        except:
            s_availed_temp = 'off'
        if s_availed_temp == 'on':
            services = 1
        else:
            services = 0
        cur.execute(f"INSERT INTO Rooms VALUES('{rno}','{rtype}','{services}','{u_id}')")
        mysql.connection.commit()
        cur.close()
        return redirect('/get_rooms/')
    else:
        return render_template('Rooms/CreateRoom.html')

@app.route('/get_rooms/', methods = ['GET','POST'])
def retrieve_rooms():
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM Rooms")
    rv = cur.fetchall()
    data = rv
    mysql.connection.commit()
    cur.close()
    return render_template('Rooms/GetRooms.html',data=data)

@app.route('/update_rooms/', methods = ['GET','POST'])
def update_rooms():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        rno = request.form['RoomNo']
        u_id = request.form['ID']
        rtype = request.form['RoomType']
        try:
            s_availed_temp = request.form['Services']
        except:
            s_availed_temp = 'off'
        if s_availed_temp == 'on':
            services = 1
        else:
            services = 0
        cur.execute(f"UPDATE Rooms SET room_type='{rtype}', services='{services}', ID='{u_id}' WHERE room_number='{rno}'")
        mysql.connection.commit()
        cur.close()
        return redirect('/get_rooms/')
    else:
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT * FROM Rooms")
        rv = cur.fetchall()
        data = rv
        mysql.connection.commit()
        cur.close()
        return render_template('Rooms/UpdateRoom.html',data=data)

@app.route('/delete_rooms/', methods = ['GET','POST'])
def delete_rooms():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        rno = request.form['RoomNo']
        cur.execute(f"DELETE FROM rooms WHERE room_number='{rno}'")
        mysql.connection.commit()
        cur.close()
        return redirect('/get_rooms/')
    else:
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT * FROM rooms")
        rv = cur.fetchall()
        data = rv
        mysql.connection.commit()
        cur.close()
        return render_template('Rooms/DeleteRoom.html',data=data)

#Rupali
@app.route('/create_food/', methods = ['GET','POST'])
def create_food():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        try:
            cur.execute("CREATE TABLE FoodMenu (ItemName  VARCHAR(40),Cost INT(10), ID VARCHAR(5), FOREIGN KEY (ID) REFERENCES User(ID))")
        except:
            print("Already exists")
        ordered_by = request.form['OrderedBy']
        i_name = request.form['ItemName']
        cost = request.form['Cost']
        cur.execute(f"INSERT INTO FoodMenu VALUES('{i_name}','{cost}','{ordered_by}')")
        mysql.connection.commit()
        cur.close()
        return redirect('/get_food/')
    else:
        return render_template('Food/CreateFood.html')

@app.route('/get_food/', methods = ['GET','POST'])
def retrieve_menu():
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM FoodMenu")
    rv = cur.fetchall()
    data = rv
    mysql.connection.commit()
    cur.close()
    return render_template('Food/GetFood.html',data=data)

@app.route('/update_food/', methods = ['GET','POST'])
def update_food():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        i_name = request.form['ItemName']
        cost = request.form['Cost']
        cur.execute(f"UPDATE FoodMenu SET Cost='{cost}' WHERE ItemName='{i_name}'")
        mysql.connection.commit()
        cur.close()
        return redirect('/get_food/')
    else:
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT * FROM FoodMenu")
        rv = cur.fetchall()
        data = rv
        mysql.connection.commit()
        cur.close()
        return render_template('Food/UpdateFood.html',data=data)

@app.route('/delete_food/', methods = ['GET','POST'])
def delete_food():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        i_name = request.form['OrderedBy']
        cur.execute(f"DELETE FROM FoodMenu WHERE ID='{i_name}'")
        mysql.connection.commit()
        cur.close()
        return redirect('/get_food/')
    else:
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT * FROM FoodMenu")
        rv = cur.fetchall()
        data = rv
        mysql.connection.commit()
        cur.close()
        return render_template('Food/DeleteFood.html',data=data)


if __name__ == '__main__':
    app.run(debug=True)
