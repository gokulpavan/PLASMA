from flask import Flask , render_template , request,redirect,url_for,jsonify
import sqlite3
import os
import datetime
import json

cd = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)

app.secret_key = 'PLASMADONOR'




@app.route("/")
def index():
	
	return render_template("index.html",)



@app.route("/update",methods = ['POST'])
def update():
	name = request.form['name']
	email = request.form['email']
	phnum = request.form['phonenumber']
	bgrp = request.form['Bloodgroup']
	state = request.form['state']
	city = request.form['city']
	date = request.form['date']
	age = request.form['age']
	adddate = datetime.datetime.now()
	conn = sqlite3.connect(cd+"/plasmadonor.db")
	cursor = conn.cursor()
	query = f"""INSERT INTO plasmadonor VALUES('{name}','{email}',{phnum},'{bgrp}','{state}','{city}','{date}','{age}','{adddate}')"""
	try:
		cursor.execute(query)
		conn.commit()
		return f"""<h1 id="head1">Dear {name},
					<br>
					<br>
					Thank you for your generous Donation. We are thrilled to have your support. Through your donation we have been able to accomplish plasma donation and continue working towards donation of plasma. You truly make the difference for us, and we are extremely grateful!
					<br><br>
					Today your donation will help battle Covid-19. 
					<br><br>
					Sincerely,
					<br>
					Co-Plasma team</h1>"""

	except sqlite3.IntegrityError:
		return "Email already exist"
	except sqlite3.OperationalError:
		return 'Please fill the form completely'
	cursor.close()
	conn.close() 


@app.route("/<string:page_name>")

def html_page(page_name):
    return render_template(page_name)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/requirement_form',methods=['POST'])
def requirement_form():
		name = request.form['name']
		
		city = request.form['city']
		phnum = request.form['phonenumber']
		bgrp = request.form['Bloodgroup']
		adddate = datetime.datetime.now()
		getplasma = sqlite3.connect(cd+"/getplasma.db")
		query1 = f"""INSERT INTO getplasma VALUES('{name}',{phnum},'{bgrp}','{city}','{adddate}')"""
		cur = getplasma.cursor()
		try:
			result1 = cur.execute(query1)
			getplasma.commit()

		
		except sqlite3.OperationalError:
			return 'Please fill the form completely'
		result1.close()
		getplasma.close() 

		conn = sqlite3.connect(cd+"/plasmadonor.db")
		conn.row_factory = dict_factory
		cursor = conn.cursor()
		
		query = f"SELECT * from plasmadonor WHERE (bgroup = '{bgrp}'  AND City='{city}') ORDER BY datetime(adddate) "
		result = cursor.execute(query)
		m = result.fetchall()
		return json.dumps(m)
