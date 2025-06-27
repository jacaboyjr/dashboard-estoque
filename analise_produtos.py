
import pandas as pd
import plotly.express as px
import streamlit as st

# Título para o Dashboard
st.title("Dashboard de Estoque - Depósito São Benedito")

# Leitura fixa da planilha
try:
    df = pd.read_excel("PRODUTOS_ATIVOS.xlsx")
except FileNotFoundError:
    st.error("❌ Arquivo PRODUTOS_ATIVOS.xlsx não encontrado no projeto.")
    st.stop()

# Exibir dados
st.subheader("📋 Primeiras Linhas da Planilha")
st.dataframe(df.head())

# Exibir colunas
st.write("📋 Colunas disponíveis: ", df.columns.tolist())

# Filtro produto com estoque > 0
coluna_estoque = "ESTOQUE"

if coluna_estoque in df.columns:
    df_pos = df[df[coluna_estoque] > 0].sort_values(by=coluna_estoque, ascending=False)

    st.subheader("TOP 20 produtos com maior estoque 🏆")
    st.dataframe(df_pos.head(20))

    # Gráfico de produtos com maior estoque
    fig = px.bar(df_pos.head(20), x="DESCRICAO", y=coluna_estoque, title="Top 20 produtos com maior Estoque", height=500)
    fig.update_traces(text=df_pos.head(20)[coluna_estoque], textposition='outside')
    st.plotly_chart(fig, use_container_width=True)

    # Produtos com estoque zerado ou negativo
    df_zero = df[df[coluna_estoque] == 0].sort_values(by=coluna_estoque, ascending=False)
    df_neg  = df[df[coluna_estoque] < 0 ].sort_values(by=coluna_estoque, ascending=False)

    st.subheader("🚨 Produtos com estoque negativo")
    st.dataframe(df_neg)

    fig_estoque_negativo = px.bar(
        df_neg.head(20),
        x="DESCRICAO",
        y=coluna_estoque,
        title="Top 20 produtos com estoque Negativo",
        height=500,
        color_discrete_sequence=["#FF0000"]
    )
    st.plotly_chart(fig_estoque_negativo, use_container_width=True, key="grafico_negativo")

    st.subheader("⚠️ Produtos com estoque ZERO")
    st.dataframe(df_zero)

    # TOTAL DE PRODUTOS
    qtd_total = df.shape[0]
    qtd_estoque_zero = (df[coluna_estoque] == 0).sum()
    qtd_estoque_negativo = (df[coluna_estoque] < 0).sum()
    total_unidades_em_estoque = df[df[coluna_estoque] > 0][coluna_estoque].sum()

    # Primeira linha (3 colunas)
    col1, col2, col3 = st.columns(3)

    col1.markdown(f"""
    <div style="
        text-align: center;
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    ">
        <h5 style="margin: 0;">🧾 Total de produtos</h5>
        <h2 style="margin: 0;">{f"{qtd_total:,.0f}".replace(",", ".")}</h2>
    </div>
    """, unsafe_allow_html=True)

    col2.markdown(f"""
    <div style="
        text-align: center;
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    ">
        <h5 style="margin: 0;">🚨 Estoque negativo</h5>
        <h2 style="margin: 0;">{f"{qtd_estoque_negativo:,.0f}".replace(",", ".")}</h2>
    </div>
    """, unsafe_allow_html=True)

    col3.markdown(f"""
    <div style="
        text-align: center;
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    ">
        <h5 style="margin: 0;">📦 Estoque 0</h5>
        <h2 style="margin: 0;">{f"{qtd_estoque_zero:,.0f}".replace(",", ".")}</h2>
    </div>
    """, unsafe_allow_html=True)

    # Segunda linha (1 coluna)
    valor_formatado = f"{total_unidades_em_estoque:,.0f}".replace(",", ".")
    col4, = st.columns(1)
    col4.markdown(f"""
    <div style="
        text-align: center;
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 20px;
        margin-top: 30px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    ">
        <h5 style="margin: 0;">📦 Unidades<br>em estoque</h5>
        <h2 style="margin: 0;">{valor_formatado}</h2>
    </div>
    """, unsafe_allow_html=True)
