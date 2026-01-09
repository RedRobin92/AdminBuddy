from flask import Flask, render_template
app = Flask(__name__)
@app.route('/')
def home():
    # Busca archivo "index.html" en templates
    return render_template('index.html')
if __name__ == '__main__':
    # debug=True permite que el servidor se reinicie solo cuando haga cambios en el codigo
    app.run(debug=True)
    