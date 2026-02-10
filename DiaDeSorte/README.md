# Análise por Posição - Dia de Sorte

Aplicação web para análise estatística e geração de palpites inteligentes para a loteria **Dia de Sorte** da Caixa Econômica Federal.

## 📋 Sobre o Dia de Sorte

O Dia de Sorte é uma modalidade de loteria onde:
- São sorteados **7 números** de 1 a 31
- É sorteado também um **Mês da Sorte**
- Os sorteios ocorrem às terças, quintas e sábados

## 🎯 Funcionalidades

### Análise Estatística
- **Frequência de Dezenas**: Análise das dezenas mais e menos sorteadas
- **Distribuição por Faixas**: Baixas (1-10), Médias (11-20), Altas (21-31)
- **Padrões de Sequências**: Detecção de sequências consecutivas
- **Finais Iguais**: Análise de dezenas com finais iguais
- **Mês da Sorte**: Estatísticas do mês da sorte

### Geração de Palpites Inteligentes
- **Estratégia Balanceada**: Combinação equilibrada de dezenas frequentes e raras
- **Estratégia por Frequência**: Baseada nas dezenas mais sorteadas
- **Estratégia por Faixas**: Distribuição equilibrada entre faixas
- **Estratégia Aleatória Inteligente**: Aleatoriedade com peso estatístico
- **Estratégia Mista**: Combinação de todas as estratégias

Cada palpite inclui:
- 7 dezenas selecionadas
- Sugestão de mês da sorte
- Nível de confiança
- Justificativa da estratégia

## 🚀 Como Usar

### Requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/projetospyton2025/AnalisePorPosicao-DuplaSena.git
cd AnalisePorPosicao-DuplaSena/DiaDeSorte
```

2. Crie um ambiente virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente (opcional):
```bash
export SECRET_KEY="sua-chave-secreta-aqui"
export FLASK_DEBUG="false"  # true para desenvolvimento
```

5. Execute a aplicação:
```bash
python app.py
```

6. Acesse no navegador:
```
http://localhost:5000
```

## 📦 Estrutura do Projeto

```
DiaDeSorte/
├── app.py                      # Aplicação Flask principal
├── requirements.txt            # Dependências Python
├── README.md                   # Este arquivo
├── .gitignore                  # Arquivos ignorados pelo Git
│
├── models/                     # Modelos de dados
│   ├── __init__.py
│   └── dia_de_sorte.py        # Classes Concurso e Palpite
│
├── services/                   # Lógica de negócio
│   ├── __init__.py
│   ├── fetcher.py             # Busca dados da API da Caixa
│   ├── analisador.py          # Análise estatística
│   └── gerador_palpites.py    # Geração de palpites
│
├── routes/                     # Rotas HTTP
│   ├── __init__.py
│   └── main.py                # Rotas da aplicação
│
├── templates/                  # Templates HTML
│   ├── base.html              # Template base
│   ├── index.html             # Página inicial
│   ├── analise.html           # Página de análise
│   └── palpites.html          # Página de palpites
│
└── static/                     # Arquivos estáticos
    ├── css/
    │   └── style.css          # Estilos personalizados
    └── js/
        └── script.js          # JavaScript

```

## 🎨 Tema Visual

A aplicação utiliza um tema dourado (#D4B31A) que reflete a identidade visual do Dia de Sorte:
- Cor principal: `#D4B31A`
- Interface responsiva com Bootstrap 5
- Design moderno e intuitivo

## 🔌 API da Caixa

A aplicação se conecta à API oficial da Caixa Econômica Federal:
```
https://servicebus2.caixa.gov.br/portaldeloterias/api/diadesorte
```

Endpoint para concurso específico:
```
https://servicebus2.caixa.gov.br/portaldeloterias/api/diadesorte/{numero}
```

## 📊 Algoritmos de Análise

### Frequência de Dezenas
Calcula quantas vezes cada dezena (1-31) foi sorteada historicamente.

### Distribuição por Faixas
- **Baixas**: 1-10 (33%)
- **Médias**: 11-20 (32%)
- **Altas**: 21-31 (35%)

### Padrões Identificados
1. **Sequências**: Números consecutivos (ex: 20, 21, 22)
2. **Finais Iguais**: 2-4 dezenas com mesmo final (ex: 12, 22)
3. **Combinações Frequentes**: Análise de combinações que mais aparecem

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:
1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## ⚠️ Aviso Legal

Esta aplicação é apenas para fins educacionais e de entretenimento. Os palpites gerados são baseados em análises estatísticas e não garantem ganhos. Jogue com responsabilidade.

## 👥 Autores

Desenvolvido por [projetospyton2025](https://github.com/projetospyton2025)

## 🔗 Links Úteis

- [Loterias Caixa](https://loterias.caixa.gov.br/)
- [Resultados Dia de Sorte](https://loterias.caixa.gov.br/Paginas/Dia-de-Sorte.aspx)
- [API Documentação](https://servicebus2.caixa.gov.br/portaldeloterias/)

---

**Boa sorte! 🍀**
