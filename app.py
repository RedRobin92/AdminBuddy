from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/registro', methods=['POST'])
def registro():
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    email = request.form.get('email')

    print(f"Nuevo registro: {nombre} {apellido} - Email: {email}")

    return f"<h1>¡Gracias {nombre}!</h1><p>Te has registrado exitosamente con el correo {email}.</p>"

if __name__ == '__main__':
    # debug=True permite que el servidor se reinicie solo cuando haga cambios en el codigo
    app.run(debug=True)