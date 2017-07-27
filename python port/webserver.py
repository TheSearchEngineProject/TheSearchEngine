from flask import Flask, request, url_for, redirect, render_template
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Admin, Data

Search_engine = Flask(__name__)

engine = create_engine('sqlite:///Database.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@Search_engine.route('/')
def SearchBox():
    return redirect(url_for('AdminPage'))

@Search_engine.route('/admin')
def AdminPage():
    return render_template('Admin_Page.html')

@Search_engine.route('/admin/viewdata')
def Viewdata():
    wholedata = session.query(Data).order_by(asc(Data.Title))
    return render_template('viewdata.html', wholedata = wholedata)

@Search_engine.route('/admin/Newdata', methods=['GET','POST'])
def NewData():
    if request.method == 'POST':
        newdata = Data(Title=request.form['Title'], name = request.form['Name'], website = request.form['Website'],
                        phoneno = request.form['phone_number'], description = request.form['Description'],
                        address = request.form['Address'])
        session.add(newdata)
        session.commit()
        return redirect(url_for('AdminPage'))
    else:
        return render_template('data-entry.html')

@Search_engine.route('/admin/<int:data_id>/edit', methods = ['GET','POST'])
def EditData(data_id):
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

@Search_engine.route('/admin/<int:data_id>/delete', methods = ['GET','POST'])
def DeleteData(data_id):
    delete_data = session.query(Data).filter_by(id=data_id).one()
    if request.method == "POST":
        session.delete(delete_data)
        session.commit()
        return redirect(url_for('Viewdata'))
    else:
        return render_template('Delete-data.html', data = delete_data)

if __name__ == '__main__':
    Search_engine.debug = True
    Search_engine.run(host='0.0.0.0', port = 5000)
