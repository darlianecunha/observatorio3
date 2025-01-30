import streamlit as st
import pandas as pd

# Definir estilo global com fundo branco e títulos azul escuro
st.markdown(
    """
    <style>
        body {
            background-color: white;
            color: black;
        }
        h1, h2 {
            color: #003366;
        }
        .stDataFrame, .stTable {
            background-color: white;
            color: black;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Cabeçalho do Dashboard
st.markdown("<h1 style='text-align: center; color: #003366;'>Dashboard de Mercadoria Movimentada pelo Setor Aquaviário por País e Produto</h1>", unsafe_allow_html=True)

# Carregar os dados
@st.cache_data
def load_data():
    file_path = "data.csv.xlsx"
    df = pd.read_excel(file_path)
    df = df.rename(columns={
        'Ano': 'ano',
        'Nomenclatura Simplificada': 'tipo_produto',
        'Total de Movimentação Portuária\nem toneladas (t)': 'movimentacao_total_t',
        'País Origem': 'pais'
    })
    df["ano"] = df["ano"].astype(int).astype(str)  # Garantir formato correto de ano
    return df

df = load_data()

# Filtros
st.sidebar.header("Filtros")
ano_selecionado = st.sidebar.selectbox("Selecione o Ano", sorted(df["ano"].unique()), index=0)
tipo_produto_selecionado = st.sidebar.selectbox("Selecione o Tipo de Produto", ["Todos"] + list(df["tipo_produto"].unique()), index=0)
pais_selecionado = st.sidebar.selectbox("Selecione o País", ["Todos"] + list(df["pais"].unique()), index=0)

# Aplicar filtros
df_filtered = df[df["ano"] == ano_selecionado]
if tipo_produto_selecionado != "Todos":
    df_filtered = df_filtered[df_filtered["tipo_produto"] == tipo_produto_selecionado]
if pais_selecionado != "Todos":
    df_filtered = df_filtered[df_filtered["pais"] == pais_selecionado]

# Agregar dados por ano
df_summary = df_filtered.groupby("ano", as_index=False)["movimentacao_total_t"].sum()

total_movimentacao = df[df["ano"] == ano_selecionado]["movimentacao_total_t"].sum()

if not df_summary.empty:
    df_summary["percentual"] = (df_summary["movimentacao_total_t"] / total_movimentacao) * 100
    df_summary["movimentacao_total_t"] = df_summary["movimentacao_total_t"].apply(lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    df_summary["percentual"] = df_summary["percentual"].apply(lambda x: f"{x:.2f}%")
    st.dataframe(df_summary, width=1000)
else:
    st.write("Nenhum dado disponível para os filtros selecionados.")

# Crédito 
st.write("Fonte: Estatístico Aquaviário ANTAQ")
st.markdown("<p><strong>Ferramenta desenvolvida por Darliane Cunha.</strong></p>", unsafe_allow_html=True)
