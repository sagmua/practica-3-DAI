# -*- coding: utf-8 -*-

from flask import Flask, render_template, session, redirect, url_for, escape, request
import shelve, queue


app = Flask(__name__)


app.secret_key = 'any random string'


#creamos una variable que indique las últimas páginas visitadas:




@app.route('/',  methods  = ['GET', 'POST'])                         # decorador, varia los parametros
def index():

	session["last_visited"] = []

	data_page = {

		'header_title': 'Mi página personal',
		'header_subtitle' : 'pequeño titulo',
		'logo' : 'static/img/carretera.jpg',
		'menu' : [
			('Home', '/'),
			('Contact', '/contact'),
			('About us', '/about'),

		],

		'last_visited' : session["last_visited"]
	}

	if len(session["last_visited"])>0:
		return(len(session["last_visited"]))

	#comprobamos si el usuario y la contraseña introducidas coinciden con algún usuario del sistema:
	if request.method == 'POST':
		
		data_base = shelve.open("data_base.dat")
		user = data_base.get(request.form['username'], None)

		if user != None and user['username'] == request.form['password']:
			session['username'] = request.form['username']
			
			return redirect(url_for('index'))

	#Si esta logeado:
	if 'username' in session:
		username = session['username']
		return render_template('welcome.html', data_page=data_page,logged=True)

	#en caso de no estar registrado:
	else:
		return render_template('welcome.html',data_page=data_page, logged=False)



	return render_template('welcome.html')



@app.route('/about')
def about():
	return render_template('about.html')

#ruta para registrarse en caso de no estarlo:
@app.route('/signup', methods= ['GET', 'POST'])
def signup():
	if request.method == 'POST':
		#sacamos los datos del formulario:
		data_base = shelve.open('data_base.dat')
		user = request.form['username']
		password = request.form['password']

		#creamos una nueva instancia del user en la base de datos:
		data_base[user] = {'username': user, 'password': password}
		session[user] = user

		#cerramos la base de datos:
		data_base.close()



	return(render_template('signup.html'))


@app.after_request
def store_visted_urls(response):

	if len(session) >= 3:
		session["last_visited"].pop(0)
		session["last_visited"].append(request.url)
	else:
		session["last_visited"].append(request.url)

	return response


	


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

	



@app.route('/logout')
def logout():
	# remove the username from the session if it is there
   session.pop('username', None)
   return redirect(url_for('index'))


if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)


