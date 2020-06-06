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

'''By default the cursor is created using the default cursor class. Different cursor class can be specified by setting the 'cursorclass' parameter to the cursor class needed. Use DictCursor to have results returned as Python dictionaries instead of the default which is a Python list.'''

app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# instantiate an object for the MySQL module
mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
	message = ''
	if request.method == "POST":
		name = request.form['uname']
		age = request.form['uage']
		
		# create a cursor by executing cursor function of db object
		cur = mysql.connection.cursor()
		
		query = "SELECT * FROM table_name WHERE name='" + name + "'"
		count = cur.execute(query)
		if count > 0:
			message = "That name already exists. Choose another one."
		else:
			# take cursor object and call execute function to execute query
			cur.execute("INSERT INTO table_name(name, age) VALUES(%s, %s)", (name, age))

			# commit the changes to the database
			mysql.connection.commit()

			# cleanup
			cur.close()
		
	return render_template("index.html", title="Form", message=message)

@app.route('/employees')
def employees():
	cur = mysql.connection.cursor()
	count = cur.execute("SELECT * FROM table_name")
	if count > 0:
		employees = cur.fetchall()
		cur.close()
		return render_template("employees.html", title="Employees", employees=employees)
	else: 
		message = "Currently no employees in the list"
		return render_template("employees.html", title="Employees", message=message)

if __name__ == '__main__':
	app.run(debug=True)
	