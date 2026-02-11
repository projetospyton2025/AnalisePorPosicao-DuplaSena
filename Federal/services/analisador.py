"""
Serviço de análise estatística da Loteria Federal
"""
from typing import List, Dict, Any
from collections import Counter
import statistics

class AnalisadorService:
    """Análise estatística de resultados da Loteria Federal"""
    
    @staticmethod
    def analisar_frequencia_digitos(numeros: List[str]) -> Dict[int, Dict[str, int]]:
        """Analisa frequência de cada dígito (0-9) em cada posição (1-6)"""
        frequencias = {pos: Counter() for pos in range(1, 7)}
        
        for numero in numeros:
            numero_str = str(numero).zfill(6)
            for pos, digito in enumerate(numero_str, 1):
                frequencias[pos][digito] += 1
        
        return {
            pos: dict(sorted(freq.items(), key=lambda x: x[1], reverse=True))
            for pos, freq in frequencias.items()
        }
    
    @staticmethod
    def analisar_ultimos_digitos(numeros: List[str]) -> Dict[str, int]:
        """Analisa frequência dos últimos dígitos"""
        ultimos = [str(n).zfill(6)[-1] for n in numeros]
        return dict(Counter(ultimos).most_common())
    
    @staticmethod
    def analisar_sequencias(numeros: List[str]) -> Dict[str, Any]:
        """Analisa presença de sequências nos números"""
        com_sequencia = 0
        total = len(numeros)
        
        for numero in numeros:
            numero_str = str(numero).zfill(6)
            digitos = [int(d) for d in numero_str]
            
            # Verifica sequências de 3+ dígitos
            for i in range(len(digitos) - 2):
                if digitos[i+1] == digitos[i] + 1 and digitos[i+2] == digitos[i] + 2:
                    com_sequencia += 1
                    break
        
        return {
            'total_com_sequencia': com_sequencia,
            'percentual': round((com_sequencia / total * 100) if total > 0 else 0, 2)
        }
    
    @staticmethod
    def analisar_numeros_quentes_frios(numeros_recentes: List[str], limite: int = 50) -> Dict[str, Any]:
        """Identifica dígitos quentes (frequentes) e frios (raros) nos últimos concursos"""
        todos_digitos = []
        for numero in numeros_recentes[:limite]:
            todos_digitos.extend(list(str(numero).zfill(6)))
        
        frequencia = Counter(todos_digitos)
        
        # Ordena por frequência
        ordenados = sorted(frequencia.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'quentes': [{'digito': d, 'freq': f} for d, f in ordenados[:5]],
            'frios': [{'digito': d, 'freq': f} for d, f in ordenados[-5:]],
            'periodo_analise': min(len(numeros_recentes), limite)
        }
    
    @staticmethod
    def analisar_soma_numeros(numeros: List[str]) -> Dict[str, Any]:
        """Analisa a soma dos dígitos dos números"""
        somas = []
        for numero in numeros:
            digitos = [int(d) for d in str(numero).zfill(6)]
            somas.append(sum(digitos))
        
        return {
            'soma_media': round(statistics.mean(somas), 2) if somas else 0,
            'soma_minima': min(somas) if somas else 0,
            'soma_maxima': max(somas) if somas else 0,
            'soma_mediana': round(statistics.median(somas), 2) if somas else 0
        }
    
    @staticmethod
    def analisar_pares_impares(numeros: List[str]) -> Dict[str, Any]:
        """Analisa distribuição de dígitos pares e ímpares"""
        pares_total = 0
        impares_total = 0
        total_digitos = 0
        
        for numero in numeros:
            digitos = [int(d) for d in str(numero).zfill(6)]
            pares_total += sum(1 for d in digitos if d % 2 == 0)
            impares_total += sum(1 for d in digitos if d % 2 != 0)
            total_digitos += 6
        
        return {
            'pares': pares_total,
            'impares': impares_total,
            'percentual_pares': round((pares_total / total_digitos * 100) if total_digitos > 0 else 0, 2),
            'percentual_impares': round((impares_total / total_digitos * 100) if total_digitos > 0 else 0, 2)
        }
