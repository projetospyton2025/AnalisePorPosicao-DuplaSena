"""
Modelo de dados para resultados da Dupla Sena
"""
from datetime import datetime
from typing import List, Optional


class Concurso:
    """Representa um concurso da Dupla Sena"""
    
    def __init__(self, numero: int, data: str, dezenas_sorteio1: List[int], 
                 dezenas_sorteio2: List[int], **kwargs):
        self.numero = numero
        self.data = data
        self.dezenas_sorteio1 = sorted(dezenas_sorteio1)
        self.dezenas_sorteio2 = sorted(dezenas_sorteio2)
        self.data_apuracao = kwargs.get('dataApuracao', data)
        
    @classmethod
    def from_api_response(cls, data: dict) -> 'Concurso':
        """Cria um objeto Concurso a partir da resposta da API"""
        numero = data.get('numero')
        data_apuracao = data.get('dataApuracao', '')
        
        # Converte strings para inteiros
        dezenas1 = [int(d) for d in data.get('listaDezenas', [])]
        dezenas2 = [int(d) for d in data.get('listaDezenasSegundoSorteio', [])]
        
        return cls(numero, data_apuracao, dezenas1, dezenas2, **data)
    
    def to_dict(self) -> dict:
        """Converte o objeto para dicionário"""
        return {
            'numero': self.numero,
            'data': self.data,
            'dataApuracao': self.data_apuracao,
            'dezenas_sorteio1': self.dezenas_sorteio1,
            'dezenas_sorteio2': self.dezenas_sorteio2
        }
    
    def __repr__(self):
        return f"Concurso({self.numero}, {self.data})"


class EstatisticaPosicao:
    """Estatísticas de uma posição específica"""
    
    def __init__(self, posicao: int, sorteio: int):
        self.posicao = posicao
        self.sorteio = sorteio
        self.media = 0.0
        self.mediana = 0.0
        self.moda = None
        self.desvio_padrao = 0.0
        self.minimo = 0
        self.maximo = 0
        self.total_ocorrencias = 0
        self.numeros_unicos = 0
        self.mais_frequentes = []
        
    def to_dict(self) -> dict:
        """Converte para dicionário"""
        return {
            'posicao': self.posicao,
            'sorteio': self.sorteio,
            'media': self.media,
            'mediana': self.mediana,
            'moda': self.moda,
            'desvio_padrao': self.desvio_padrao,
            'minimo': self.minimo,
            'maximo': self.maximo,
            'total_ocorrencias': self.total_ocorrencias,
            'numeros_unicos': self.numeros_unicos,
            'mais_frequentes': self.mais_frequentes
        }
