from re import template
from flask import render_template, send_file, session, redirect, send_file
from flask.globals import request
import qrcode
import datetime
import cv2
import os

users = dict()
active_user = dict()
work_seconds = dict()

def decode(path):
    detector = cv2.QRCodeDetector()
    res, _, _ = detector.detectAndDecode(cv2.imread(path))
    return res

def home():
    return render_template('home.html')


def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']

        if name in users:
            if users[name][0] ==  password:
                session['id'] = name
                active_user[session['id']] = datetime.datetime.now()
                return redirect('/logged_in')
            else:
                return 'wrong password'

        if "qr" in request.files:
            img = request.files["qr"]
            if img:
                path = "./uploads/" + img.filename
                img.save(path)
                data = decode(path).lstrip("(").rstrip(")").split(",")
                data = [val.strip().strip("'") for val in data]
                name, password, email, dob = data
                session['id'] = name
                active_user[session['id']] = datetime.datetime.now()
                return redirect("/logged_in")
        else:
            return 'user not found'
    return render_template('login.html')

 
def register():
    if request.method == 'GET':
        return render_template('register.html')

    elif request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        dob = request.form['birthday']

        if name in users:
            return 'user already exists'
        else:
            users[name] = (password, email, dob)
            tmp = (name, password, email, dob)
            data = str(tmp)
            qrcode.make(data).save("./static/myqr.png")
            employee_data = dict()

            employee_data['email'] = users[name][1]
            employee_data['dob'] = users[name][2]

            employee_data['qr_str'] = "localhost:5000/scan/"+name
            employee_data['qr_path'] = 'static/myqr.png'

            return render_template('profile.html', emp_data = employee_data)
    else:
        return 'wrong request'

def profile():
    name = session['id']
    employee_data = dict()

    employee_data['email'] = users[name][1]
    employee_data['dob'] = users[name][2]

    employee_data['qr_str'] = "localhost:5000/scan/"+name
    employee_data['qr_path'] = 'static/myqr.png'

    return render_template('profile.html', emp_data = employee_data)

def logged_in():
    if request.method == 'GET':
        name = session['id']
        employee_data = dict()

        employee_data['email'] = users[name][1]
        employee_data['dob'] = users[name][2]

        return render_template('logged_in.html',emp_data = employee_data);
    
    elif request.method == 'POST':
        id = session['id']
        
        if "qr" in request.files:
            if id not in users:
                return 'user not found!'

            # if id in active_user:   # user already have logged in.
            timeout = datetime.datetime.now()
            difference = timeout - active_user[id]
            if id not in work_seconds:                    
                work_seconds[id] = 0
            work_seconds[id] = work_seconds[id] + difference.seconds
                # del active_user[id]
                # session.pop("id")
            return f'user logged out. Active session time: {str(difference.seconds)}'

        return "Please upload your code!"

def download():
    return send_file("./static/myqr.png", as_attachment=True)
