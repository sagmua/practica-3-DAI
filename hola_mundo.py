# -*- coding: utf-8 -*-

from flask import Flask, render_template, session, redirect, url_for, escape, request
app = Flask(__name__)


app.secret_key = 'any random string'

@app.route('/',  methods  = ['GET', 'POST'])                         # decorador, varia los parametros
def index():

	data_page = {

		'header_title': 'GRAN TITULO',
		'header_subtitle' : 'pequeño titulo',
		'logo' : 'static/img/carretera.jpg',
		'menu' : [
			('Home', '/'),
			('Contact', '/contact'),
			('About us', '/about')
		]

		
	}


	if request.method == 'POST':
		session['username'] = request.form['username']
		return redirect(url_for('index'))

	if 'username' in session:
		username = session['username']
		return render_template('welcome.html', data_page=data_page,logged=True)

	else:
		return render_template('welcome.html',data_page=data_page, logged=False)






	return render_template('welcome.html')



@app.route('/logout')
def logout():
	# remove the username from the session if it is there
   session.pop('username', None)
   return redirect(url_for('index'))


if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)

