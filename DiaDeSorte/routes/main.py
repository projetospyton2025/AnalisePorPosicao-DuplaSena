from flask import Blueprint, render_template, jsonify, request
from services.fetcher import DiaDeSorteService
from services.analisador import AnalisadorService
from services.gerador_palpites import GeradorPalpitesService

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Página inicial"""
    concurso = DiaDeSorteService.buscar_ultimo_concurso()
    return render_template('index.html', concurso=concurso)

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
    """API: Retorna o último concurso"""
    concurso = DiaDeSorteService.buscar_ultimo_concurso()
    
    if not concurso:
        return jsonify({'erro': 'Não foi possível buscar o último concurso'}), 500
    
    return jsonify({
        'numero': concurso.numero,
        'data_sorteio': concurso.data_sorteio,
        'dezenas': concurso.dezenas,
        'dezenas_ordem_sorteio': concurso.dezenas_ordem_sorteio,
        'mes_sorte': concurso.mes_sorte,
        'acumulado': concurso.acumulado,
        'valor_acumulado_proximo': concurso.valor_acumulado_proximo,
        'data_proximo_concurso': concurso.data_proximo_concurso,
        'numero_proximo_concurso': concurso.numero_proximo_concurso
    })

@main_bp.route('/api/analise-estatistica')
def api_analise_estatistica():
    """API: Retorna análise estatística completa"""
    try:
        limite = int(request.args.get('limite', 100))
        
        frequencia_dezenas = AnalisadorService.analisar_frequencia_dezenas(limite)
        distribuicao_faixas = AnalisadorService.analisar_distribuicao_faixas(limite)
        meses_sorte = AnalisadorService.analisar_meses_sorte(limite)
        
        # Ordena frequência de dezenas
        frequencia_ordenada = sorted(
            [{'dezena': k, 'frequencia': v} for k, v in frequencia_dezenas.items()],
            key=lambda x: x['frequencia'],
            reverse=True
        )
        
        # Ordena meses da sorte
        meses_ordenados = sorted(
            [{'mes': k, 'frequencia': v} for k, v in meses_sorte.items()],
            key=lambda x: x['frequencia'],
            reverse=True
        )
        
        return jsonify({
            'frequencia_dezenas': frequencia_ordenada,
            'distribuicao_faixas': distribuicao_faixas,
            'meses_sorte': meses_ordenados,
            'concursos_analisados': limite
        })
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@main_bp.route('/api/gerar-palpites', methods=['POST'])
def api_gerar_palpites():
    """API: Gera palpites inteligentes"""
    try:
        data = request.get_json() or {}
        quantidade = int(data.get('quantidade', 5))
        quantidade = max(1, min(quantidade, 10))  # Entre 1 e 10
        
        palpites = GeradorPalpitesService.gerar_palpites(quantidade)
        
        return jsonify({
            'palpites': [p.to_dict() for p in palpites],
            'quantidade': len(palpites)
        })
    except Exception as e:
        return jsonify({'erro': str(e)}), 500
