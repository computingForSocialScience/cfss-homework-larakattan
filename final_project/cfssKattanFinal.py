import pymysql
from flask import Flask, render_template, request, redirect, url_for
import flask
import numpy as np 
import pandas as pd 
import statsmodels.api as sm 
import statsmodels.formula.api as smf
import csv 



dbname="kattan"
host="localhost"
user="root"
passwd=""
db=pymysql.connect(db=dbname,host=host,user=user,passwd=passwd,charset='utf8',unix_socket="/tmp/mysql.sock",port=3306)

cur = db.cursor()


app = Flask(__name__)

cur.execute('''drop table data;''')
cur.execute('''drop table coefficients;''')

mysql_edu_data = '''CREATE TABLE IF NOT EXISTS data (state varchar(25),test VARCHAR(25),score VARCHAR(25), black VARCHAR(25), hispanic VARCHAR(25), FRL VARCHAR(25), income VARCHAR(25));'''
cur.execute(mysql_edu_data)

mysql_coefficients = '''CREATE TABLE IF NOT EXISTS coefficients (id INTEGER PRIMARY KEY AUTO_INCREMENT, constant FLOAT, black FLOAT, hispanic FLOAT, FRL FLOAT, income FLOAT);'''
cur.execute(mysql_coefficients)

db.commit()

@app.route('/', methods=['GET','POST'])
def make_index_resp():

	if request.method == 'GET':
		return(render_template('/index.html'))

	elif request.method == 'POST':
		formData = request.values
		variables = request.form.getlist('variables')
		NAEP = request.form.get('test')
		

		sql = "SELECT  " + "score," + ",".join(variables) + " FROM data WHERE test = %s"
		cur.execute(sql,(NAEP))

		f = open('/users/larakattan/cfss-homework-larakattan/final_project/analysis_data.csv','w')
		tempdata = csv.writer(f,delimiter=',')
		
		tempdata.writerow([i[0] for i in cur.description])

		for row in cur.fetchall():
			tempdata.writerow(row)

		f.close()


	return(redirect("/output/"))

@app.route('/output/')
def make_output_resp():

	coeffList = []

	coeffList = analyze_data();

	# order of coefficients: const, FRL, black, hispanic, income

	try:
		FRL = coeffList['FRL'] 
	except: 
		FRL = 'not included'

	try: 
		black = coeffList['black']
	except:
		black = 'not included'
	try: 
		hispanic = coeffList['hispanic']
	except:
		hispanic = 'not included'
	try:
		income = coeffList['income']
	except:
		income = 'not included'
	try: 
		constant = coeffList['const']
	except:
		constant ='not included'


	return render_template('output.html',constant=constant,FRL=FRL,black=black,hispanic=hispanic,income=income)

@app.route('/documentation/')
def make_documentation_resp():
	return render_template('documentation.html')


def load_data():
	# load the data file from CSV into mySQL
	load_data = '''LOAD DATA INFILE '~/cfss-homework-larakattan/final_project/cfssfinaldata.csv' INTO TABLE data FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r' IGNORE 1 ROWS;'''
	cur.execute(load_data)
	db.commit()

	return 


def analyze_data():
	df = pd.read_csv('~/cfss-homework-larakattan/final_project/analysis_data.csv')

	y = df.score
	X = df.ix[:,1:]
	X = sm.add_constant(X)

	est = sm.OLS(y,X)
	est = est.fit()

	# order of coefficients: const, FRL, black, hispanic, income
	params = est.params 

	print (est.params);

	return params;

load_data()

if __name__ == '__main__':
    app.debug=True
    app.run()
