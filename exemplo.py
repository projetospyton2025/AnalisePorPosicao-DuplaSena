#!/usr/bin/env python3
"""
Script de exemplo demonstrando o uso dos módulos.
"""
from fetcher import DuplaSenaFetcher
from analisador import AnalisePorPosicao


def exemplo_basico():
    """Demonstra uso básico da ferramenta."""
    print("="*80)
    print("EXEMPLO DE USO - Análise Por Posição Dupla Sena")
    print("="*80)
    
    # Carrega dados de exemplo
    fetcher = DuplaSenaFetcher()
    resultados = fetcher.carregar_resultados('exemplo_resultados.json')
    
    if not resultados:
        print("Erro ao carregar dados de exemplo")
        return
    
    # Cria analisador
    analisador = AnalisePorPosicao(resultados)
    
    # Obtém e exibe análise completa
    analise = analisador.obter_analise_completa()
    
    print(f"\n✅ Análise de {analise['total_concursos']} concursos realizada com sucesso!")
    
    # Exibe sugestões
    print("\n" + "="*80)
    print("EXEMPLO: Obtendo sugestões programaticamente")
    print("="*80)
    
    sugestoes_s1 = analisador.obter_sugestoes(sorteio=1)
    sugestoes_s2 = analisador.obter_sugestoes(sorteio=2)
    
    print("\n📊 Sugestões para o Sorteio 1:")
    for pos, nums in sugestoes_s1.items():
        print(f"   Posição {pos}: {nums}")
    
    print("\n📊 Sugestões para o Sorteio 2:")
    for pos, nums in sugestoes_s2.items():
        print(f"   Posição {pos}: {nums}")
    
    print("\n" + "="*80)
    print("Para análise completa, use: python main.py --analisar exemplo_resultados.json")
    print("="*80)


if __name__ == '__main__':
    exemplo_basico()
