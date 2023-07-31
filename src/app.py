from flask import Flask, render_template
from config import config

# Routes
from routes import Pais
from routes import Pilot
from routes import Formada
from routes import GranPremi
from routes import Temporada
from routes import Participa
from routes import Constructor

# Utils
from utils.Format import classes

from utils.error_handler import page_not_found, internal_server_error

app = Flask(__name__)
app.config['search'] = {}

@app.route('/')
def index():

    info = {
        'titol' : 'Aplicació de Gestió',
        'alumne' : 'Omar Briqa',
    }
    return render_template('index.html', 
                           data = info,
                           classes = classes)

if __name__ == "__main__":
    
    # Config
    app.config.from_object(config['development'])
    
    # Blueprints
    app.register_blueprint(Pais.main, url_prefix='/paissos')
    app.register_blueprint(Pilot.main, url_prefix='/pilots')
    app.register_blueprint(Formada.main, url_prefix='/formades')
    app.register_blueprint(Temporada.main, url_prefix='/temporades')
    app.register_blueprint(GranPremi.main, url_prefix='/granspremis')
    app.register_blueprint(Participa.main, url_prefix='/participants')
    app.register_blueprint(Constructor.main, url_prefix='/constructors')

    # Error handlers
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)
    
    # Run
    app.run()
