# Loteca - Análise e Palpites Inteligentes

Aplicação web para análise estatística e geração de palpites inteligentes para a Loteca (Futebol).

![Loteca](https://i.postimg.cc/pr21mRdb/loteca.png)

## 📋 Sobre a Loteca

A Loteca é uma modalidade de loteria esportiva da Caixa Econômica Federal onde você aposta nos resultados de 14 jogos de futebol:

- **Coluna 1**: Vitória do time mandante (time 1)
- **Coluna do Meio**: Empate
- **Coluna 2**: Vitória do time visitante (time 2)

## 🎯 Funcionalidades

### 📊 Análise Estatística
- Distribuição de resultados (vitórias mandante, empates, vitórias visitante)
- Análise de vantagem do mandante
- Desempenho detalhado de cada time
- Histórico de confrontos diretos
- Estatísticas de aproveitamento

### 💡 Geração de Palpites
Estratégias inteligentes baseadas em dados reais:

1. **Equilibrado**: Baseado na distribuição histórica geral
2. **Favorito Mandante**: Prioriza vitórias dos times que jogam em casa
3. **Empates Estratégicos**: Inclui mais empates em jogos equilibrados
4. **Força Visitante**: Aposta em times visitantes surpreendentes
5. **Zebra**: Resultados improváveis (alto risco, alto retorno)

### 🔍 Dados em Tempo Real
- Integração com API oficial da Caixa Econômica Federal
- Busca de concursos anteriores
- Informações sobre prêmios e acumulação

## 🚀 Instalação e Uso

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

```bash
# Clone o repositório
git clone https://github.com/projetospyton2025/AnalisePorPosicao-Loteca.git
cd AnalisePorPosicao-Loteca/Loteca

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
python app.py
```

A aplicação estará disponível em: http://localhost:5000

### Variáveis de Ambiente (Opcional)

```bash
# Chave secreta para produção
export SECRET_KEY=sua-chave-secreta-aqui

# Modo debug (desenvolvimento)
export FLASK_DEBUG=true

# Porta personalizada
export PORT=5000
```

## 📁 Estrutura do Projeto

```
Loteca/
├── app.py                      # Aplicação Flask
├── requirements.txt            # Dependências Python
├── models/
│   ├── __init__.py
│   └── loteca.py              # Modelos de dados (Concurso, Jogo, Palpite)
├── services/
│   ├── __init__.py
│   ├── fetcher.py             # Serviço de busca de dados da API
│   ├── analisador.py          # Serviço de análise estatística
│   └── gerador_palpites.py    # Serviço de geração de palpites
├── routes/
│   ├── __init__.py
│   └── main.py                # Rotas HTTP e endpoints da API
├── templates/
│   ├── base.html              # Template base
│   ├── index.html             # Página inicial
│   ├── analise.html           # Página de análise
│   └── palpites.html          # Página de palpites
└── static/
    ├── css/
    │   └── style.css          # Estilos customizados
    └── js/
        └── script.js          # JavaScript utilities
```

## 🎨 Design

A aplicação utiliza o esquema de cores oficial da Loteca:

- **Azul Primário**: #0066B3 (Coluna 1)
- **Vermelho**: #F81A03 (Coluna 2)
- **Cinza Claro**: #F9FBFA (Fundo)

Interface responsiva com Bootstrap 5 para uma experiência otimizada em dispositivos móveis e desktop.

## 🔌 API Endpoints

### GET `/`
Página inicial com último concurso

### GET `/analise`
Página de análise estatística

### GET `/palpites`
Página de geração de palpites

### GET `/api/ultimo-concurso`
Retorna dados do último concurso em JSON

### GET `/api/buscar-concurso/<numero>`
Busca um concurso específico

### GET `/api/analise-estatistica`
Retorna análise estatística completa

### POST `/api/gerar-palpites`
Gera palpites com base em uma estratégia
```json
{
  "estrategia": "equilibrado"
}
```

## 📊 Fonte de Dados

Todos os dados são obtidos em tempo real da API oficial da Caixa Econômica Federal:
- API: https://servicebus2.caixa.gov.br/portaldeloterias/api/loteca
- Site oficial: https://loterias.caixa.gov.br

## ⚙️ Tecnologias

- **Backend**: Python 3.8+, Flask 3.0
- **Frontend**: HTML5, CSS3, JavaScript (ES6+), Bootstrap 5
- **API**: Requests
- **Deploy**: Gunicorn (production ready)

## 🚀 Deploy em Produção

### Usando Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Usando Docker (opcional)

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## ⚠️ Aviso Legal

Esta aplicação é apenas para fins educacionais e de análise estatística. Os palpites gerados não garantem acertos. Jogue com responsabilidade!

## 📝 Licença

MIT License - veja LICENSE para mais detalhes.

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abrir um Pull Request

## 📧 Contato

Para dúvidas ou sugestões, abra uma issue no repositório.

---

Desenvolvido com ❤️ para apostadores inteligentes da Loteca
