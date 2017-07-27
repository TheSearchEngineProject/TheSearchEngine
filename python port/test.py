from flask import Flask, request, url_for, redirect, render_template, session
from sqlalchemy import create_engine, asc, exc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Admin, Data, UserAccounts

Search_engine = Flask(__name__)

engine = create_engine('sqlite:///Database.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
Session = DBSession()

@Search_engine.route('/login', methods=['GET', 'POST'])
def loginPage():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' and request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('AdminPage'))
    return render_template('loginPage.html', error=error)
@Search_engine.route('/')
def SearchBox():
    return redirect(url_for('loginPage'))

@Search_engine.route('/admin')
def AdminPage():
    return render_template('Admin_Page.html')

@Search_engine.route('/admin/viewdata')
def Viewdata():
    wholedata = Session.query(Data).order_by(asc(Data.Title))
    return render_template('viewdata.html', wholedata = wholedata)

@Search_engine.route('/admin/Newdata', methods=['GET','POST'])
def NewData():
    if request.method == 'POST':
        newdata = Data(Title=request.form['Title'], name = request.form['Name'], website = request.form['Website'],
                        phoneno = request.form['phone_number'], description = request.form['Description'],
                        address = request.form['Address'])
        Session.add(newdata)
        Session.commit()
        return redirect(url_for('AdminPage'))
    else:
        return render_template('data-entry.html')

@Search_engine.route('/admin/<int:data_id>/edit', methods = ['GET','POST'])
def EditData(data_id):
    editeddata = Session.query(Data).filter_by(id=data_id).one()
    if request.method == "POST":
        editeddata.Title = request.form['Title']
        editeddata.name = request.form['Name']
        editeddata.website = request.form['Website']
        editeddata.phoneno = request.form['phone_number']
        editeddata.description = request.form['Description']
        editeddata.address = request.form['Address']
        Session.add(editeddata)
        Session.commit()
        return redirect(url_for('Viewdata'))
    else:
        return render_template('Edit-data.html', data_id = data_id, editdata = editeddata)

@Search_engine.route('/admin/<int:data_id>/delete', methods = ['GET','POST'])
def DeleteData(data_id):
    delete_data = Session.query(Data).filter_by(id=data_id).one()
    if request.method == "POST":
        Session.delete(delete_data)
        Session.commit()
        return redirect(url_for('Viewdata'))
    else:
        return render_template('Delete-data.html', data = delete_data)
@Search_engine.route('/signup', methods=['GET', 'POST'])
def signupUsers():
    if session.get('username') == None:
        if request.method == 'POST':
            newUser = UserAccounts(username=request.form['inputName'],
                                   password=request.form['inputPassword'],
                                   mail=request.form['inputEmail'])
            Session.add(newUser)
            Session.commit()
            return redirect(url_for('AdminPage'))
    return render_template('signupPage.html')
if __name__ == '__main__':
    Search_engine.debug = True
    Search_engine.run(host='0.0.0.0', port = 5000)
