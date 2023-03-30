from flask import Flask, render_template, request, url_for
from flask_migrate import Migrate
from werkzeug.utils import redirect

from database import db
from forms import PersonaForm
from models import Persona

app = Flask(__name__)

#Configuracion de la bd
USER_BD ='postgres'
PASS_DB = 'Vcarmona32'
URL_DB = 'localhost'
NAME_DB ='sap_flask_db'
FULL_URL_DB =f'postgresql://{USER_BD}:{PASS_DB}@{URL_DB}/{NAME_DB}'


app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db.init_app(app)

#configurar_flask-migrate
migrate = Migrate()
migrate.init_app(app, db)

#configuracion de flask-wtf
app.config['SECRET_KEY']='llave_secreta'

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def inicio():
    #Listado de personas Nos devolvera todos los objetos de tipo persona de nuestra BBDD
    personas = Persona.query.all()
    #Recuperar el numero de personas
    total_personas = Persona.query.count()
    #Imprimimos
    app.logger.debug(f'Listado Personas: {personas}')
    app.logger.debug(f'Total Personas: {total_personas}')
    #Renderizamos nuestra plantilla
    return render_template('index.html', persListadoHTML = personas, total_pHTML = total_personas)


@app.route('/ver/<int:id>')
def ver_detalle(id):
    #Recuperamos un objeto persona mediante el id proporcionado
    persona = Persona.query.get_or_404(id)
    app.logger.debug(f'Ver persona: {persona}')
    return render_template('detalle.html', personaVerDetalle =persona)

@app.route('/agregar', methods =['GET','POST'])
def agregar():
    #Instanciamos la clase Persona
    persona = Persona()
    personaForm = PersonaForm(obj = persona)
    #preguntamos si nuestro metodo es de tipo post
    if request.method == 'POST':
        # Preguntamos si el formulario es valido
        if personaForm.validate_on_submit():
            #Rellenamos el objeto persona
            personaForm.populate_obj(persona)
            app.logger.debug(f'Persona a insertar: {persona}')
            #Insertamos el nuevo registro
            db.session.add(persona)
            #Hacemos commit de la transaccion
            db.session.commit()
            #Redireccionamos a la pagina
            return redirect(url_for('inicio'))
    return render_template('agregar.html', forma = personaForm)
