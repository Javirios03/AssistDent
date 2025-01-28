from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
DATABASE = 'data/pacientes.db'


# Inicializar BBDD
def init_db():
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pacientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                fecha_nacimiento TEXT NOT NULL,
                email TEXT NOT NULL,
                telefono TEXT NOT NULL,
                diagnostico TEXT NOT NULL,
                fecha_revision TEXT NOT NULL
            )
        """)
        conn.commit()


def borrar_datos():
    '''
    Borra todos los registros de la tabla pacientes
    '''
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM pacientes")
        conn.commit()


@app.route('/', methods=['GET', 'POST'])
def formulario():
    if request.method == 'POST':
        nombre = request.form['nombre']
        fecha_nacimiento = request.form['fecha_nacimiento']
        email = request.form.get("email")
        telefono = request.form.get("telefono")
        diagnostico = request.form.get("diagnostico")
        fecha_revision = request.form.get("fecha_revision")

        # Mandar a BBDD en posteriores versiones
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO pacientes (nombre, fecha_nacimiento, email, telefono, diagnostico, fecha_revision)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (nombre, fecha_nacimiento, email, telefono, diagnostico, fecha_revision))
            conn.commit()

        return redirect(url_for('gracias'))
    return render_template('formulario.html')


@app.route('/gracias')
def gracias():
    return "Gracias por rellenar el formulario. Los datos han sido guardados."


@app.route('/listado')
def listado():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pacientes")
        pacientes = cursor.fetchall()
    return render_template('listado.html', pacientes=pacientes)


# if __name__ == '__main__':
#     init_db()
#     # borrar_datos()  # Descomentar para borrar datos de la tabla
#     app.run(debug=True)
