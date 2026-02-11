"""
Rotas principais da aplicação Federal
"""
from flask import Blueprint, render_template, jsonify, request
from services.fetcher import FederalService
from services.analisador import AnalisadorService
from services.gerador_palpites import GeradorPalpitesService
from models.federal import Concurso

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Página inicial"""
    return render_template('index.html')

@main_bp.route('/analise')
def analise():
    """Página de análise estatística"""
    return render_template('analise.html')

@main_bp.route('/palpites')
def palpites():
    """Página de geração de palpites"""
    return render_template('palpites.html')

@main_bp.route('/api/ultimo-concurso')
def api_ultimo_concurso():
    """API: Retorna dados do último concurso"""
    try:
        dados = FederalService.buscar_ultimo_concurso()
        if dados:
            concurso = Concurso.from_api_response(dados)
            return jsonify({
                'success': True,
                'concurso': {
                    'numero': concurso.numero,
                    'data_apuracao': concurso.data_apuracao,
                    'premios': [
                        {
                            'posicao': p.posicao,
                            'numero': p.numero,
                            'serie': p.serie,
                            'valor': p.valor,
                            'ganhadores': p.ganhadores
                        }
                        for p in concurso.premios
                    ],
                    'proximo_concurso': concurso.proximo_concurso,
                    'data_proximo_concurso': concurso.data_proximo_concurso
                }
            })
        return jsonify({'success': False, 'erro': 'Não foi possível buscar os dados'}), 500
    except Exception as e:
        return jsonify({'success': False, 'erro': str(e)}), 500

@main_bp.route('/api/buscar-concurso/<int:numero>')
def api_buscar_concurso(numero):
    """API: Busca um concurso específico"""
    try:
        dados = FederalService.buscar_concurso(numero)
        if dados:
            concurso = Concurso.from_api_response(dados)
            return jsonify({
                'success': True,
                'concurso': {
                    'numero': concurso.numero,
                    'data_apuracao': concurso.data_apuracao,
                    'premios': [
                        {
                            'posicao': p.posicao,
                            'numero': p.numero,
                            'serie': p.serie,
                            'valor': p.valor
                        }
                        for p in concurso.premios
                    ]
                }
            })
        return jsonify({'success': False, 'erro': 'Concurso não encontrado'}), 404
    except Exception as e:
        return jsonify({'success': False, 'erro': str(e)}), 500

@main_bp.route('/api/gerar-palpites', methods=['POST'])
def api_gerar_palpites():
    """API: Gera palpites baseados em análise"""
    try:
        quantidade = request.json.get('quantidade', 5) if request.json else 5
        
        # Busca dados históricos para análise
        dados = FederalService.buscar_ultimo_concurso()
        if not dados:
            return jsonify({'success': False, 'erro': 'Não foi possível buscar dados'}), 500
        
        # Extrai números dos últimos concursos (simplificado - idealmente buscaria múltiplos)
        numeros = dados.get('listaDezenas', [])
        
        # Análise
        frequencias = AnalisadorService.analisar_frequencia_digitos(numeros)
        soma_stats = AnalisadorService.analisar_soma_numeros(numeros)
        
        dados_analise = {
            'frequencia_digitos': frequencias,
            'numeros_recentes': numeros,
            'soma_numeros': soma_stats
        }
        
        # Gera palpites
        palpites = GeradorPalpitesService.gerar_palpites(dados_analise, quantidade)
        
        return jsonify({
            'success': True,
            'palpites': [
                {
                    'numero': p.numero,
                    'estrategia': p.estrategia,
                    'confianca': p.confianca,
                    'justificativa': p.justificativa
                }
                for p in palpites
            ]
        })
    except Exception as e:
        return jsonify({'success': False, 'erro': str(e)}), 500
