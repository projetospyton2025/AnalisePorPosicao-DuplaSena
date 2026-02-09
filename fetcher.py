"""
Módulo para buscar resultados históricos da Dupla Sena.
"""
import requests
from typing import List, Dict, Optional
import json
import os

class DuplaSenaFetcher:
    """Classe para buscar resultados históricos da Dupla Sena."""
    
    def __init__(self):
        self.base_url = "https://servicebus2.caixa.gov.br/portaldeloterias/api/duplasena"
        self.resultados = []
    
    def buscar_ultimo_concurso(self) -> Optional[Dict]:
        """
        Busca o resultado do último concurso da Dupla Sena.
        
        Returns:
            Dict com os dados do último concurso ou None se houver erro.
        """
        try:
            response = requests.get(self.base_url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Erro ao buscar último concurso: {e}")
            return None
    
    def buscar_concurso(self, numero: int) -> Optional[Dict]:
        """
        Busca o resultado de um concurso específico.
        
        Args:
            numero: Número do concurso.
            
        Returns:
            Dict com os dados do concurso ou None se houver erro.
        """
        try:
            url = f"{self.base_url}/{numero}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Erro ao buscar concurso {numero}: {e}")
            return None
    
    def buscar_multiplos_concursos(self, inicio: int, fim: int) -> List[Dict]:
        """
        Busca resultados de múltiplos concursos.
        
        Args:
            inicio: Número do primeiro concurso.
            fim: Número do último concurso.
            
        Returns:
            Lista de dicts com os dados dos concursos.
        """
        resultados = []
        print(f"Buscando concursos de {inicio} até {fim}...")
        
        for numero in range(inicio, fim + 1):
            resultado = self.buscar_concurso(numero)
            if resultado:
                resultados.append(resultado)
                print(f"Concurso {numero} obtido com sucesso")
            else:
                print(f"Falha ao obter concurso {numero}")
        
        self.resultados = resultados
        return resultados
    
    def salvar_resultados(self, arquivo: str = "resultados_dupla_sena.json"):
        """
        Salva os resultados em arquivo JSON.
        
        Args:
            arquivo: Nome do arquivo para salvar.
        """
        if not self.resultados:
            print("Nenhum resultado para salvar")
            return
        
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(self.resultados, f, ensure_ascii=False, indent=2)
        
        print(f"Resultados salvos em {arquivo}")
    
    def carregar_resultados(self, arquivo: str = "resultados_dupla_sena.json") -> List[Dict]:
        """
        Carrega resultados de arquivo JSON.
        
        Args:
            arquivo: Nome do arquivo para carregar.
            
        Returns:
            Lista de dicts com os dados dos concursos.
        """
        if not os.path.exists(arquivo):
            print(f"Arquivo {arquivo} não encontrado")
            return []
        
        with open(arquivo, 'r', encoding='utf-8') as f:
            self.resultados = json.load(f)
        
        print(f"{len(self.resultados)} resultados carregados de {arquivo}")
        return self.resultados
