"""
Serviço de busca de resultados da Dupla Sena
"""
import requests
from typing import List, Optional
import json
import os
from models.dupla_sena import Concurso


class DuplaSenaService:
    """Serviço para buscar resultados da Dupla Sena"""
    
    def __init__(self):
        self.base_url = "https://servicebus2.caixa.gov.br/portaldeloterias/api/duplasena"
        self.resultados = []
    
    def buscar_ultimo_concurso(self) -> Optional[Concurso]:
        """
        Busca o resultado do último concurso da Dupla Sena.
        
        Returns:
            Concurso com os dados do último concurso ou None se houver erro.
        """
        try:
            response = requests.get(self.base_url, timeout=10)
            response.raise_for_status()
            data = response.json()
            return Concurso.from_api_response(data)
        except requests.exceptions.Timeout:
            print(f"Erro: Timeout ao buscar último concurso")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Erro de rede ao buscar último concurso: {e}")
            return None
        except Exception as e:
            print(f"Erro inesperado ao buscar último concurso: {e}")
            return None
    
    def buscar_concurso(self, numero: int) -> Optional[Concurso]:
        """
        Busca o resultado de um concurso específico.
        
        Args:
            numero: Número do concurso.
            
        Returns:
            Concurso com os dados do concurso ou None se houver erro.
        """
        try:
            url = f"{self.base_url}/{numero}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            return Concurso.from_api_response(data)
        except requests.exceptions.Timeout:
            print(f"Erro: Timeout ao buscar concurso {numero}")
            return None
        except requests.exceptions.HTTPError as e:
            print(f"Erro HTTP ao buscar concurso {numero}: {e.response.status_code}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Erro de rede ao buscar concurso {numero}: {e}")
            return None
        except Exception as e:
            print(f"Erro inesperado ao buscar concurso {numero}: {e}")
            return None
    
    def buscar_multiplos_concursos(self, inicio: int, fim: int) -> List[Concurso]:
        """
        Busca resultados de múltiplos concursos.
        
        Args:
            inicio: Número do primeiro concurso.
            fim: Número do último concurso.
            
        Returns:
            Lista de Concursos.
        """
        resultados = []
        print(f"Buscando concursos de {inicio} até {fim}...")
        
        for numero in range(inicio, fim + 1):
            concurso = self.buscar_concurso(numero)
            if concurso:
                resultados.append(concurso)
                print(f"Concurso {numero} obtido com sucesso")
            else:
                print(f"Falha ao obter concurso {numero}")
        
        self.resultados = resultados
        return resultados
    
    def buscar_ultimos_n_concursos(self, n: int) -> List[Concurso]:
        """
        Busca os últimos N concursos.
        
        Args:
            n: Quantidade de concursos a buscar.
            
        Returns:
            Lista de Concursos.
        """
        ultimo = self.buscar_ultimo_concurso()
        if not ultimo:
            return []
        
        numero_ultimo = ultimo.numero
        numero_inicio = max(1, numero_ultimo - n + 1)
        
        return self.buscar_multiplos_concursos(numero_inicio, numero_ultimo)
    
    def salvar_resultados(self, arquivo: str = "resultados_dupla_sena.json"):
        """
        Salva os resultados em arquivo JSON.
        
        Args:
            arquivo: Nome do arquivo para salvar.
        """
        if not self.resultados:
            print("Nenhum resultado para salvar")
            return
        
        data = [c.to_dict() for c in self.resultados]
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Resultados salvos em {arquivo}")
    
    def carregar_resultados(self, arquivo: str = "resultados_dupla_sena.json") -> List[Concurso]:
        """
        Carrega resultados de arquivo JSON.
        
        Args:
            arquivo: Nome do arquivo para carregar.
            
        Returns:
            Lista de Concursos.
        """
        if not os.path.exists(arquivo):
            print(f"Arquivo {arquivo} não encontrado")
            return []
        
        with open(arquivo, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Converte os dados para objetos Concurso
        self.resultados = []
        for item in data:
            concurso = Concurso(
                numero=item.get('numero', 0),
                data=item.get('data', ''),
                dezenas_sorteio1=item.get('dezenas_sorteio1', []),
                dezenas_sorteio2=item.get('dezenas_sorteio2', [])
            )
            self.resultados.append(concurso)
        
        print(f"{len(self.resultados)} resultados carregados de {arquivo}")
        return self.resultados
