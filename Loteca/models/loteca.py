"""Data models for Loteca application."""
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


@dataclass
class Jogo:
    """Representa um jogo de futebol da Loteca."""
    numero: int
    sequencial: int
    time_um: str
    time_dois: str
    uf_um: str
    uf_dois: str
    campeonato: str
    data_jogo: str
    dia_semana: str
    gols_time_um: Optional[int] = None
    gols_time_dois: Optional[int] = None
    resultado: Optional[str] = None  # '1', 'X', '2'
    
    def get_resultado_formatado(self) -> str:
        """Retorna o resultado formatado."""
        if self.resultado:
            return self.resultado
        if self.gols_time_um is not None and self.gols_time_dois is not None:
            if self.gols_time_um > self.gols_time_dois:
                return '1'
            elif self.gols_time_um < self.gols_time_dois:
                return '2'
            else:
                return 'X'
        return '?'
    
    def get_placar(self) -> str:
        """Retorna o placar formatado."""
        if self.gols_time_um is not None and self.gols_time_dois is not None:
            return f"{self.gols_time_um} x {self.gols_time_dois}"
        return "? x ?"


@dataclass
class Concurso:
    """Representa um concurso da Loteca."""
    numero: int
    data_apuracao: str
    data_proximo_concurso: str
    jogos: List[Jogo]
    valor_arrecadado: float
    valor_acumulado: float
    valor_estimado_proximo: float
    acumulado: bool
    rateio_premio: List[dict]
    
    def get_jogos_por_resultado(self, resultado: str) -> List[Jogo]:
        """Retorna jogos com um resultado específico."""
        return [jogo for jogo in self.jogos if jogo.get_resultado_formatado() == resultado]
    
    def get_total_coluna_1(self) -> int:
        """Total de vitórias do time 1."""
        return len(self.get_jogos_por_resultado('1'))
    
    def get_total_empates(self) -> int:
        """Total de empates."""
        return len(self.get_jogos_por_resultado('X'))
    
    def get_total_coluna_2(self) -> int:
        """Total de vitórias do time 2."""
        return len(self.get_jogos_por_resultado('2'))


@dataclass
class Palpite:
    """Representa um palpite para a Loteca."""
    concurso: int
    jogos_palpites: List[dict]  # [{"jogo": 1, "palpite": "1", "confianca": 0.75}, ...]
    estrategia: str
    justificativa: str
    confianca_geral: float
    
    def to_dict(self) -> dict:
        """Converte para dicionário."""
        return {
            'concurso': self.concurso,
            'jogos_palpites': self.jogos_palpites,
            'estrategia': self.estrategia,
            'justificativa': self.justificativa,
            'confianca_geral': self.confianca_geral
        }
