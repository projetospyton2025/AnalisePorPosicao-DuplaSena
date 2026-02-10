"""
Aplicação Flask - Análise Por Posição Dupla Sena
"""
import os
from flask import Flask
from routes.main import main_bp


def create_app():
    """Factory para criar a aplicação Flask"""
    app = Flask(__name__)
    
    # Configurações
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
    app.config['JSON_AS_ASCII'] = False
    
    # Registra blueprints
    app.register_blueprint(main_bp)
    
    return app


if __name__ == '__main__':
    app = create_app()
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5051)
