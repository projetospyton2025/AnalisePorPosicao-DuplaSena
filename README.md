<<<<<<< HEAD
# Análise Por Posição - Dupla Sena

Aplicação web para análise estatística dos resultados da Dupla Sena por posição dos números sorteados.

## 📊 Descrição

Este projeto é uma aplicação web Flask que realiza análise estatística dos resultados históricos da Dupla Sena, focando especificamente na posição de cada número sorteado. A Dupla Sena sorteia 6 números de 1 a 50 em dois sorteios por concurso. Esta ferramenta analisa a frequência e distribuição dos números em cada uma das 6 posições (do menor ao maior número sorteado).

## ✨ Funcionalidades

- 🌐 **Interface Web Moderna**: Interface responsiva e intuitiva usando Bootstrap
- 🔍 **Busca de resultados**: Obtém resultados históricos diretamente da API oficial da Caixa
- 📈 **Análise estatística por posição**: Calcula média, mediana, moda, desvio padrão e frequências
- 🎯 **Sugestões de números**: Gera sugestões baseadas nos números mais frequentes em cada posição
- 📊 **Visualização interativa**: Gráficos e tabelas para melhor compreensão dos dados
- 🔄 **API REST**: Endpoints JSON para integração com outras aplicações

## 🏗️ Arquitetura Modular

```
AnalisePorPosicao-DuplaSena/
├── app.py                  # Aplicação Flask principal
├── models/                 # Modelos de dados
│   ├── __init__.py
│   └── dupla_sena.py      # Concurso, EstatisticaPosicao
├── services/              # Serviços de negócio
│   ├── __init__.py
│   ├── fetcher.py         # Busca de resultados da API
│   └── analisador.py      # Análise estatística
├── routes/                # Rotas da aplicação
│   ├── __init__.py
│   └── main.py            # Rotas principais
├── templates/             # Templates HTML
│   ├── base.html
│   ├── index.html
│   └── analise.html
├── static/                # Arquivos estáticos
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── script.js
│       └── analise.js
├── requirements.txt       # Dependências
└── README.md
```

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

3. Execute a aplicação:
```bash
python app.py
```

4. Acesse no navegador:
```
http://localhost:5000
```

## 📖 Uso

### Interface Web

1. **Página Inicial**: Visualize o último concurso e informações sobre o sistema
2. **Página de Análise**: Configure e execute análises personalizadas
   - Escolha entre últimos N concursos ou intervalo específico
   - Visualize estatísticas detalhadas por posição
   - Obtenha sugestões baseadas em frequência histórica

### API Endpoints

#### Buscar último concurso
```bash
GET /api/ultimo-concurso
```

#### Buscar concurso específico
```bash
GET /api/buscar-concurso/<numero>
```

#### Realizar análise
```bash
POST /api/analisar
Content-Type: application/json

{
  "quantidade": 50
}
# ou
{
  "inicio": 2500,
  "fim": 2600
}
```

#### Obter sugestões
```bash
GET /api/sugestoes?quantidade=50
```

## 📊 Exemplo de Saída

A aplicação web exibe:

1. **Dashboard Inicial**:
   - Último concurso atualizado
   - Navegação intuitiva
   - Informações sobre o sistema

2. **Análise Por Posição**:
   - Configuração flexível de análise
   - Estatísticas por posição (média, mediana, moda, desvio padrão)
   - Top 10 números mais frequentes com percentuais
   - Visualização em abas (1º e 2º sorteio)

3. **Sugestões de Números**:
   - Top 5 números mais frequentes para cada posição
   - Separado por sorteio
   - Visualização destacada

## 🔧 Módulos

### `models/dupla_sena.py`
Define os modelos de dados:
- **Concurso**: Representa um concurso com seus sorteios
- **EstatisticaPosicao**: Armazena estatísticas de uma posição

### `services/fetcher.py`
Serviço de busca de dados:
- **DuplaSenaService**: Busca resultados da API da Caixa
- Métodos para buscar concursos individuais, múltiplos ou últimos N
- Persistência em JSON

### `services/analisador.py`
Serviço de análise estatística:
- **AnalisadorService**: Realiza análises por posição
- Calcula métricas estatísticas
- Gera sugestões baseadas em frequência

### `routes/main.py`
Rotas da aplicação web:
- Páginas HTML (index, análise)
- API REST endpoints
- Integração com serviços

## 📝 Tecnologias Utilizadas

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **UI Framework**: Bootstrap 5
- **API**: Caixa Econômica Federal (Loterias)

## 🎲 Sobre a Dupla Sena

A Dupla Sena é uma loteria brasileira onde:
- São sorteados 6 números de 1 a 50
- Há dois sorteios por concurso
- Os jogadores escolhem de 6 a 15 números
- Prêmios para acertos de 3, 4, 5 ou 6 números

## 🚀 Deploy

### Produção com Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker (opcional)

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

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
=======
A
>>>>>>> 92a548fba3c714403ad6019eb255c32ddf907373
