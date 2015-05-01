import pymysql
import flask
import numpy as np 
import matplotlib
import matplotlib.pyplot as plt 

dbname=""
host="localhost"
user="root"
passwd=""
db=pymysql.connect(db=dbname,host=host,user=user,passwd=passwd,charset='utf8',unix_socket="/tmp/mysql.sock", port=3306)
cur = db.cursor()

app = Flask(__name__)

@app.route('/')
def make_index_resp():
    # this function just renders templates/index.html when
    # someone goes to http://127.0.0.1:5000/
    return(render_template('index.html'))
    