"""
Modelos de dados para Loteria Federal
"""
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class Premio:
    """Representa um prêmio da Loteria Federal"""
    posicao: int
    numero: str
    serie: str
    valor: float
    ganhadores: int = 0
    
    def __post_init__(self):
        """Valida e formata o número"""
        if isinstance(self.numero, str):
            self.numero = self.numero.zfill(6)

@dataclass
class Concurso:
    """Representa um concurso da Loteria Federal"""
    numero: int
    data_apuracao: str
    premios: List[Premio]
    proximo_concurso: Optional[int] = None
    data_proximo_concurso: Optional[str] = None
    acumulado: bool = False
    
    @classmethod
    def from_api_response(cls, data: dict) -> 'Concurso':
        """Cria um Concurso a partir da resposta da API"""
        premios = []
        
        # Processa os 5 prêmios
        numeros = data.get('listaDezenas', [])
        ratei os = data.get('listaRateioPremio', [])
        ganhadores_info = data.get('listaMunicipioUFGanhadores', [])
        
        for i, numero in enumerate(numeros[:5], 1):
            # Encontra informações do prêmio
            premio_info = next((r for r in rateios if r['faixa'] == i), None)
            ganhador_info = next((g for g in ganhadores_info if g['posicao'] == i), None)
            
            premio = Premio(
                posicao=i,
                numero=numero,
                serie=ganhador_info.get('serie', 'A') if ganhador_info else 'A',
                valor=premio_info.get('valorPremio', 0.0) if premio_info else 0.0,
                ganhadores=premio_info.get('numeroDeGanhadores', 0) if premio_info else 0
            )
            premios.append(premio)
        
        return cls(
            numero=data.get('numero'),
            data_apuracao=data.get('dataApuracao'),
            premios=premios,
            proximo_concurso=data.get('numeroConcursoProximo'),
            data_proximo_concurso=data.get('dataProximoConcurso'),
            acumulado=data.get('acumulado', False)
        )

@dataclass
class Palpite:
    """Representa um palpite gerado"""
    numero: str
    estrategia: str
    confianca: float
    justificativa: str
    
    def __post_init__(self):
        """Valida e formata o número"""
        if isinstance(self.numero, str):
            self.numero = self.numero.zfill(6)
        elif isinstance(self.numero, int):
            self.numero = str(self.numero).zfill(6)
