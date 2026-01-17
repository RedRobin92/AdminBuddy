from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

print(f"--- ESTOY EJECUTANDO EL ARCHIVO EN: {__file__} ---")

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from datetime import datetime

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f'<Usuario {self.nombre}>'
    
class Transaccion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    monto = db.Column(db.Float, nullable=False)
    descripcion = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.String(10), nullable=False) # 'ingreso' o 'gasto'
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    def __repr__(self):
        return f'<Transaccion {self.tipo}: {self.monto}>'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/registro', methods=['POST'])
def registro():
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    email = request.form.get('email')

    usuario_existente = Usuario.query.filter_by(email=email).first()
    if usuario_existente:
        return f"<h1>El correo {email} ya se encuentra registrado,</h1><p>Por favor intente con otro correo</p>"
    
    try:
        nuevo_usuario = Usuario(nombre=nombre, apellido=apellido, email=email)
        db.session.add(nuevo_usuario)
        db.session.commit()

        return f"<h1>¡Gracias {nombre}!</h1><p>Te has registrado exitosamente con el correo {email}.</p>"
    except Exception as e:
        return "<h1>Hubo un problema</h1><p>No se pudo completar el registro. Por favor, inténtalo de nuevo más tarde.</p>"
    
@app.route('/dashboard')
def dashboard():
    transacciones = Transaccion.query.filter_by(user_id=1).all()  # Suponiendo que el usuario con ID 1 está logueado

    ingresos = 0.0
    gastos = 0.0

    for t in transacciones:
        if t.tipo == 'ingreso':
            ingresos += t.monto
        else:
            gastos += t.monto

    resumen ={
        'saldo': ingresos - gastos,
        'ingresos': ingresos,
        'gastos': gastos,
    }
    return render_template('dashboard.html', resumen=resumen, transacciones=transacciones)
    
if __name__ == '__main__':
    # debug=True permite que el servidor se reinicie solo cuando haga cambios en el codigo
    app.run(debug=True)

@app.route('/add_transaction', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        # 1. Capturamos los datos del formulario
        monto = request.form.get('monto')
        descripcion = request.form.get('descripcion')
        tipo = request.form.get('tipo')
        
        # 2. Creamos el registro en la base de datos
        # Nota: Por ahora usamos user_id=1 manualmente
        nueva_t = Transaccion(
            monto=float(monto), 
            descripcion=descripcion, 
            tipo=tipo, 
            user_id=1
        )
        
        db.session.add(nueva_t)
        db.session.commit()
        
        # 3. Redirigimos al Dashboard para ver el cambio
        return redirect(url_for('dashboard'))
    
    # Si es GET, simplemente mostramos el formulario
    return render_template('nueva_transaccion.html')

@app.route('/debug')
def debug_check():
    return "La ruta /debug funciona correctamente"

@app.route('/add_transaction', methods=['GET', 'POST'])
def add_transaction():
    try:
        if request.method == 'POST':
            monto = request.form.get('monto')
            descripcion = request.form.get('descripcion')
            tipo = request.form.get('tipo')
            
            # Forzamos un registro básico para probar
            nueva_t = Transaccion(
                monto=float(monto), 
                descripcion=descripcion, 
                tipo=tipo, 
                user_id=1
            )
            db.session.add(nueva_t)
            db.session.commit()
            return redirect(url_for('dashboard'))
        
        return render_template('nueva_transaccion.html')
    except Exception as e:
        return f"Error interno: {str(e)}"
    
if __name__ == '__main__':
    app.run(debug=true, port="5001")