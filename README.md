Dashboard de Análise de Vendas

Um dashboard interativo para visualizar e analisar dados de vendas, com a possibilidade de adicionar novas vendas diretamente pela interface web.

O projeto utiliza Streamlit, Plotly e Pandas, consumindo dados de uma API REST.

🚀 Tecnologias utilizadas

Python 3.11+

Streamlit

Pandas

Plotly

Requests

API própria (FastAPI ou outra)

Docker (opcional, para deploy)

📦 Instalação

Crie e ative um ambiente virtual (recomendado):

python -m venv venv
# Windows
venv\Scripts\activate
# Linux / MacOS
source venv/bin/activate


Instale as dependências:

pip install -r requirements.txt

⚙️ Configuração

Defina a URL da sua API de vendas (opcional, padrão: http://api:8000):

export API_URL="http://localhost:8000"
# Windows PowerShell
$env:API_URL="http://localhost:8000"


Adicione o logo da loja na pasta assets/ com o nome logo1.png.

🖥️ Como rodar

Execute o Streamlit:

streamlit run app.py


O dashboard abrirá automaticamente no navegador em: http://localhost:8501

📊 Funcionalidades
Aba 1: Visualização de Dados

Filtros por categoria de produto.

Gráfico de barras: Receita total por categoria.

Gráfico donut: Proporção de vendas por categoria.

Evolução da receita por data (quando uma categoria específica é selecionada).

Tabela interativa de vendas.

Aba 2: Inserir Novos Dados

Formulário para adicionar novas vendas.

Suporte a categorias existentes ou novas categorias.

Atualização automática do dashboard após envio.

📷 Exemplos do Dashboard

Header com logo e título


Gráfico de barras e donut


Tabela de vendas


🛠️ Estrutura do Projeto
dashboard-vendas/
│
├─ app.py                 # Aplicação principal do Streamlit
├─ requirements.txt       # Dependências do projeto
├─ assets/
│   ├─ logo1.png          # Logo do dashboard
│   ├─ screenshot_header.png
│   ├─ screenshot_charts.png
│   └─ screenshot_table.png
└─ README.md

🔗 API Endpoints utilizados

GET /vendas → retorna todas as vendas

GET /vendas/analise → retorna dados agregados para análise

POST /vendas → insere uma nova venda

🐳 Deploy com Docker

Crie um Dockerfile no projeto:

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]


Construa e execute o container:

docker build -t dashboard-vendas .
docker run -p 8501:8501 -e API_URL="http://api:8000" dashboard-vendas


O dashboard estará disponível em: http://localhost:8501

👨‍💻 Autor

Nome: Sandro

Email: sandro.f67@gmail.com

GitHub:Sandroimpacta



