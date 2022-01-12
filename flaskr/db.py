import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    # 'g': variável especial que é único para
    # cada requisição de recurso 

    # Se a conexão com o banco não existir, crie:
    if 'db' not in g:
        # [...] sqlite3.connect() realiza a conexão
        # entre o arquivo criado do banco 
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # diz para a conexão retornar as linhas 
        # que possuem comportamento de dicionários, para
        # ser possível acessar o valor pela chave
        # (chave:valor)
        g.db.row_factory = sqlite3.Row

    # Retorne a conexão criada ou pré-existente
    return g.db

# Encerra a conexão criada por get_db()
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

# Inicializa uma nova tabela no banco.
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Limpa dados pré-existentes e cria uma nova tabela no banco."""
    init_db()
    click.echo('Banco de dados inicializado.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
