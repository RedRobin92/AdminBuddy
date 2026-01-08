from flask import Flask
app = Flask(__name__)
@app.route('/')
def home():
    # Return es lo que el servidor le envia al navegador
    return "<h1>Servidor de Finanzas Activo</h1><p>Hola Daniel, el entorno funciona.</p>"
if __name__ == '__main__':
    # debug=True permite que el servidor se reinicie solo cuando haga cambios en el codigo
    app.run(debug=True)
    