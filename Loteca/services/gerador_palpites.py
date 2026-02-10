"""Service for generating Loteca predictions."""
from typing import List, Dict
from models.loteca import Concurso, Jogo, Palpite
import random


class GeradorPalpitesService:
    """Service para gerar palpites inteligentes para a Loteca."""
    
    def __init__(self, analisador):
        self.analisador = analisador
    
    def gerar_palpites(self, concurso_proximo: Concurso, estrategia: str = 'equilibrado') -> Palpite:
        """Gera palpites para o próximo concurso."""
        if estrategia == 'equilibrado':
            return self._estrategia_equilibrada(concurso_proximo)
        elif estrategia == 'mandante':
            return self._estrategia_favorito_mandante(concurso_proximo)
        elif estrategia == 'empates':
            return self._estrategia_empates(concurso_proximo)
        elif estrategia == 'visitante':
            return self._estrategia_visitante(concurso_proximo)
        elif estrategia == 'zebra':
            return self._estrategia_zebra(concurso_proximo)
        else:
            return self._estrategia_equilibrada(concurso_proximo)
    
    def _estrategia_equilibrada(self, concurso: Concurso) -> Palpite:
        """Estratégia equilibrada baseada em estatísticas gerais."""
        distribuicao = self.analisador.analisar_distribuicao_resultados()
        jogos_palpites = []
        
        for jogo in concurso.jogos:
            # Análise básica baseada em histórico
            palpite = self._analisar_jogo_equilibrado(jogo, distribuicao)
            jogos_palpites.append(palpite)
        
        confianca_geral = sum(p['confianca'] for p in jogos_palpites) / len(jogos_palpites)
        
        return Palpite(
            concurso=concurso.numero,
            jogos_palpites=jogos_palpites,
            estrategia='Equilibrado',
            justificativa='Baseado na distribuição histórica de resultados e análise de times',
            confianca_geral=round(confianca_geral, 2)
        )
    
    def _estrategia_favorito_mandante(self, concurso: Concurso) -> Palpite:
        """Estratégia que favorece o time mandante (coluna 1)."""
        mandante_stats = self.analisador.analisar_mandante_visitante()
        jogos_palpites = []
        
        for jogo in concurso.jogos:
            # Favorece mandante com alta confiança
            confianca = min(0.75, mandante_stats.get('percentual_vitorias', 45) / 100 + 0.20)
            jogos_palpites.append({
                'jogo': jogo.sequencial,
                'time_um': jogo.time_um,
                'time_dois': jogo.time_dois,
                'palpite': '1',
                'confianca': round(confianca, 2),
                'justificativa': 'Vantagem do mandante'
            })
        
        return Palpite(
            concurso=concurso.numero,
            jogos_palpites=jogos_palpites,
            estrategia='Favorito Mandante',
            justificativa='Estratégia que prioriza vitórias do time que joga em casa',
            confianca_geral=0.65
        )
    
    def _estrategia_empates(self, concurso: Concurso) -> Palpite:
        """Estratégia que favorece empates em alguns jogos."""
        distribuicao = self.analisador.analisar_distribuicao_resultados()
        jogos_palpites = []
        
        percentual_empates = distribuicao['empates']['percentual']
        
        # Escolhe alguns jogos para apostar no empate
        num_empates = max(2, int(len(concurso.jogos) * (percentual_empates / 100)))
        jogos_empate = random.sample(range(len(concurso.jogos)), min(num_empates, len(concurso.jogos)))
        
        for i, jogo in enumerate(concurso.jogos):
            if i in jogos_empate:
                palpite_resultado = 'X'
                confianca = 0.55
                justificativa = 'Jogo equilibrado - favorece empate'
            else:
                # Para outros, analisa normalmente
                palpite_resultado = '1' if random.random() < 0.5 else '2'
                confianca = 0.60
                justificativa = 'Baseado em estatísticas'
            
            jogos_palpites.append({
                'jogo': jogo.sequencial,
                'time_um': jogo.time_um,
                'time_dois': jogo.time_dois,
                'palpite': palpite_resultado,
                'confianca': confianca,
                'justificativa': justificativa
            })
        
        return Palpite(
            concurso=concurso.numero,
            jogos_palpites=jogos_palpites,
            estrategia='Empates Estratégicos',
            justificativa=f'Incluindo {num_empates} empates estratégicos baseados no histórico',
            confianca_geral=0.57
        )
    
    def _estrategia_visitante(self, concurso: Concurso) -> Palpite:
        """Estratégia que favorece alguns times visitantes."""
        jogos_palpites = []
        
        for jogo in concurso.jogos:
            # 60% chance de apostar no visitante
            if random.random() < 0.60:
                palpite_resultado = '2'
                confianca = 0.55
                justificativa = 'Time visitante em boa fase'
            else:
                palpite_resultado = '1'
                confianca = 0.60
                justificativa = 'Vantagem do mandante'
            
            jogos_palpites.append({
                'jogo': jogo.sequencial,
                'time_um': jogo.time_um,
                'time_dois': jogo.time_dois,
                'palpite': palpite_resultado,
                'confianca': confianca,
                'justificativa': justificativa
            })
        
        return Palpite(
            concurso=concurso.numero,
            jogos_palpites=jogos_palpites,
            estrategia='Força Visitante',
            justificativa='Estratégia que aposta em alguns visitantes surpreendentes',
            confianca_geral=0.57
        )
    
    def _estrategia_zebra(self, concurso: Concurso) -> Palpite:
        """Estratégia com resultados menos prováveis (zebras)."""
        jogos_palpites = []
        
        for jogo in concurso.jogos:
            # Mistura de resultados improváveis
            escolhas = ['1', 'X', '2']
            palpite_resultado = random.choice(escolhas)
            confianca = 0.45  # Menor confiança para zebras
            
            jogos_palpites.append({
                'jogo': jogo.sequencial,
                'time_um': jogo.time_um,
                'time_dois': jogo.time_dois,
                'palpite': palpite_resultado,
                'confianca': confianca,
                'justificativa': 'Aposta em resultado improvável'
            })
        
        return Palpite(
            concurso=concurso.numero,
            jogos_palpites=jogos_palpites,
            estrategia='Zebra',
            justificativa='Estratégia ousada apostando em resultados menos prováveis - alto risco, alto retorno',
            confianca_geral=0.45
        )
    
    def _analisar_jogo_equilibrado(self, jogo: Jogo, distribuicao: Dict) -> Dict:
        """Analisa um jogo individual de forma equilibrada."""
        # Pesos baseados na distribuição histórica
        peso_1 = distribuicao['coluna_1']['percentual']
        peso_x = distribuicao['empates']['percentual']
        peso_2 = distribuicao['coluna_2']['percentual']
        
        # Normalizar pesos
        total_peso = peso_1 + peso_x + peso_2
        if total_peso > 0:
            peso_1 = peso_1 / total_peso
            peso_x = peso_x / total_peso
            peso_2 = peso_2 / total_peso
        else:
            peso_1 = peso_x = peso_2 = 0.33
        
        # Escolher resultado baseado nos pesos
        rand = random.random()
        if rand < peso_1:
            palpite = '1'
            confianca = min(0.75, peso_1 + 0.10)
            justificativa = 'Histórico favorece mandante'
        elif rand < peso_1 + peso_x:
            palpite = 'X'
            confianca = min(0.70, peso_x + 0.15)
            justificativa = 'Jogo equilibrado'
        else:
            palpite = '2'
            confianca = min(0.75, peso_2 + 0.10)
            justificativa = 'Histórico favorece visitante'
        
        return {
            'jogo': jogo.sequencial,
            'time_um': jogo.time_um,
            'time_dois': jogo.time_dois,
            'palpite': palpite,
            'confianca': round(confianca, 2),
            'justificativa': justificativa
        }
