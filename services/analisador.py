"""
Serviço de análise estatística por posição para Dupla Sena
"""
from typing import List, Dict
from collections import defaultdict, Counter
import statistics
from models.dupla_sena import Concurso, EstatisticaPosicao


class AnalisadorService:
    """Serviço para análise estatística dos números por posição"""
    
    def __init__(self, concursos: List[Concurso]):
        """
        Inicializa o analisador com os concursos.
        
        Args:
            concursos: Lista de Concursos.
        """
        self.concursos = concursos
        self.analise_sorteio1 = self._analisar_sorteio(1)
        self.analise_sorteio2 = self._analisar_sorteio(2)
    
    def _extrair_numeros_por_posicao(self, sorteio: int) -> Dict[int, List[int]]:
        """
        Extrai os números por posição de um sorteio específico.
        
        Args:
            sorteio: Número do sorteio (1 ou 2).
            
        Returns:
            Dict onde a chave é a posição (0-5) e o valor é uma lista de números.
        """
        numeros_por_posicao = defaultdict(list)
        
        for concurso in self.concursos:
            if sorteio == 1:
                dezenas = concurso.dezenas_sorteio1
            else:
                dezenas = concurso.dezenas_sorteio2
            
            for posicao, numero in enumerate(dezenas):
                numeros_por_posicao[posicao].append(numero)
        
        return numeros_por_posicao
    
    def _analisar_sorteio(self, sorteio: int) -> Dict[int, EstatisticaPosicao]:
        """
        Analisa estatísticas de um sorteio específico.
        
        Args:
            sorteio: Número do sorteio (1 ou 2).
            
        Returns:
            Dict com análises por posição.
        """
        numeros_por_posicao = self._extrair_numeros_por_posicao(sorteio)
        analise = {}
        
        for posicao in range(6):
            numeros = numeros_por_posicao[posicao]
            if not numeros:
                continue
            
            # Cria objeto de estatísticas
            stat = EstatisticaPosicao(posicao + 1, sorteio)
            
            # Estatísticas básicas
            counter = Counter(numeros)
            mais_frequentes = counter.most_common(10)
            
            stat.media = round(statistics.mean(numeros), 2)
            stat.mediana = statistics.median(numeros)
            stat.moda = statistics.mode(numeros) if len(set(numeros)) < len(numeros) else None
            stat.desvio_padrao = round(statistics.stdev(numeros), 2) if len(numeros) > 1 else 0
            stat.minimo = min(numeros)
            stat.maximo = max(numeros)
            stat.total_ocorrencias = len(numeros)
            stat.numeros_unicos = len(set(numeros))
            stat.mais_frequentes = mais_frequentes
            
            analise[posicao] = stat
        
        return analise
    
    def obter_analise_completa(self) -> Dict:
        """
        Retorna análise completa dos dois sorteios.
        
        Returns:
            Dict com análises do sorteio 1 e 2.
        """
        return {
            'sorteio_1': {k: v.to_dict() for k, v in self.analise_sorteio1.items()},
            'sorteio_2': {k: v.to_dict() for k, v in self.analise_sorteio2.items()},
            'total_concursos': len(self.concursos)
        }
    
    def obter_sugestoes(self, sorteio: int = 1) -> Dict[int, List[int]]:
        """
        Gera sugestões de números por posição baseadas na frequência.
        
        Args:
            sorteio: Número do sorteio (1 ou 2).
            
        Returns:
            Dict com sugestões de números por posição.
        """
        analise = self.analise_sorteio1 if sorteio == 1 else self.analise_sorteio2
        sugestoes = {}
        
        for posicao in range(6):
            if posicao not in analise:
                continue
            
            stat = analise[posicao]
            # Top 5 números mais frequentes
            top_5 = [num for num, _ in stat.mais_frequentes[:5]]
            sugestoes[posicao + 1] = top_5
        
        return sugestoes
    
    def obter_estatisticas_posicao(self, posicao: int, sorteio: int = 1) -> EstatisticaPosicao:
        """
        Obtém estatísticas de uma posição específica.
        
        Args:
            posicao: Posição (1-6).
            sorteio: Número do sorteio (1 ou 2).
            
        Returns:
            EstatisticaPosicao ou None.
        """
        analise = self.analise_sorteio1 if sorteio == 1 else self.analise_sorteio2
        return analise.get(posicao - 1)
