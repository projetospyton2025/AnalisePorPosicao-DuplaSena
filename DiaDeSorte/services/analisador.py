import logging
from typing import List, Dict, Tuple
from collections import Counter
from services.fetcher import DiaDeSorteService

logger = logging.getLogger(__name__)

class AnalisadorService:
    """Serviço para análise estatística dos resultados"""
    
    MESES = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
             'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    
    @classmethod
    def analisar_frequencia_dezenas(cls, limite_concursos: int = 100) -> Dict[int, int]:
        """
        Analisa a frequência de cada dezena nos últimos concursos
        
        Args:
            limite_concursos: Número de concursos a analisar
            
        Returns:
            Dicionário com dezena: frequência
        """
        frequencias = Counter()
        concurso_atual = DiaDeSorteService.buscar_ultimo_concurso()
        
        if not concurso_atual:
            logger.error("Não foi possível buscar o último concurso")
            return {i: 0 for i in range(1, 32)}
        
        numero_inicial = max(1, concurso_atual.numero - limite_concursos + 1)
        
        for num in range(numero_inicial, concurso_atual.numero + 1):
            concurso = DiaDeSorteService.buscar_concurso(num)
            if concurso and concurso.dezenas:
                for dezena in concurso.dezenas:
                    try:
                        frequencias[int(dezena)] += 1
                    except ValueError:
                        continue
        
        # Garante que todas as dezenas estejam no resultado
        resultado = {i: frequencias.get(i, 0) for i in range(1, 32)}
        return resultado
    
    @classmethod
    def analisar_distribuicao_faixas(cls, limite_concursos: int = 100) -> Dict[str, Dict]:
        """
        Analisa a distribuição de dezenas por faixas (baixa, média, alta)
        
        Args:
            limite_concursos: Número de concursos a analisar
            
        Returns:
            Dicionário com estatísticas por faixa
        """
        baixas = 0  # 1-10
        medias = 0  # 11-20
        altas = 0   # 21-31
        total = 0
        
        concurso_atual = DiaDeSorteService.buscar_ultimo_concurso()
        
        if not concurso_atual:
            return {
                'baixas': {'count': 0, 'percentual': 0, 'range': '1-10'},
                'medias': {'count': 0, 'percentual': 0, 'range': '11-20'},
                'altas': {'count': 0, 'percentual': 0, 'range': '21-31'}
            }
        
        numero_inicial = max(1, concurso_atual.numero - limite_concursos + 1)
        
        for num in range(numero_inicial, concurso_atual.numero + 1):
            concurso = DiaDeSorteService.buscar_concurso(num)
            if concurso and concurso.dezenas:
                for dezena in concurso.dezenas:
                    try:
                        d = int(dezena)
                        total += 1
                        if 1 <= d <= 10:
                            baixas += 1
                        elif 11 <= d <= 20:
                            medias += 1
                        else:
                            altas += 1
                    except ValueError:
                        continue
        
        if total == 0:
            total = 1  # Evita divisão por zero
        
        return {
            'baixas': {
                'count': baixas,
                'percentual': round((baixas / total) * 100, 1),
                'range': '1-10',
                'dezenas': list(range(1, 11))
            },
            'medias': {
                'count': medias,
                'percentual': round((medias / total) * 100, 1),
                'range': '11-20',
                'dezenas': list(range(11, 21))
            },
            'altas': {
                'count': altas,
                'percentual': round((altas / total) * 100, 1),
                'range': '21-31',
                'dezenas': list(range(21, 32))
            }
        }
    
    @classmethod
    def analisar_meses_sorte(cls, limite_concursos: int = 100) -> Dict[str, int]:
        """
        Analisa a frequência dos meses da sorte
        
        Args:
            limite_concursos: Número de concursos a analisar
            
        Returns:
            Dicionário com mês: frequência
        """
        frequencias = Counter()
        concurso_atual = DiaDeSorteService.buscar_ultimo_concurso()
        
        if not concurso_atual:
            return {mes: 0 for mes in cls.MESES}
        
        numero_inicial = max(1, concurso_atual.numero - limite_concursos + 1)
        
        for num in range(numero_inicial, concurso_atual.numero + 1):
            concurso = DiaDeSorteService.buscar_concurso(num)
            if concurso and concurso.mes_sorte:
                frequencias[concurso.mes_sorte] += 1
        
        # Garante que todos os meses estejam no resultado
        resultado = {mes: frequencias.get(mes, 0) for mes in cls.MESES}
        return resultado
    
    @classmethod
    def detectar_padroes_sequencias(cls, dezenas: List[int]) -> List[Tuple[int, ...]]:
        """
        Detecta sequências consecutivas nas dezenas
        
        Args:
            dezenas: Lista de dezenas sorteadas
            
        Returns:
            Lista de tuplas com as sequências encontradas
        """
        if not dezenas:
            return []
        
        dezenas_ordenadas = sorted([int(d) for d in dezenas])
        sequencias = []
        sequencia_atual = [dezenas_ordenadas[0]]
        
        for i in range(1, len(dezenas_ordenadas)):
            if dezenas_ordenadas[i] == sequencia_atual[-1] + 1:
                sequencia_atual.append(dezenas_ordenadas[i])
            else:
                if len(sequencia_atual) >= 2:
                    sequencias.append(tuple(sequencia_atual))
                sequencia_atual = [dezenas_ordenadas[i]]
        
        # Verifica a última sequência
        if len(sequencia_atual) >= 2:
            sequencias.append(tuple(sequencia_atual))
        
        return sequencias
    
    @classmethod
    def detectar_finais_iguais(cls, dezenas: List[int]) -> Dict[int, List[int]]:
        """
        Detecta dezenas com finais iguais
        
        Args:
            dezenas: Lista de dezenas sorteadas
            
        Returns:
            Dicionário com final: lista de dezenas
        """
        finais = {}
        
        for dezena in dezenas:
            try:
                d = int(dezena)
                final = d % 10
                if final not in finais:
                    finais[final] = []
                finais[final].append(d)
            except ValueError:
                continue
        
        # Retorna apenas finais que aparecem 2+ vezes
        return {k: v for k, v in finais.items() if len(v) >= 2}
