from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

DB_PATH = "meu_banco.db"

# Cria o banco e a tabela caso ainda não existam
def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        conn.execute("""
            CREATE TABLE usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    init_db()
    conn = get_db_connection()
    usuarios = conn.execute('SELECT * FROM usuarios').fetchall()
    conn.close()
    return render_template('index.html', usuarios=usuarios)

@app.route('/add', methods=['POST'])
def add():
    nome = request.form['nome']
    conn = get_db_connection()
    conn.execute('INSERT INTO usuarios (nome) VALUES (?)', (nome,))
    conn.commit()
    conn.close()
    return 'Usuário adicionado! <a href="/">Voltar</a>'

if __name__ == '__main__':
    # O Render usa porta 10000; localmente você pode acessar em 5000
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
