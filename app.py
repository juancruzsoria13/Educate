from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de la base de datos (usar SQLite o PostgreSQL según se necesite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///educate.db'  # Para SQLite
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/educate'  # Para PostgreSQL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Definir el modelo para almacenar las respuestas
class Respuesta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contenido = db.Column(db.String(120), nullable=False)
    respuesta_usuario = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f'<Respuesta {self.id}>'

# Ruta principal
@app.route('/')
def home():
    return render_template('home.html')

# Ruta para explorar categorías
@app.route('/explore')
def explore():
    categories = ['Matemáticas', 'Ciencias', 'Historia']  # Ejemplo de categorías
    return render_template('explore.html', categories=categories)

# Ruta para mostrar contenido de una categoría
@app.route('/content/<category>')
def content(category):
    contents = ['Tema 1', 'Tema 2', 'Tema 3']  # Ejemplo de temas en cada categoría
    return render_template('content.html', category=category, contents=contents)

# Ruta para mostrar las preguntas de evaluación
@app.route('/evaluate/<content>', methods=['GET', 'POST'])
def evaluate(content):
    questions = [
        'Pregunta 1: ¿Cuál es la fórmula del área de un círculo?',
        'Pregunta 2: Define la segunda ley de Newton.',
        'Pregunta 3: Explica la diferencia entre prosa y poesía.'
    ]
    
    if request.method == 'POST':
        # Recoger las respuestas del formulario
        for i in range(1, len(questions) + 1):
            answer = request.form.get(f"answer_{i}")
            # Guardar cada respuesta en la base de datos
            respuesta = Respuesta(contenido=content, respuesta_usuario=answer)
            db.session.add(respuesta)
        db.session.commit()
        return redirect(url_for('progress'))

    return render_template('evaluation.html', content=content, questions=questions)

# Ruta para mostrar el progreso del usuario
@app.route('/progress')
def progress():
    # Obtener todas las respuestas de la base de datos
    respuestas = Respuesta.query.all()
    progress_data = {}
    for respuesta in respuestas:
        if respuesta.contenido not in progress_data:
            progress_data[respuesta.contenido] = 0
        progress_data[respuesta.contenido] += 1
    return render_template('progress.html', progress_data=progress_data)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crear las tablas de la base de datos
    app.run(debug=True)

