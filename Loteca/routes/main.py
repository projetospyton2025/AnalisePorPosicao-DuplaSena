"""Main routes for Loteca application."""
from flask import Blueprint, render_template, jsonify, request
from services.fetcher import LotecaService
from services.analisador import AnalisadorService
from services.gerador_palpites import GeradorPalpitesService
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('main', __name__)

# Inicializa serviços
loteca_service = LotecaService()
analisador_service = AnalisadorService()
gerador_service = GeradorPalpitesService(analisador_service)


@bp.route('/')
def index():
    """Página inicial."""
    return render_template('index.html')


@bp.route('/analise')
def analise():
    """Página de análise estatística."""
    return render_template('analise.html')


@bp.route('/palpites')
def palpites():
    """Página de geração de palpites."""
    return render_template('palpites.html')


@bp.route('/api/ultimo-concurso')
def api_ultimo_concurso():
    """API: Retorna o último concurso."""
    try:
        concurso = loteca_service.buscar_ultimo_concurso()
        if not concurso:
            return jsonify({'error': 'Não foi possível buscar o último concurso'}), 500
        
        # Adiciona ao histórico do analisador
        analisador_service.adicionar_concurso(concurso)
        
        return jsonify({
            'numero': concurso.numero,
            'dataApuracao': concurso.data_apuracao,
            'dataProximoConcurso': concurso.data_proximo_concurso,
            'acumulado': concurso.acumulado,
            'valorArrecadado': concurso.valor_arrecadado,
            'valorAcumulado': concurso.valor_acumulado,
            'valorEstimadoProximo': concurso.valor_estimado_proximo,
            'totalColuna1': concurso.get_total_coluna_1(),
            'totalEmpates': concurso.get_total_empates(),
            'totalColuna2': concurso.get_total_coluna_2(),
            'jogos': [{
                'sequencial': jogo.sequencial,
                'timeUm': jogo.time_um,
                'timeDois': jogo.time_dois,
                'ufUm': jogo.uf_um,
                'ufDois': jogo.uf_dois,
                'campeonato': jogo.campeonato,
                'dataJogo': jogo.data_jogo,
                'diaSemana': jogo.dia_semana,
                'golsTimeUm': jogo.gols_time_um,
                'golsTimeDois': jogo.gols_time_dois,
                'resultado': jogo.get_resultado_formatado(),
                'placar': jogo.get_placar()
            } for jogo in concurso.jogos],
            'rateioPremio': concurso.rateio_premio
        })
    except Exception as e:
        logger.error(f"Erro ao buscar último concurso: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/api/buscar-concurso/<int:numero>')
def api_buscar_concurso(numero):
    """API: Busca um concurso específico."""
    try:
        concurso = loteca_service.buscar_concurso(numero)
        if not concurso:
            return jsonify({'error': f'Concurso {numero} não encontrado'}), 404
        
        # Adiciona ao histórico do analisador
        analisador_service.adicionar_concurso(concurso)
        
        return jsonify({
            'numero': concurso.numero,
            'dataApuracao': concurso.data_apuracao,
            'dataProximoConcurso': concurso.data_proximo_concurso,
            'acumulado': concurso.acumulado,
            'valorArrecadado': concurso.valor_arrecadado,
            'valorAcumulado': concurso.valor_acumulado,
            'valorEstimadoProximo': concurso.valor_estimado_proximo,
            'totalColuna1': concurso.get_total_coluna_1(),
            'totalEmpates': concurso.get_total_empates(),
            'totalColuna2': concurso.get_total_coluna_2(),
            'jogos': [{
                'sequencial': jogo.sequencial,
                'timeUm': jogo.time_um,
                'timeDois': jogo.time_dois,
                'ufUm': jogo.uf_um,
                'ufDois': jogo.uf_dois,
                'campeonato': jogo.campeonato,
                'dataJogo': jogo.data_jogo,
                'diaSemana': jogo.dia_semana,
                'golsTimeUm': jogo.gols_time_um,
                'golsTimeDois': jogo.gols_time_dois,
                'resultado': jogo.get_resultado_formatado(),
                'placar': jogo.get_placar()
            } for jogo in concurso.jogos],
            'rateioPremio': concurso.rateio_premio
        })
    except Exception as e:
        logger.error(f"Erro ao buscar concurso {numero}: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/api/analise-estatistica')
def api_analise_estatistica():
    """API: Retorna análise estatística completa."""
    try:
        # Buscar últimos 10 concursos para análise
        concurso_atual = loteca_service.buscar_ultimo_concurso()
        if not concurso_atual:
            return jsonify({'error': 'Não foi possível buscar dados'}), 500
        
        numero_atual = concurso_atual.numero
        for i in range(10):
            numero = numero_atual - i
            if numero > 0:
                conc = loteca_service.buscar_concurso(numero)
                if conc:
                    analisador_service.adicionar_concurso(conc)
        
        # Análises
        distribuicao = analisador_service.analisar_distribuicao_resultados()
        times = analisador_service.analisar_times()
        mandante = analisador_service.analisar_mandante_visitante()
        
        return jsonify({
            'distribuicao': distribuicao,
            'times': times,
            'mandante': mandante
        })
    except Exception as e:
        logger.error(f"Erro na análise estatística: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/api/gerar-palpites', methods=['POST'])
def api_gerar_palpites():
    """API: Gera palpites para o próximo concurso."""
    try:
        data = request.json
        estrategia = data.get('estrategia', 'equilibrado')
        
        # Buscar último concurso
        concurso = loteca_service.buscar_ultimo_concurso()
        if not concurso:
            return jsonify({'error': 'Não foi possível buscar o último concurso'}), 500
        
        # Buscar histórico para análise
        numero_atual = concurso.numero
        for i in range(10):
            numero = numero_atual - i
            if numero > 0:
                conc = loteca_service.buscar_concurso(numero)
                if conc:
                    analisador_service.adicionar_concurso(conc)
        
        # Criar concurso simulado para o próximo (com os mesmos jogos mas sem resultados)
        from models.loteca import Concurso, Jogo
        jogos_proximo = []
        for jogo in concurso.jogos:
            jogo_novo = Jogo(
                numero=concurso.numero + 1,
                sequencial=jogo.sequencial,
                time_um=jogo.time_um,
                time_dois=jogo.time_dois,
                uf_um=jogo.uf_um,
                uf_dois=jogo.uf_dois,
                campeonato=jogo.campeonato,
                data_jogo=concurso.data_proximo_concurso,
                dia_semana='',
                gols_time_um=None,
                gols_time_dois=None,
                resultado=None
            )
            jogos_proximo.append(jogo_novo)
        
        concurso_proximo = Concurso(
            numero=concurso.numero + 1,
            data_apuracao='',
            data_proximo_concurso='',
            jogos=jogos_proximo,
            valor_arrecadado=0,
            valor_acumulado=concurso.valor_acumulado,
            valor_estimado_proximo=concurso.valor_estimado_proximo,
            acumulado=False,
            rateio_premio=[]
        )
        
        # Gerar palpites
        palpite = gerador_service.gerar_palpites(concurso_proximo, estrategia)
        
        return jsonify(palpite.to_dict())
    except Exception as e:
        logger.error(f"Erro ao gerar palpites: {e}")
        return jsonify({'error': str(e)}), 500
