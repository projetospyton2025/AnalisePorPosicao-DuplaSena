"""Service for analyzing Loteca statistics."""
from typing import List, Dict
from models.loteca import Concurso, Jogo
from collections import Counter, defaultdict


class AnalisadorService:
    """Service para análise estatística da Loteca."""
    
    def __init__(self):
        self.historico_concursos = []
    
    def adicionar_concurso(self, concurso: Concurso):
        """Adiciona um concurso ao histórico."""
        self.historico_concursos.append(concurso)
    
    def analisar_distribuicao_resultados(self) -> Dict:
        """Analisa a distribuição de resultados (coluna 1, empate, coluna 2)."""
        total_jogos = 0
        coluna_1 = 0
        empates = 0
        coluna_2 = 0
        
        for concurso in self.historico_concursos:
            for jogo in concurso.jogos:
                resultado = jogo.get_resultado_formatado()
                if resultado != '?':
                    total_jogos += 1
                    if resultado == '1':
                        coluna_1 += 1
                    elif resultado == 'X':
                        empates += 1
                    elif resultado == '2':
                        coluna_2 += 1
        
        if total_jogos == 0:
            return {
                'total_jogos': 0,
                'coluna_1': {'count': 0, 'percentual': 0},
                'empates': {'count': 0, 'percentual': 0},
                'coluna_2': {'count': 0, 'percentual': 0}
            }
        
        return {
            'total_jogos': total_jogos,
            'coluna_1': {
                'count': coluna_1,
                'percentual': round((coluna_1 / total_jogos) * 100, 2)
            },
            'empates': {
                'count': empates,
                'percentual': round((empates / total_jogos) * 100, 2)
            },
            'coluna_2': {
                'count': coluna_2,
                'percentual': round((coluna_2 / total_jogos) * 100, 2)
            }
        }
    
    def analisar_times(self) -> Dict:
        """Analisa o desempenho de cada time."""
        times_stats = defaultdict(lambda: {
            'jogos': 0,
            'vitorias': 0,
            'empates': 0,
            'derrotas': 0,
            'gols_marcados': 0,
            'gols_sofridos': 0
        })
        
        for concurso in self.historico_concursos:
            for jogo in concurso.jogos:
                if jogo.gols_time_um is not None and jogo.gols_time_dois is not None:
                    # Time 1
                    times_stats[jogo.time_um]['jogos'] += 1
                    times_stats[jogo.time_um]['gols_marcados'] += jogo.gols_time_um
                    times_stats[jogo.time_um]['gols_sofridos'] += jogo.gols_time_dois
                    
                    # Time 2
                    times_stats[jogo.time_dois]['jogos'] += 1
                    times_stats[jogo.time_dois]['gols_marcados'] += jogo.gols_time_dois
                    times_stats[jogo.time_dois]['gols_sofridos'] += jogo.gols_time_um
                    
                    resultado = jogo.get_resultado_formatado()
                    if resultado == '1':
                        times_stats[jogo.time_um]['vitorias'] += 1
                        times_stats[jogo.time_dois]['derrotas'] += 1
                    elif resultado == 'X':
                        times_stats[jogo.time_um]['empates'] += 1
                        times_stats[jogo.time_dois]['empates'] += 1
                    elif resultado == '2':
                        times_stats[jogo.time_um]['derrotas'] += 1
                        times_stats[jogo.time_dois]['vitorias'] += 1
        
        # Calcular percentuais e ordenar
        times_lista = []
        for time, stats in times_stats.items():
            if stats['jogos'] > 0:
                stats['time'] = time
                stats['aproveitamento'] = round(
                    ((stats['vitorias'] * 3 + stats['empates']) / (stats['jogos'] * 3)) * 100, 2
                )
                stats['saldo_gols'] = stats['gols_marcados'] - stats['gols_sofridos']
                times_lista.append(stats)
        
        # Ordenar por aproveitamento
        times_lista.sort(key=lambda x: x['aproveitamento'], reverse=True)
        
        return {
            'times': times_lista[:20],  # Top 20 times
            'total_times': len(times_lista)
        }
    
    def analisar_confrontos_diretos(self, time1: str, time2: str) -> Dict:
        """Analisa o histórico de confrontos diretos entre dois times."""
        confrontos = []
        
        for concurso in self.historico_concursos:
            for jogo in concurso.jogos:
                if (jogo.time_um == time1 and jogo.time_dois == time2) or \
                   (jogo.time_um == time2 and jogo.time_dois == time1):
                    confrontos.append({
                        'concurso': concurso.numero,
                        'data': jogo.data_jogo,
                        'time_um': jogo.time_um,
                        'time_dois': jogo.time_dois,
                        'placar': jogo.get_placar(),
                        'resultado': jogo.get_resultado_formatado()
                    })
        
        if not confrontos:
            return {
                'total_jogos': 0,
                'vitorias_time1': 0,
                'empates': 0,
                'vitorias_time2': 0,
                'confrontos': []
            }
        
        vitorias_time1 = 0
        vitorias_time2 = 0
        empates = 0
        
        for confronto in confrontos:
            if confronto['time_um'] == time1:
                if confronto['resultado'] == '1':
                    vitorias_time1 += 1
                elif confronto['resultado'] == 'X':
                    empates += 1
                elif confronto['resultado'] == '2':
                    vitorias_time2 += 1
            else:
                if confronto['resultado'] == '1':
                    vitorias_time2 += 1
                elif confronto['resultado'] == 'X':
                    empates += 1
                elif confronto['resultado'] == '2':
                    vitorias_time1 += 1
        
        return {
            'total_jogos': len(confrontos),
            'vitorias_time1': vitorias_time1,
            'empates': empates,
            'vitorias_time2': vitorias_time2,
            'confrontos': confrontos[-10:]  # Últimos 10 confrontos
        }
    
    def analisar_mandante_visitante(self) -> Dict:
        """Analisa vantagem de jogar em casa."""
        mandante_stats = {'vitorias': 0, 'empates': 0, 'derrotas': 0, 'total': 0}
        
        for concurso in self.historico_concursos:
            for jogo in concurso.jogos:
                resultado = jogo.get_resultado_formatado()
                if resultado != '?':
                    mandante_stats['total'] += 1
                    if resultado == '1':
                        mandante_stats['vitorias'] += 1
                    elif resultado == 'X':
                        mandante_stats['empates'] += 1
                    elif resultado == '2':
                        mandante_stats['derrotas'] += 1
        
        if mandante_stats['total'] == 0:
            return mandante_stats
        
        mandante_stats['percentual_vitorias'] = round(
            (mandante_stats['vitorias'] / mandante_stats['total']) * 100, 2
        )
        mandante_stats['percentual_empates'] = round(
            (mandante_stats['empates'] / mandante_stats['total']) * 100, 2
        )
        mandante_stats['percentual_derrotas'] = round(
            (mandante_stats['derrotas'] / mandante_stats['total']) * 100, 2
        )
        
        return mandante_stats
