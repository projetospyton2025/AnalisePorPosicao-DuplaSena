# Análise Por Posição - Dupla Sena

Uma ferramenta Python para análise estatística dos resultados da Dupla Sena por posição dos números sorteados.

## 📊 Descrição

Este projeto realiza análise estatística dos resultados históricos da Dupla Sena, focando especificamente na posição de cada número sorteado. A Dupla Sena sorteia 6 números de 1 a 50 em dois sorteios por concurso. Esta ferramenta analisa a frequência e distribuição dos números em cada uma das 6 posições (do menor ao maior número sorteado).

## ✨ Funcionalidades

- 🔍 **Busca de resultados**: Obtém resultados históricos diretamente da API oficial da Caixa
- 📈 **Análise estatística por posição**: Calcula média, mediana, moda, desvio padrão e frequências
- 🎯 **Sugestões de números**: Gera sugestões baseadas nos números mais frequentes em cada posição
- 💾 **Armazenamento local**: Salva e carrega resultados em formato JSON
- 📊 **Relatórios detalhados**: Exibe análises completas formatadas no console

## 🚀 Instalação

### Requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

### Passos

1. Clone o repositório:
```bash
git clone https://github.com/projetospyton2025/AnalisePorPosicao-DuplaSena.git
cd AnalisePorPosicao-DuplaSena
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 📖 Uso

### Exemplos Básicos

#### Buscar e analisar os últimos 100 concursos
```bash
python main.py --buscar 100
```

#### Buscar concursos em um intervalo específico
```bash
python main.py --buscar-range 2500 2600
```

#### Analisar dados já salvos
```bash
python main.py --analisar resultados_dupla_sena.json
```

#### Exibir apenas sugestões de números
```bash
python main.py --analisar resultados_dupla_sena.json --sugestoes
```

### Opções da Linha de Comando

```
Argumentos:
  --buscar N              Busca os últimos N concursos da API
  --buscar-range I F      Busca concursos do número I até F
  --analisar ARQUIVO      Analisa resultados de um arquivo JSON
  --sugestoes             Exibe apenas sugestões (sem análise completa)
  --salvar ARQUIVO        Nome do arquivo para salvar (padrão: resultados_dupla_sena.json)
  -h, --help              Exibe ajuda
```

## 📊 Exemplo de Saída

A ferramenta exibe:

1. **Estatísticas por posição**:
   - Média dos números
   - Mediana
   - Moda (se houver)
   - Desvio padrão
   - Intervalo (mínimo e máximo)
   - Números únicos sorteados
   - Top 10 números mais frequentes com percentuais

2. **Sugestões de números**:
   - Top 5 números mais frequentes para cada posição
   - Separado por sorteio (1º e 2º sorteio)

## 🔧 Módulos

### `fetcher.py`
Responsável por buscar dados da API oficial da Caixa e gerenciar o armazenamento local dos resultados.

**Principais métodos:**
- `buscar_ultimo_concurso()`: Busca o concurso mais recente
- `buscar_concurso(numero)`: Busca um concurso específico
- `buscar_multiplos_concursos(inicio, fim)`: Busca múltiplos concursos
- `salvar_resultados(arquivo)`: Salva em JSON
- `carregar_resultados(arquivo)`: Carrega de JSON

### `analisador.py`
Realiza a análise estatística dos números por posição.

**Principais métodos:**
- `obter_analise_completa()`: Retorna análise dos dois sorteios
- `exibir_analise()`: Mostra análise formatada
- `obter_sugestoes(sorteio)`: Gera sugestões por posição
- `exibir_sugestoes(sorteio)`: Mostra sugestões formatadas

### `main.py`
Script principal que integra os módulos e fornece interface de linha de comando.

## 📝 Formato dos Dados

Os resultados são salvos em JSON com o seguinte formato (exemplo):
```json
[
  {
    "numero": 2500,
    "data": "01/01/2025",
    "listaDezenas": ["05", "12", "23", "34", "41", "48"],
    "listaDezenasSegundoSorteio": ["08", "15", "22", "31", "39", "45"]
  }
]
```

## 🎲 Sobre a Dupla Sena

A Dupla Sena é uma loteria brasileira onde:
- São sorteados 6 números de 1 a 50
- Há dois sorteios por concurso
- Os jogadores escolhem de 6 a 15 números
- Prêmios para acertos de 3, 4, 5 ou 6 números

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir novas funcionalidades
- Enviar pull requests

## ⚠️ Aviso Legal

Esta ferramenta é apenas para fins educacionais e de análise estatística. Os resultados não garantem ganhos em apostas. Jogue com responsabilidade.

## 📧 Contato

Projeto desenvolvido por projetospython2025

---

⭐ Se este projeto foi útil para você, considere dar uma estrela no GitHub!
