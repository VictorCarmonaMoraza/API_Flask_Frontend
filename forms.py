from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class PersonaForm(FlaskForm):
    #Campo requerido
    nombre = StringField('Nombre',validators =[DataRequired()])
    #Campo opcional
    apellido = StringField('Apellido')
    email = StringField('Email',validators =[DataRequired()])
    enviar = SubmitField('Enviar')