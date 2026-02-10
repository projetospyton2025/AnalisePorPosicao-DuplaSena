"""
Rotas principais da aplicação Dupla Sena
"""
from flask import Blueprint, render_template, request, jsonify
from services.fetcher import DuplaSenaService
from services.analisador import AnalisadorService

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Página inicial"""
    return render_template('index.html')


@main_bp.route('/analise')
def analise():
    """Página de análise"""
    return render_template('analise.html')


@main_bp.route('/api/buscar-concurso/<int:numero>')
def buscar_concurso(numero):
    """API para buscar um concurso específico"""
    service = DuplaSenaService()
    concurso = service.buscar_concurso(numero)
    
    if concurso:
        return jsonify(concurso.to_dict())
    else:
        return jsonify({'erro': 'Concurso não encontrado'}), 404


@main_bp.route('/api/ultimo-concurso')
def ultimo_concurso():
    """API para buscar o último concurso"""
    service = DuplaSenaService()
    concurso = service.buscar_ultimo_concurso()
    
    if concurso:
        return jsonify(concurso.to_dict())
    else:
        return jsonify({'erro': 'Erro ao buscar concurso'}), 500


@main_bp.route('/api/analisar', methods=['POST'])
def analisar():
    """API para realizar análise por posição"""
    data = request.get_json()
    
    inicio = data.get('inicio')
    fim = data.get('fim')
    quantidade = data.get('quantidade')
    
    service = DuplaSenaService()
    
    # Busca concursos
    if inicio and fim:
        concursos = service.buscar_multiplos_concursos(int(inicio), int(fim))
    elif quantidade:
        concursos = service.buscar_ultimos_n_concursos(int(quantidade))
    else:
        return jsonify({'erro': 'Parâmetros inválidos'}), 400
    
    if not concursos:
        return jsonify({'erro': 'Nenhum concurso encontrado'}), 404
    
    # Realiza análise
    analisador = AnalisadorService(concursos)
    resultado = analisador.obter_analise_completa()
    
    # Adiciona sugestões
    resultado['sugestoes_sorteio1'] = analisador.obter_sugestoes(1)
    resultado['sugestoes_sorteio2'] = analisador.obter_sugestoes(2)
    
    return jsonify(resultado)


@main_bp.route('/api/sugestoes')
def sugestoes():
    """API para obter sugestões baseadas em análise histórica"""
    quantidade = request.args.get('quantidade', 50, type=int)
    
    service = DuplaSenaService()
    concursos = service.buscar_ultimos_n_concursos(quantidade)
    
    if not concursos:
        return jsonify({'erro': 'Erro ao buscar concursos'}), 500
    
    analisador = AnalisadorService(concursos)
    
    return jsonify({
        'sorteio_1': analisador.obter_sugestoes(1),
        'sorteio_2': analisador.obter_sugestoes(2),
        'total_concursos': len(concursos)
    })
