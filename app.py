import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Caminho absoluto para o banco SQLite dentro da pasta instance
db_path = os.path.join(app.root_path, 'instance', 'terreiros.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Terreiro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    segmento = db.Column(db.String(50), nullable=False)
    estado = db.Column(db.String(50), nullable=False)
    cidade = db.Column(db.String(50), nullable=False)
    bairro = db.Column(db.String(50), nullable=False)
    rua = db.Column(db.String(100), nullable=False)
    numero = db.Column(db.String(20), nullable=False)
    cep = db.Column(db.String(20), nullable=False)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        novo = Terreiro(
            nome=request.form['nome'],
            segmento=request.form['segmento'],
            estado=request.form['estado'],
            cidade=request.form['cidade'],
            bairro=request.form['bairro'],
            rua=request.form['rua'],
            numero=request.form['numero'],
            cep=request.form['cep']
        )
        db.session.add(novo)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('cadastro.html')

@app.route('/busca')
def busca():
    query = request.args
    resultados = Terreiro.query
    for campo in ['cep', 'estado', 'cidade', 'bairro', 'rua']:
        if query.get(campo):
            resultados = resultados.filter(getattr(Terreiro, campo).ilike(f"%{query[campo]}%"))
    resultados = resultados.all()
    return render_template('busca.html', resultados=resultados)

@app.route('/orixas')
def orixas():
    return render_template('orixas.html')

if __name__ == '__main__':
    # Cria pasta instance se não existir
    if not os.path.exists(os.path.join(app.root_path, 'instance')):
        os.makedirs(os.path.join(app.root_path, 'instance'))
    with app.app_context():
        db.create_all()
    app.run(debug=True)