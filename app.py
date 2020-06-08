from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from flask_bootstrap import Bootstrap
import yaml

app = Flask(__name__)
bootstrap = Bootstrap(app)

# open db.yaml using yaml module
db = yaml.full_load(open('db.yaml'))
# instantiate an object for the MySQL module
mysql = MySQL(app)

# Configure the db
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


@app.route('/', methods=['GET', 'POST'])
def index():
	message = ''
	if request.method == "POST":
		try:
			name = request.form['uname']
			age = request.form['uage']

			# create a cursor by executing cursor function of db object
			cur = mysql.connection.cursor()

			query = "SELECT * FROM table_name WHERE name='" + name + "'"
			# take cursor object and call execute function to execute query
			count = cur.execute(query)
			
			if count > 0:
				message = "That name already exists. Choose another one."
			else:
				cur.execute("INSERT INTO table_name(name, age) VALUES(%s, %s)", (name, age))

				# commit the changes to the database
				mysql.connection.commit()

				# display the success message
				message = "Successfully added the details"

				# cleanup
				cur.close()
		except:
			message = "Failed to add details"
		
	return render_template("index.html", title="Home", message=message)


@app.route('/employees')
def employees():
	message = ''
	cur = mysql.connection.cursor()
	count = cur.execute("SELECT * FROM table_name")
	
	if count > 0:
		employees = cur.fetchall()
	else:
		employees = None
		message = "Currently no employees in the list"
		
	cur.close()
	return render_template("employees.html", title="Employees", employees=employees, message=message)

if __name__ == '__main__':
	app.run(debug=True)
	