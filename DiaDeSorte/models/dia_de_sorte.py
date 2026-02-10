from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class Concurso:
    """Representa um concurso do Dia de Sorte"""
    numero: int
    data_sorteio: str
    dezenas: List[str]
    dezenas_ordem_sorteio: List[str]
    mes_sorte: str
    arrecadacao: float
    acumulado: bool
    valor_acumulado_proximo: float
    data_proximo_concurso: str
    numero_proximo_concurso: int
    premiacoes: List[dict]
    
    @classmethod
    def from_api_response(cls, data: dict) -> 'Concurso':
        """Cria um Concurso a partir da resposta da API"""
        return cls(
            numero=data.get('numero', 0),
            data_sorteio=data.get('dataApuracao', ''),
            dezenas=data.get('listaDezenas', []),
            dezenas_ordem_sorteio=data.get('dezenasSorteadasOrdemSorteio', []),
            mes_sorte=data.get('nomeTimeCoracaoMesSorte', ''),
            arrecadacao=data.get('valorArrecadado', 0.0),
            acumulado=data.get('acumulado', False),
            valor_acumulado_proximo=data.get('valorAcumuladoProximoConcurso', 0.0),
            data_proximo_concurso=data.get('dataProximoConcurso', ''),
            numero_proximo_concurso=data.get('numeroConcursoProximo', 0),
            premiacoes=data.get('listaRateioPremio', [])
        )

@dataclass
class Palpite:
    """Representa um palpite gerado"""
    dezenas: List[int]
    mes_sugerido: str
    estrategia: str
    confianca: str
    justificativa: str
    
    def to_dict(self) -> dict:
        """Converte o palpite para dicionário"""
        return {
            'dezenas': sorted(self.dezenas),
            'mes_sugerido': self.mes_sugerido,
            'estrategia': self.estrategia,
            'confianca': self.confianca,
            'justificativa': self.justificativa
        }
