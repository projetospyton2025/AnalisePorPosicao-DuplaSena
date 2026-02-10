import random
import logging
from typing import List
from models.dia_de_sorte import Palpite
from services.analisador import AnalisadorService

logger = logging.getLogger(__name__)

class GeradorPalpitesService:
    """Serviço para geração inteligente de palpites"""
    
    MESES = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
             'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    
    @classmethod
    def gerar_palpites(cls, quantidade: int = 5) -> List[Palpite]:
        """
        Gera múltiplos palpites usando diferentes estratégias
        
        Args:
            quantidade: Número de palpites a gerar
            
        Returns:
            Lista de palpites gerados
        """
        palpites = []
        estrategias = [
            cls._estrategia_balanceada,
            cls._estrategia_frequencia,
            cls._estrategia_por_faixas,
            cls._estrategia_aleatoria_inteligente,
            cls._estrategia_mista
        ]
        
        for i in range(min(quantidade, len(estrategias))):
            try:
                palpite = estrategias[i]()
                if palpite:
                    palpites.append(palpite)
            except Exception as e:
                logger.error(f"Erro ao gerar palpite com estratégia {i}: {e}")
        
        # Se pediu mais palpites do que estratégias, gera aleatórios
        while len(palpites) < quantidade:
            try:
                palpite = cls._estrategia_aleatoria_inteligente()
                if palpite:
                    palpites.append(palpite)
            except Exception as e:
                logger.error(f"Erro ao gerar palpite adicional: {e}")
                break
        
        return palpites
    
    @classmethod
    def _estrategia_balanceada(cls) -> Palpite:
        """Estratégia balanceada: combina dezenas frequentes e raras"""
        frequencias = AnalisadorService.analisar_frequencia_dezenas(100)
        
        # Ordena por frequência
        ordenadas = sorted(frequencias.items(), key=lambda x: x[1], reverse=True)
        
        # Pega 4 das mais frequentes (top 10)
        mais_frequentes = [d for d, _ in ordenadas[:10]]
        dezenas_selecionadas = random.sample(mais_frequentes, 4)
        
        # Pega 3 das menos frequentes (bottom 10)
        menos_frequentes = [d for d, _ in ordenadas[-10:]]
        dezenas_selecionadas += random.sample(menos_frequentes, 3)
        
        # Mês mais frequente
        meses_freq = AnalisadorService.analisar_meses_sorte(100)
        mes_sugerido = max(meses_freq.items(), key=lambda x: x[1])[0]
        
        return Palpite(
            dezenas=dezenas_selecionadas,
            mes_sugerido=mes_sugerido,
            estrategia="Balanceada",
            confianca="Média-Alta",
            justificativa="Combina 4 dezenas mais sorteadas com 3 menos sorteadas para equilíbrio"
        )
    
    @classmethod
    def _estrategia_frequencia(cls) -> Palpite:
        """Estratégia baseada puramente em frequência histórica"""
        frequencias = AnalisadorService.analisar_frequencia_dezenas(100)
        
        # Pega as 15 mais frequentes
        ordenadas = sorted(frequencias.items(), key=lambda x: x[1], reverse=True)
        candidatas = [d for d, _ in ordenadas[:15]]
        
        # Seleciona 7 aleatoriamente entre as candidatas
        dezenas_selecionadas = random.sample(candidatas, 7)
        
        # Mês mais frequente
        meses_freq = AnalisadorService.analisar_meses_sorte(100)
        mes_sugerido = max(meses_freq.items(), key=lambda x: x[1])[0]
        
        return Palpite(
            dezenas=dezenas_selecionadas,
            mes_sugerido=mes_sugerido,
            estrategia="Por Frequência",
            confianca="Alta",
            justificativa="Baseado nas 15 dezenas mais sorteadas historicamente"
        )
    
    @classmethod
    def _estrategia_por_faixas(cls) -> Palpite:
        """Estratégia que distribui dezenas por faixas (baixa, média, alta)"""
        frequencias = AnalisadorService.analisar_frequencia_dezenas(100)
        
        # Divide por faixas
        baixas = [d for d in range(1, 11) if frequencias.get(d, 0) > 0]
        medias = [d for d in range(11, 21) if frequencias.get(d, 0) > 0]
        altas = [d for d in range(21, 32) if frequencias.get(d, 0) > 0]
        
        # Distribui: 2 baixas, 2 médias, 3 altas (baseado nos 35% de altas)
        dezenas_selecionadas = []
        
        if len(baixas) >= 2:
            dezenas_selecionadas += random.sample(baixas, 2)
        elif baixas:
            dezenas_selecionadas += random.sample(baixas, len(baixas))
        
        if len(medias) >= 2:
            dezenas_selecionadas += random.sample(medias, 2)
        elif medias:
            dezenas_selecionadas += random.sample(medias, len(medias))
        
        if len(altas) >= 3:
            dezenas_selecionadas += random.sample(altas, 3)
        elif altas:
            dezenas_selecionadas += random.sample(altas, min(3, len(altas)))
        
        # Completa se necessário
        while len(dezenas_selecionadas) < 7:
            candidata = random.randint(1, 31)
            if candidata not in dezenas_selecionadas:
                dezenas_selecionadas.append(candidata)
        
        # Mês aleatório ponderado
        meses_freq = AnalisadorService.analisar_meses_sorte(100)
        meses_ponderados = [m for m, f in meses_freq.items() for _ in range(f + 1)]
        mes_sugerido = random.choice(meses_ponderados) if meses_ponderados else random.choice(cls.MESES)
        
        return Palpite(
            dezenas=dezenas_selecionadas[:7],
            mes_sugerido=mes_sugerido,
            estrategia="Por Faixas",
            confianca="Média",
            justificativa="Distribuição equilibrada: 2 baixas (1-10), 2 médias (11-20), 3 altas (21-31)"
        )
    
    @classmethod
    def _estrategia_aleatoria_inteligente(cls) -> Palpite:
        """Estratégia aleatória mas com peso estatístico"""
        frequencias = AnalisadorService.analisar_frequencia_dezenas(100)
        
        # Cria pool ponderado (dezenas aparecem proporcionalmente à frequência)
        pool = []
        for dezena, freq in frequencias.items():
            pool.extend([dezena] * (freq + 1))  # +1 para incluir até as com freq 0
        
        # Seleciona 7 únicas
        dezenas_selecionadas = []
        tentativas = 0
        while len(dezenas_selecionadas) < 7 and tentativas < 100:
            dezena = random.choice(pool)
            if dezena not in dezenas_selecionadas:
                dezenas_selecionadas.append(dezena)
            tentativas += 1
        
        # Mês aleatório ponderado
        meses_freq = AnalisadorService.analisar_meses_sorte(100)
        meses_ponderados = [m for m, f in meses_freq.items() for _ in range(f + 1)]
        mes_sugerido = random.choice(meses_ponderados) if meses_ponderados else random.choice(cls.MESES)
        
        return Palpite(
            dezenas=dezenas_selecionadas,
            mes_sugerido=mes_sugerido,
            estrategia="Aleatória Inteligente",
            confianca="Média-Baixa",
            justificativa="Seleção aleatória ponderada pela frequência histórica"
        )
    
    @classmethod
    def _estrategia_mista(cls) -> Palpite:
        """Estratégia que mistura elementos de todas as outras"""
        frequencias = AnalisadorService.analisar_frequencia_dezenas(100)
        ordenadas = sorted(frequencias.items(), key=lambda x: x[1], reverse=True)
        
        dezenas_selecionadas = []
        
        # 2 das top 5
        top5 = [d for d, _ in ordenadas[:5]]
        dezenas_selecionadas += random.sample(top5, min(2, len(top5)))
        
        # 2 da faixa média (posições 10-20)
        medias = [d for d, _ in ordenadas[10:20]]
        if len(medias) >= 2:
            dezenas_selecionadas += random.sample(medias, 2)
        
        # 1 das menos frequentes
        menos_freq = [d for d, _ in ordenadas[-5:]]
        if menos_freq:
            dezenas_selecionadas += random.sample(menos_freq, 1)
        
        # Completa com aleatórias
        while len(dezenas_selecionadas) < 7:
            candidata = random.randint(1, 31)
            if candidata not in dezenas_selecionadas:
                dezenas_selecionadas.append(candidata)
        
        # Mês mais frequente
        meses_freq = AnalisadorService.analisar_meses_sorte(100)
        mes_sugerido = max(meses_freq.items(), key=lambda x: x[1])[0]
        
        return Palpite(
            dezenas=dezenas_selecionadas[:7],
            mes_sugerido=mes_sugerido,
            estrategia="Mista",
            confianca="Alta",
            justificativa="Combina elementos de todas as estratégias: top frequentes, médias e raras"
        )
