from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

# open db.yaml using yaml module
db = yaml.load(open('db.yaml'))

# Configure the db
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == "POST":
		name = request.form['uname']
		age = request.form['uage']
		val = "Registered user " + name + " of age " + age
		return val
	return render_template("index.html", title="Form")

if __name__ == '__main__':
	app.run(debug=True)
	