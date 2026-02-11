# Loteria Federal - Análise e Gerador de Palpites

Aplicação web para análise estatística e geração inteligente de palpites para a Loteria Federal.

## Sobre a Loteria Federal

A Loteria Federal é uma das modalidades de loteria mais tradicionais do Brasil:
- **5 prêmios** por concurso (1º ao 5º lugar)
- **Números de 6 dígitos** (000000 a 999999)
- **Sistema de séries** (A, B, C, D, E)
- **Prêmios fixos** (não acumulam)
- **Sorteios aos sábados**

## Funcionalidades

### 📊 Análise Estatística
- Frequência de dígitos por posição
- Números quentes e frios
- Detecção de padrões sequenciais
- Análise de últimos dígitos
- Estatísticas de soma e distribuição

### 🎯 Geração de Palpites
5 estratégias inteligentes baseadas em dados reais:
1. **Frequência Balanceada** - Baseado em frequência histórica
2. **Números Quentes** - Usa dígitos mais frequentes recentes
3. **Números Frios** - Usa dígitos menos frequentes
4. **Sequências** - Inclui padrões sequenciais
5. **Aleatório Inteligente** - Aleatório com restrições

## Instalação

```bash
# Clone o repositório
git clone https://github.com/projetospyton2025/AnalisePorPosicao-Federal.git
cd AnalisePorPosicao-Federal

# Instale as dependências
pip install -r requirements.txt

# Configure variáveis de ambiente (opcional)
export FLASK_DEBUG=false
export SECRET_KEY=sua-chave-secreta

# Execute a aplicação
python app.py
```

## Uso

Acesse `http://localhost:5000` no navegador.

### Páginas Disponíveis
- **Home** (`/`) - Visualiza último concurso
- **Análise** (`/analise`) - Estatísticas detalhadas
- **Palpites** (`/palpites`) - Gerador de números

### API Endpoints
- `GET /api/ultimo-concurso` - Dados do último concurso
- `POST /api/gerar-palpites` - Gera novos palpites

## Tecnologias

- **Backend:** Python 3.8+, Flask 3.0
- **Frontend:** Bootstrap 5, JavaScript
- **API:** Caixa Econômica Federal
- **Deployment:** Gunicorn

## Estrutura do Projeto

```
Federal/
├── app.py                  # Aplicação Flask
├── models/
│   └── federal.py         # Modelos de dados
├── services/
│   ├── fetcher.py         # Integração com API
│   ├── analisador.py      # Análise estatística
│   └── gerador_palpites.py # Geração de palpites
├── routes/
│   └── main.py            # Rotas HTTP
├── templates/             # Templates HTML
└── static/                # CSS e JavaScript
```

## Licença

MIT License

## Contato

Para dúvidas ou sugestões, abra uma issue no GitHub.
