"""
Loteria Federal - Aplicação Flask
Análise e geração de palpites para Loteria Federal
"""
import os
from flask import Flask
from routes.main import main_bp

def create_app():
    """Cria e configura a aplicação Flask"""
    app = Flask(__name__)
    
    # Configurações
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['JSON_AS_ASCII'] = False
    
    # Registra blueprints
    app.register_blueprint(main_bp)
    
    return app

app = create_app()

if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)
