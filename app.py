# -*- coding: utf-8 -*-

from flask import Flask, render_template, session, redirect, url_for, escape, request, g
import shelve, queue


app = Flask(__name__)


app.secret_key = 'any random string'

@app.before_first_request
def start():
	session['last_visited'] = []





@app.route('/',  methods  = ['GET', 'POST'])			# decorador, varia los parametros
def index():

	

	data_page = {
		'title' : 'pagina personal',
		'header_title': 'Soluciones Domótica',
		'header_subtitle' : 'Haciendo más facil la vida',
		'logo' : 'static/img/logo.png',
		'menu' : [
			('Home', '/'),
			('Contact', '/contact'),
			('About us', '/about'),

		],

		'last_visited' : session['last_visited']
	}

	



	

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

		#descripción inicial:
		descripcion = 'Esta es una descripción de mi usuario'
		#creamos una nueva instancia del user en la base de datos:
		data_base[user] = {'username': user, 'password': password, 'descripcion': descripcion}
		session['username'] = user

		#cerramos la base de datos:
		data_base.close()



	return(render_template('signup.html'))


@app.after_request
def store_visted_urls(response):
	if not request.url in session['last_visited']:
		if len(session['last_visited']) < 3 :
			session['last_visited'].append(request.url)
		else:
			session['last_visited'].pop(0)
			session['last_visited'].append(request.url)
	
	return response


	


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

	



@app.route('/logout')
def logout():
	# remove the username from the session if it is there
   session.pop('username', None)
   return redirect(url_for('index'))



#Permitimos al usuario visualizar los datos de su cuenta:
@app.route('/userInfo')
def user_info():
	#sacamos los datos del formulario:
	data_base = shelve.open('data_base.dat')
	user = data_base.get('username', None)

	data_page = {
			'user': user.username,
			'descripcion' : user.descripcion
	}

	render_template('user_info.html', data_page=data_page)



#Función en la cuál permitiremos al usuario modificar los datos de su cuenta:
@app.route('/setting')
def setting():

	return render_template('settings.html')


#Función para actualizar los datos del usuario:
@app.route('/update', methods =['GET', 'POST'])
def update_info():
	if(request.method == 'POST'):
		if request.form['password'] != request.form['confirm_password']:
			return render_template('setting.html', error=True)
		else:
			#sacamos los datos del formulario:
			data_base = shelve.open('data_base.dat')
			user = request.form['username']
			password = request.form['password']

			#descripción inicial:
			descripcion = request.form['descripcion']
			#creamos una nueva instancia del user en la base de datos:
			data_base[user] = {'username': user, 'password': password, 'descripcion': descripcion}
			session['username'] = user

			#cerramos la base de datos:
			data_base.close()
			return redirect(url_for(index))
			





if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)


