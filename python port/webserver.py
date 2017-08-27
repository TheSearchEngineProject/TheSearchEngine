from flask import Flask, request, url_for, redirect, render_template
from flask import session as term
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Admin, Data
import random
import string
from bcrypt import hashpw, gensalt
Search_engine = Flask(__name__)

engine = create_engine('sqlite:///Database.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# some functions to make password

# function to make salt used in password hashing

def make_pw_hash(pw):
    h = hashpw(pw.encode('utf8'), gensalt())
    return '%s' % (h)

def valid_pw(pw, h):
    return h == hashpw(pw.encode('utf8'), h)

# Redirect to Main page
@Search_engine.route('/')
def SearchBox():
    if not term.get('logged_in'):
        return redirect(url_for('LoginPage'))
    else:
        return redirect(url_for('AdminPage'))

# Signup functionality and page
@Search_engine.route('/signup', methods=['GET','POST'])
def SignupPage():
    error = None
    if term.get('logged_in'):
        return redirect(url_for('AdminPage'))
    else:
        if request.method == "POST":
            paswd = request.form['Password']
            repaswd = request.form['REPassword']

            email = request.form['Email']
            users = session.query(Admin).all()
            for i in users:
                if i.email == email:
                    error = "User already Exists!"
                    return render_template('Signup.html', error = error)

            if paswd == repaswd:
                key = request.form['Key']
                hashed = make_pw_hash(paswd)
                if key == "adminbanado":
                    newAdmin = Admin(name = request.form['Name'], email = email,
                                    password = hashed, power = "Admin")
                    session.add(newAdmin)
                    session.commit()
                    term['logged_in'] = True
                    return redirect(url_for('AdminPage'))
                else:
                    error = "Wrong Key!"
                    return render_template('Signup.html', error = error)
            else:
                error = "Password are not matching. Type again please!"
                return render_template('Signup.html', error = error)
        else:
            return render_template('Signup.html')

# Login functionality and page
@Search_engine.route('/login', methods=['GET','POST'])
def LoginPage():
    error = None
    if term.get('logged_in'):
        return redirect(url_for('AdminPage'))
    else:
        if request.method == "POST":
            email = request.form['Email']
            password = request.form['Password']
            users = session.query(Admin).all()
            for i in users:
                if email == i.email and valid_pw(i.password):
                    term['logged_in'] = True
                    return redirect(url_for('AdminPage'))
                else:
                    error = "Invalid Email or Password"
                    return render_template('login.html', error = error)
        else:
            return render_template('login.html', error = error)

# Logout functionality
@Search_engine.route('/logout')
def Logout():
    term.pop('logged_in', None)
    return redirect(url_for('LoginPage'))

# Admin page
@Search_engine.route('/admin')
def AdminPage():
    if term.get('logged_in'):
        return render_template('Admin_Page.html')
    else:
        return redirect(url_for('LoginPage'))

# Function to view all the users
@Search_engine.route('/admin/viewAdmins')
def ViewAdmins():
    if term.get('logged_in'):
        wholedata = session.query(Admin).order_by(asc(Admin.id))
        return render_template('viewAdmin.html', wholedata = wholedata)
    else:
        return redirect(url_for('LoginPage'))

# Function to view all the data of database
@Search_engine.route('/admin/viewdata')
def Viewdata():
    if term.get('logged_in'):
        wholedata = session.query(Data).order_by(asc(Data.Title))
        return render_template('viewdata.html', wholedata = wholedata)
    else:
        return redirect(url_for('LoginPage'))

# Function to add new data to database
@Search_engine.route('/admin/Newdata', methods=['GET','POST'])
def NewData():
    if term.get('logged_in'):
        if request.method == 'POST':
            newdata = Data(Title=request.form['Title'], name = request.form['Name'], website = request.form['Website'],
                            phoneno = request.form['phone_number'], description = request.form['Description'],
                            address = request.form['Address'])
            session.add(newdata)
            session.commit()
            return redirect(url_for('AdminPage'))
        else:
            return render_template('data-entry.html')
    else:
        return redirect(url_for('LoginPage'))

# Function to edit existing data in the database
@Search_engine.route('/admin/<int:data_id>/edit', methods = ['GET','POST'])
def EditData(data_id):
    if term.get('logged_in'):
        editeddata = session.query(Data).filter_by(id=data_id).one()
        if request.method == "POST":
            editeddata.Title = request.form['Title']
            editeddata.name = request.form['Name']
            editeddata.website = request.form['Website']
            editeddata.phoneno = request.form['phone_number']
            editeddata.description = request.form['Description']
            editeddata.address = request.form['Address']
            session.add(editeddata)
            session.commit()
            return redirect(url_for('Viewdata'))
        else:
            return render_template('Edit-data.html', data_id = data_id, editdata = editeddata)
    else:
        return redirect(url_for('LoginPage'))

# Function to delete a data from the database
@Search_engine.route('/admin/<int:data_id>/delete', methods = ['GET','POST'])
def DeleteData(data_id):
    if term.get('logged_in'):
        delete_data = session.query(Data).filter_by(id=data_id).one()
        if request.method == "POST":
            session.delete(delete_data)
            session.commit()
            return redirect(url_for('Viewdata'))
        else:
            return render_template('Delete-data.html', data = delete_data)
    else:
        return redirect(url_for('LoginPage'))

# Function to delete existing user in the database
@Search_engine.route('/Delete-User/<int:user_id>', methods = ['GET', 'POST'])
def DeleteUser(user_id):
    if term.get('logged_in'):
        deleteuser = session.query(Admin).filter_by(id = user_id).one()
        if request.method == "POST":
            session.delete(deleteuser)
            session.commit()
            return redirect(url_for('ViewAdmins'))
        else:
            return render_template('delete-user.html', data = deleteuser)
    else:
        return redirect(url_for('LoginPage'))

if __name__ == '__main__':
    Search_engine.secret_key = 'some secret key'
    Search_engine.debug = True
    Search_engine.run(host='0.0.0.0', port = 5000)
