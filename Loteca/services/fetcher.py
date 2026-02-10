"""Service for fetching Loteca data from Caixa API."""
import requests
from typing import Optional, List
from models.loteca import Concurso, Jogo
import logging

logger = logging.getLogger(__name__)


class LotecaService:
    """Service para buscar dados da API da Loteca."""
    
    BASE_URL = "https://servicebus2.caixa.gov.br/portaldeloterias/api/loteca"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def buscar_ultimo_concurso(self) -> Optional[Concurso]:
        """Busca o último concurso da Loteca."""
        try:
            response = self.session.get(
                self.BASE_URL,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            return self._parse_concurso(data)
        except requests.exceptions.Timeout:
            logger.error("Timeout ao buscar último concurso da Loteca")
            return None
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error ao buscar último concurso: {e}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao buscar último concurso: {e}")
            return None
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar último concurso: {e}")
            return None
    
    def buscar_concurso(self, numero: int) -> Optional[Concurso]:
        """Busca um concurso específico pelo número."""
        try:
            response = self.session.get(
                f"{self.BASE_URL}/{numero}",
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            return self._parse_concurso(data)
        except requests.exceptions.Timeout:
            logger.error(f"Timeout ao buscar concurso {numero}")
            return None
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error ao buscar concurso {numero}: {e}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao buscar concurso {numero}: {e}")
            return None
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar concurso {numero}: {e}")
            return None
    
    def _parse_concurso(self, data: dict) -> Concurso:
        """Converte dados da API em objeto Concurso."""
        # Parse jogos
        jogos = []
        lista_jogos = data.get('listaResultadoEquipeEsportiva', [])
        
        for jogo_data in lista_jogos:
            jogo = Jogo(
                numero=jogo_data.get('nuConcurso'),
                sequencial=jogo_data.get('nuSequencial'),
                time_um=jogo_data.get('nomeEquipeUm', ''),
                time_dois=jogo_data.get('nomeEquipeDois', ''),
                uf_um=jogo_data.get('siglaUFUm', ''),
                uf_dois=jogo_data.get('siglaUFDois', ''),
                campeonato=jogo_data.get('nomeCampeonato', ''),
                data_jogo=jogo_data.get('dtJogo', ''),
                dia_semana=jogo_data.get('diaSemana', ''),
                gols_time_um=jogo_data.get('nuGolEquipeUm'),
                gols_time_dois=jogo_data.get('nuGolEquipeDois'),
                resultado=jogo_data.get('resultado')
            )
            jogos.append(jogo)
        
        # Parse rateio de prêmios
        rateio = data.get('listaRateioPremio', [])
        
        concurso = Concurso(
            numero=data.get('numero'),
            data_apuracao=data.get('dataApuracao', ''),
            data_proximo_concurso=data.get('dataProximoConcurso', ''),
            jogos=jogos,
            valor_arrecadado=data.get('valorArrecadado', 0.0),
            valor_acumulado=data.get('valorAcumuladoProximoConcurso', 0.0),
            valor_estimado_proximo=data.get('valorEstimadoProximoConcurso', 0.0),
            acumulado=data.get('acumulado', False),
            rateio_premio=rateio
        )
        
        return concurso
