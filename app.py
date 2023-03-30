from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)

#Configuracion de la bd
USER_BD ='postgres'
PASS_DB = 'Vcarmona32'
URL_DB = 'localhost'
NAME_DB ='sap_flask_db'
FULL_URL_DB =f'postgresql://{USER_BD}:{PASS_DB}@{URL_DB}/{NAME_DB}'


app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

#Inicializazcion del objeto db de sqlalchemy
db =SQLAlchemy(app)

#configurar_flask-migrate
migrate = Migrate()
migrate.init_app(app, db)

#configuracion de flask-wtf
app.config['SECRET_KEY']='llave_secreta'


class Persona(db.Model):
    #Definimos las columnas indicando el tipo de dato
    id = db.Column(db.Integer, primary_key =True)
    nombre = db.Column(db.String(250))
    apellido = db.Column(db.String(250))
    email = db.Column(db.String(250))


    def __str__(self):
        return (
            f'Id: {self.id}'
            f'Nombre: {self.nombre}'
            f'Apellido: {self.apellido}'
            f'Email: {self.email}'
        )


class PersonaForm(FlaskForm):
    #Campo requerido
    nombre = StringField('Nombre',validators =[DataRequired()])
    #Campo opcional
    apellido = StringField('Apellido')
    email = StringField('Email',validators =[DataRequired()])
    enviar = SubmitField('Enviar')

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
