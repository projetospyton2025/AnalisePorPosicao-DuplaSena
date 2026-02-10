"""Services package for Loteca application."""
from .fetcher import LotecaService
from .analisador import AnalisadorService
from .gerador_palpites import GeradorPalpitesService

__all__ = ['LotecaService', 'AnalisadorService', 'GeradorPalpitesService']
