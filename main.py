#!/usr/bin/env python3
"""
Script principal para análise por posição da Dupla Sena.
"""
import argparse
import sys
from fetcher import DuplaSenaFetcher
from analisador import AnalisePorPosicao


def main():
    """Função principal do programa."""
    parser = argparse.ArgumentParser(
        description='Análise por posição dos resultados da Dupla Sena',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:

  # Buscar os últimos 100 concursos e analisar
  python main.py --buscar 100

  # Buscar concursos específicos (do 2500 ao 2600)
  python main.py --buscar-range 2500 2600

  # Analisar dados já salvos em arquivo
  python main.py --analisar resultados_dupla_sena.json

  # Exibir apenas sugestões
  python main.py --analisar resultados_dupla_sena.json --sugestoes
        """
    )
    
    parser.add_argument(
        '--buscar',
        type=int,
        metavar='N',
        help='Busca os últimos N concursos da API'
    )
    
    parser.add_argument(
        '--buscar-range',
        nargs=2,
        type=int,
        metavar=('INICIO', 'FIM'),
        help='Busca concursos de INICIO até FIM'
    )
    
    parser.add_argument(
        '--analisar',
        type=str,
        metavar='ARQUIVO',
        help='Analisa resultados de um arquivo JSON'
    )
    
    parser.add_argument(
        '--sugestoes',
        action='store_true',
        help='Exibe apenas sugestões de números por posição'
    )
    
    parser.add_argument(
        '--salvar',
        type=str,
        metavar='ARQUIVO',
        default='resultados_dupla_sena.json',
        help='Nome do arquivo para salvar resultados (padrão: resultados_dupla_sena.json)'
    )
    
    args = parser.parse_args()
    
    # Validação de argumentos
    if not any([args.buscar, args.buscar_range, args.analisar]):
        parser.print_help()
        sys.exit(1)
    
    fetcher = DuplaSenaFetcher()
    resultados = []
    
    # Buscar dados
    if args.buscar:
        print(f"Buscando os últimos {args.buscar} concursos...")
        ultimo = fetcher.buscar_ultimo_concurso()
        if not ultimo:
            print("Erro ao buscar último concurso")
            sys.exit(1)
        
        numero_ultimo = ultimo['numero']
        numero_inicio = max(1, numero_ultimo - args.buscar + 1)
        
        resultados = fetcher.buscar_multiplos_concursos(numero_inicio, numero_ultimo)
        fetcher.salvar_resultados(args.salvar)
    
    elif args.buscar_range:
        inicio, fim = args.buscar_range
        print(f"Buscando concursos de {inicio} até {fim}...")
        if inicio > fim:
            print("Erro: número inicial deve ser menor que o número final")
            sys.exit(1)
        
        resultados = fetcher.buscar_multiplos_concursos(inicio, fim)
        fetcher.salvar_resultados(args.salvar)
    
    elif args.analisar:
        resultados = fetcher.carregar_resultados(args.analisar)
        if not resultados:
            print(f"Erro ao carregar resultados de {args.analisar}")
            sys.exit(1)
    
    # Análise
    if resultados:
        analisador = AnalisePorPosicao(resultados)
        
        if args.sugestoes:
            # Exibir apenas sugestões
            analisador.exibir_sugestoes(sorteio=1)
            analisador.exibir_sugestoes(sorteio=2)
        else:
            # Exibir análise completa
            analisador.exibir_analise()
            print("\n")
            analisador.exibir_sugestoes(sorteio=1)
            analisador.exibir_sugestoes(sorteio=2)
        
        print("\n" + "="*80)
        print("Análise concluída!")
        print("="*80)
    else:
        print("Nenhum resultado para analisar")
        sys.exit(1)


if __name__ == '__main__':
    main()
