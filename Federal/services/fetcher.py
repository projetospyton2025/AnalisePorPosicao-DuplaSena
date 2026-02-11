"""
Serviço de busca de dados da Loteria Federal
"""
import requests
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class FederalService:
    """Serviço para buscar dados da API da Loteria Federal"""
    
    BASE_URL = "https://servicebus2.caixa.gov.br/portaldeloterias/api/federal"
    
    @classmethod
    def buscar_ultimo_concurso(cls) -> Optional[Dict[Any, Any]]:
        """Busca o último concurso disponível"""
        try:
            response = requests.get(cls.BASE_URL, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            logger.error("Timeout ao buscar último concurso")
            return None
        except requests.exceptions.HTTPError as e:
            logger.error(f"Erro HTTP ao buscar último concurso: {e}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao buscar último concurso: {e}")
            return None
    
    @classmethod
    def buscar_concurso(cls, numero: int) -> Optional[Dict[Any, Any]]:
        """Busca um concurso específico"""
        try:
            url = f"{cls.BASE_URL}/{numero}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            logger.error(f"Timeout ao buscar concurso {numero}")
            return None
        except requests.exceptions.HTTPError as e:
            logger.error(f"Erro HTTP ao buscar concurso {numero}: {e}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao buscar concurso {numero}: {e}")
            return None
