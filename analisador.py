"""
Módulo para análise por posição dos resultados da Dupla Sena.
"""
from typing import List, Dict, Tuple
from collections import defaultdict, Counter
import statistics


class AnalisePorPosicao:
    """Classe para análise estatística dos números por posição."""
    
    def __init__(self, resultados: List[Dict]):
        """
        Inicializa o analisador com os resultados.
        
        Args:
            resultados: Lista de dicts com os resultados dos concursos.
        """
        self.resultados = resultados
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
        
        for resultado in self.resultados:
            if sorteio == 1:
                dezenas = sorted([int(d) for d in resultado.get('listaDezenas', [])])
            else:
                dezenas = sorted([int(d) for d in resultado.get('listaDezenasSegundoSorteio', [])])
            
            for posicao, numero in enumerate(dezenas):
                numeros_por_posicao[posicao].append(numero)
        
        return numeros_por_posicao
    
    def _analisar_sorteio(self, sorteio: int) -> Dict:
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
            
            # Estatísticas básicas
            counter = Counter(numeros)
            mais_frequentes = counter.most_common(10)
            
            analise[posicao] = {
                'posicao': posicao + 1,
                'media': round(statistics.mean(numeros), 2),
                'mediana': statistics.median(numeros),
                'moda': statistics.mode(numeros) if len(set(numeros)) < len(numeros) else None,
                'desvio_padrao': round(statistics.stdev(numeros), 2) if len(numeros) > 1 else 0,
                'minimo': min(numeros),
                'maximo': max(numeros),
                'total_ocorrencias': len(numeros),
                'numeros_unicos': len(set(numeros)),
                'mais_frequentes': mais_frequentes
            }
        
        return analise
    
    def obter_analise_completa(self) -> Dict:
        """
        Retorna análise completa dos dois sorteios.
        
        Returns:
            Dict com análises do sorteio 1 e 2.
        """
        return {
            'sorteio_1': self.analise_sorteio1,
            'sorteio_2': self.analise_sorteio2,
            'total_concursos': len(self.resultados)
        }
    
    def exibir_analise(self):
        """Exibe a análise formatada no console."""
        print("\n" + "="*80)
        print("ANÁLISE POR POSIÇÃO - DUPLA SENA")
        print("="*80)
        print(f"\nTotal de concursos analisados: {len(self.resultados)}")
        
        for sorteio_num, analise in [(1, self.analise_sorteio1), (2, self.analise_sorteio2)]:
            print(f"\n{'='*80}")
            print(f"SORTEIO {sorteio_num}")
            print(f"{'='*80}")
            
            for posicao in range(6):
                if posicao not in analise:
                    continue
                
                dados = analise[posicao]
                print(f"\n--- POSIÇÃO {dados['posicao']} ---")
                print(f"Média: {dados['media']}")
                print(f"Mediana: {dados['mediana']}")
                if dados['moda']:
                    print(f"Moda: {dados['moda']}")
                print(f"Desvio Padrão: {dados['desvio_padrao']}")
                print(f"Intervalo: [{dados['minimo']} - {dados['maximo']}]")
                print(f"Números únicos: {dados['numeros_unicos']}")
                
                print(f"\n10 Números mais frequentes:")
                for num, freq in dados['mais_frequentes']:
                    percentual = (freq / dados['total_ocorrencias']) * 100
                    print(f"  {num:2d}: {freq:3d} vezes ({percentual:.1f}%)")
    
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
            
            dados = analise[posicao]
            # Top 5 números mais frequentes
            top_5 = [num for num, _ in dados['mais_frequentes'][:5]]
            sugestoes[posicao + 1] = top_5
        
        return sugestoes
    
    def exibir_sugestoes(self, sorteio: int = 1):
        """
        Exibe sugestões de números por posição.
        
        Args:
            sorteio: Número do sorteio (1 ou 2).
        """
        print(f"\n{'='*80}")
        print(f"SUGESTÕES DE NÚMEROS POR POSIÇÃO - SORTEIO {sorteio}")
        print(f"{'='*80}")
        print("(Baseadas nos números mais frequentes em cada posição)\n")
        
        sugestoes = self.obter_sugestoes(sorteio)
        
        for posicao, numeros in sugestoes.items():
            print(f"Posição {posicao}: {', '.join(map(str, numeros))}")
