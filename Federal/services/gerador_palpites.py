"""
Serviço de geração de palpites para Loteria Federal
"""
import random
from typing import List, Dict, Any
from collections import Counter
from models.federal import Palpite

class GeradorPalpitesService:
    """Gera palpites inteligentes baseados em estatísticas"""
    
    @staticmethod
    def gerar_numero_frequencia_balanceada(frequencias: Dict[int, Dict[str, int]]) -> str:
        """Gera número baseado na frequência histórica balanceada"""
        numero = ""
        for pos in range(1, 7):
            digitos_freq = frequencias.get(pos, {})
            if digitos_freq:
                # Escolhe com probabilidade proporcional à frequência
                digitos = list(digitos_freq.keys())
                pesos = list(digitos_freq.values())
                digito = random.choices(digitos, weights=pesos, k=1)[0]
                numero += digito
            else:
                numero += str(random.randint(0, 9))
        
        return numero.zfill(6)
    
    @staticmethod
    def gerar_numero_quente(numeros_recentes: List[str], limite: int = 50) -> str:
        """Gera número usando dígitos mais frequentes recentemente"""
        todos_digitos = []
        for numero in numeros_recentes[:limite]:
            todos_digitos.extend(list(str(numero).zfill(6)))
        
        frequencia = Counter(todos_digitos)
        digitos_quentes = [d for d, _ in frequencia.most_common(7)]
        
        numero = ""
        for _ in range(6):
            if digitos_quentes:
                numero += random.choice(digitos_quentes)
            else:
                numero += str(random.randint(0, 9))
        
        return numero.zfill(6)
    
    @staticmethod
    def gerar_numero_frio(numeros_recentes: List[str], limite: int = 50) -> str:
        """Gera número usando dígitos menos frequentes (contrarian)"""
        todos_digitos = []
        for numero in numeros_recentes[:limite]:
            todos_digitos.extend(list(str(numero).zfill(6)))
        
        frequencia = Counter(todos_digitos)
        # Pega os menos frequentes
        digitos_frios = [d for d, _ in sorted(frequencia.items(), key=lambda x: x[1])[:7]]
        
        numero = ""
        for _ in range(6):
            if digitos_frios:
                numero += random.choice(digitos_frios)
            else:
                numero += str(random.randint(0, 9))
        
        return numero.zfill(6)
    
    @staticmethod
    def gerar_numero_com_sequencia() -> str:
        """Gera número incluindo uma sequência"""
        # Gera uma sequência de 3 dígitos
        inicio_seq = random.randint(0, 7)
        sequencia = [str(inicio_seq + i) for i in range(3)]
        
        # Posiciona a sequência aleatoriamente
        posicao = random.randint(0, 3)
        
        numero = []
        for i in range(6):
            if posicao <= i < posicao + 3:
                numero.append(sequencia[i - posicao])
            else:
                numero.append(str(random.randint(0, 9)))
        
        return ''.join(numero)
    
    @staticmethod
    def gerar_numero_aleatorio_inteligente(soma_media: float) -> str:
        """Gera número aleatório mas respeitando soma média"""
        # Gera números até encontrar um com soma próxima da média
        for _ in range(100):
            numero = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            soma = sum(int(d) for d in numero)
            
            # Aceita se a soma estiver em um intervalo razoável
            if abs(soma - soma_media) <= 10:
                return numero
        
        # Se não encontrar, retorna qualquer um
        return ''.join([str(random.randint(0, 9)) for _ in range(6)])
    
    @classmethod
    def gerar_palpites(cls, dados_analise: Dict[str, Any], quantidade: int = 5) -> List[Palpite]:
        """Gera múltiplos palpites usando diferentes estratégias"""
        palpites = []
        
        frequencias = dados_analise.get('frequencia_digitos', {})
        numeros_recentes = dados_analise.get('numeros_recentes', [])
        soma_media = dados_analise.get('soma_numeros', {}).get('soma_media', 27)
        
        estrategias = [
            ('Frequência Balanceada', cls.gerar_numero_frequencia_balanceada, frequencias),
            ('Números Quentes', cls.gerar_numero_quente, numeros_recentes),
            ('Números Frios', cls.gerar_numero_frio, numeros_recentes),
            ('Com Sequência', cls.gerar_numero_com_sequencia, None),
            ('Aleatório Inteligente', cls.gerar_numero_aleatorio_inteligente, soma_media)
        ]
        
        for i, (nome, funcao, param) in enumerate(estrategias[:quantidade]):
            try:
                if param is not None:
                    if isinstance(param, dict):
                        numero = funcao(param)
                    elif isinstance(param, list):
                        numero = funcao(param)
                    else:
                        numero = funcao(param)
                else:
                    numero = funcao()
                
                confianca = 85 - (i * 5)  # Diminui levemente para cada estratégia
                
                palpite = Palpite(
                    numero=numero,
                    estrategia=nome,
                    confianca=confianca,
                    justificativa=cls._gerar_justificativa(nome, numero)
                )
                palpites.append(palpite)
            except Exception as e:
                print(f"Erro ao gerar palpite {nome}: {e}")
                continue
        
        return palpites
    
    @staticmethod
    def _gerar_justificativa(estrategia: str, numero: str) -> str:
        """Gera justificativa para o palpite"""
        justificativas = {
            'Frequência Balanceada': f'Baseado em padrões históricos de frequência. Soma dos dígitos: {sum(int(d) for d in numero)}',
            'Números Quentes': f'Usa dígitos mais frequentes nos últimos concursos. Soma: {sum(int(d) for d in numero)}',
            'Números Frios': f'Aposta em dígitos menos sorteados recentemente. Soma: {sum(int(d) for d in numero)}',
            'Com Sequência': f'Inclui sequência numérica detectada em padrões anteriores. Soma: {sum(int(d) for d in numero)}',
            'Aleatório Inteligente': f'Geração aleatória respeitando médias estatísticas. Soma: {sum(int(d) for d in numero)}'
        }
        return justificativas.get(estrategia, 'Palpite gerado por análise estatística')
