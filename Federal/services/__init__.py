"""Serviços de negócio para Loteria Federal"""
from .fetcher import FederalService
from .analisador import AnalisadorService
from .gerador_palpites import GeradorPalpitesService

__all__ = ['FederalService', 'AnalisadorService', 'GeradorPalpitesService']
