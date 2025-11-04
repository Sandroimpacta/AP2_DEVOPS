import streamlit as st # type: ignore
import pandas as pd
import plotly.express as px # type: ignore
import requests
import os
import base64
from datetime import datetime

# ================= CONFIGURAÇÃO =================
API_URL = os.environ.get("API_URL", "http://api:8000")

st.set_page_config(
    page_title="Dashboard de Análise de Vendas",
    layout="wide",
    initial_sidebar_state="auto"
)

# ================= HEADER =================

def render_header():
    # Carregar logo e converter para Base64
    with open("assets/logo1.png", "rb") as f:
        logo_bytes = f.read()
    logo_base64 = base64.b64encode(logo_bytes).decode()

    # HTML do header com degradê e logo dentro de um div amarelo
    st.markdown(
        f"""
        <div style="
            display: flex;
            align-items: center;
            background: linear-gradient(90deg, #FFFACD 0%, #FFEFD5 100%);
            padding: 15px 25px;
            border-radius: 10px;
            margin-bottom: 20px;
        ">
            <div style="
                background-color: #FFFACD;
                padding: 10px;
                border-radius: 10px;
            ">
                <img src="data:image/png;base64,{logo_base64}" width="80">
            </div>
            <h1 style="
                margin: 0;
                color: #333333;
                font-size: 2rem;
                font-family: Arial, sans-serif;
                margin-left: 20px;
            ">Loja de Vendas</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

render_header()


st.write("Dashboard interativo para análise de dados de vendas")

# ================= FUNÇÕES =================
@st.cache_data(ttl=300)
def carregar_vendas():
    response = requests.get(f"{API_URL}/vendas")
    return pd.DataFrame(response.json())

@st.cache_data(ttl=300)
def carregar_analise():
    response = requests.get(f"{API_URL}/vendas/analise")
    return pd.DataFrame(response.json())

def inserir_venda(dados):
    response = requests.post(f"{API_URL}/vendas", json=dados)
    return response.status_code in [200, 201]

# ================= MAIN =================
try:
    # Carregar dados
    df_vendas = carregar_vendas()
    df_analise = carregar_analise()
    
    tab1, tab2 = st.tabs(["Visualização de Dados", "Inserir Novos Dados"])
    
    with tab1:
        st.subheader("Filtros")
        categorias = ["Todas"] + sorted(df_vendas["categoria"].unique().tolist())
        categoria_selecionada = st.selectbox("Selecione uma categoria:", categorias)
        
        col1, col2 = st.columns(2)
        
        # ========== GRÁFICO DE BARRAS ==========
        with col1:
            st.subheader("Receita Total por Categoria")
            fig1 = px.bar(
                df_analise,
                x="categoria",
                y="receita_total",
                text_auto=True,
                color="categoria",
                title="Receita Total por Categoria de Produto"
            )
            fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig1, use_container_width=True)
        
        # ========== GRÁFICO DONUT ==========
        with col2:
            st.subheader("Proporção de Vendas por Categoria")
            fig2 = px.pie(
                df_analise,
                values="total_vendas",
                names="categoria",
                hole=0.5,  # Donut
                title="Distribuição de Vendas por Categoria"
            )
            fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig2, use_container_width=True)
        
        # ========== TABELAS ==========
        st.subheader("Dados de Vendas")
        st.dataframe(df_vendas)
        
        if categoria_selecionada != "Todas":
            df_filtrado = df_vendas[df_vendas["categoria"] == categoria_selecionada]
            st.subheader(f"Vendas na categoria: {categoria_selecionada}")
            st.dataframe(df_filtrado)
            
            if not df_filtrado.empty:
                df_por_data = df_filtrado.groupby("data_venda").agg(
                    {"valor": lambda x: (x * df_filtrado["quantidade"]).sum()}
                ).reset_index()
                df_por_data.columns = ["data", "receita"]
                
                fig3 = px.line(
                    df_por_data,
                    x="data",
                    y="receita",
                    markers=True,
                    title=f"Evolução de Receita: {categoria_selecionada}"
                )
                fig3.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig3, use_container_width=True)
    
    with tab2:
        st.subheader("Adicionar Nova Venda")
        with st.form("nova_venda_form"):
            data_venda = st.date_input("Data da Venda", datetime.now().date())
            produto = st.text_input("Nome do Produto")
            
            usar_categoria_existente = st.checkbox("Usar categoria existente", value=True)
            if usar_categoria_existente and not df_vendas.empty:
                categoria = st.selectbox("Categoria", sorted(df_vendas["categoria"].unique().tolist()))
            else:
                categoria = st.text_input("Nova Categoria")
            
            valor = st.number_input("Valor Unitário (R$)", min_value=0.01, format="%.2f")
            quantidade = st.number_input("Quantidade", min_value=1, step=1)
            
            submitted = st.form_submit_button("Adicionar Venda")
            
            if submitted:
                if not produto or not categoria:
                    st.error("Todos os campos são obrigatórios!")
                else:
                    nova_venda = {
                        "data_venda": data_venda.isoformat(),
                        "produto": produto,
                        "categoria": categoria,
                        "valor": valor,
                        "quantidade": quantidade
                    }
                    if inserir_venda(nova_venda):
                        st.success("Venda adicionada com sucesso!")
                        st.cache_data.clear()
                        st.experimental_rerun()
                    else:
                        st.error("Erro ao adicionar venda. Verifique os dados e tente novamente.")
    
except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    st.warning("Verifique se a API está disponível e funcionando corretamente.")
