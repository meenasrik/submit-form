from flask import Flask, render_template, request

app = Flask(__name__)

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
	