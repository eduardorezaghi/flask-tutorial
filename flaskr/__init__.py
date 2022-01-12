import os

from flask import Flask

# >> $env:FLASK_APP="flaskr"
# >> $env:FLASK_ENV="development"


def create_app(test_config=None):
    # Cria e configura o app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flask.sqlite'),
    )

    if test_config is None:
        # Carrega a instância config, se existir, quando os testes estão desabilitados
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Carrega a configuração dos testes, se tudo certo
        app.config.from_mapping(test_config)

    # Garante que a pasta da instância do app exista
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Uma simples página que diz Hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    return app
