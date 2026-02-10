import requests
import logging
from typing import Optional, Dict
from models.dia_de_sorte import Concurso

logger = logging.getLogger(__name__)

class DiaDeSorteService:
    """Serviço para buscar dados da API da Caixa"""
    
    BASE_URL = "https://servicebus2.caixa.gov.br/portaldeloterias/api/diadesorte"
    
    @classmethod
    def buscar_ultimo_concurso(cls) -> Optional[Concurso]:
        """
        Busca os dados do último concurso
        
        Returns:
            Concurso ou None em caso de erro
        """
        try:
            response = requests.get(cls.BASE_URL, timeout=10)
            response.raise_for_status()
            data = response.json()
            return Concurso.from_api_response(data)
        except requests.exceptions.Timeout:
            logger.error("Timeout ao buscar último concurso")
            return None
        except requests.exceptions.HTTPError as e:
            logger.error(f"Erro HTTP ao buscar último concurso: {e}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao buscar último concurso: {e}")
            return None
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar último concurso: {e}")
            return None
    
    @classmethod
    def buscar_concurso(cls, numero: int) -> Optional[Concurso]:
        """
        Busca os dados de um concurso específico
        
        Args:
            numero: Número do concurso
            
        Returns:
            Concurso ou None em caso de erro
        """
        try:
            url = f"{cls.BASE_URL}/{numero}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            return Concurso.from_api_response(data)
        except requests.exceptions.Timeout:
            logger.error(f"Timeout ao buscar concurso {numero}")
            return None
        except requests.exceptions.HTTPError as e:
            logger.error(f"Erro HTTP ao buscar concurso {numero}: {e}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao buscar concurso {numero}: {e}")
            return None
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar concurso {numero}: {e}")
            return None
