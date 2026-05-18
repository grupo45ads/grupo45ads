import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="FIFA World Cup 2022 Dashboard",
    page_icon="⚽",
    layout="wide"
)

st.title("⚽ FIFA World Cup 2022 Dashboard")
st.markdown("""
Dashboard desenvolvido pelo Grupo 45 para análise dos dados da Copa do Mundo FIFA 2022.
A aplicação apresenta métricas gerais, visualizações gráficas e filtros interativos.
""")

# Carregamento da base
df = pd.read_csv("BaseDados/Fifa_world_cup_matches.csv")

# Padronização dos nomes das colunas
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("-", "_")
)

st.sidebar.header("Filtros")

# Mostrar colunas para conferência
with st.expander("Visualizar colunas da base de dados"):
    st.write(df.columns.tolist())
    st.dataframe(df.head())

# Tentativa de identificação automática das colunas
possiveis_time_1 = ["team1", "home_team", "team_a", "home", "team_1"]
possiveis_time_2 = ["team2", "away_team", "team_b", "away", "team_2"]
possiveis_gols_1 = ["team1_score", "home_score", "score1", "team_1_score"]
possiveis_gols_2 = ["team2_score", "away_score", "score2", "team_2_score"]
possiveis_fase = ["stage", "round", "phase"]

def encontrar_coluna(lista_possivel):
    for coluna in lista_possivel:
        if coluna in df.columns:
            return coluna
    return None

time_1_col = encontrar_coluna(possiveis_time_1)
time_2_col = encontrar_coluna(possiveis_time_2)
gols_1_col = encontrar_coluna(possiveis_gols_1)
gols_2_col = encontrar_coluna(possiveis_gols_2)
fase_col = encontrar_coluna(possiveis_fase)

if time_1_col and time_2_col and gols_1_col and gols_2_col:

    df[gols_1_col] = pd.to_numeric(df[gols_1_col], errors="coerce")
    df[gols_2_col] = pd.to_numeric(df[gols_2_col], errors="coerce")

    df["total_gols"] = df[gols_1_col] + df[gols_2_col]

    def definir_vencedor(linha):
        if linha[gols_1_col] > linha[gols_2_col]:
            return linha[time_1_col]
        elif linha[gols_2_col] > linha[gols_1_col]:
            return linha[time_2_col]
        else:
            return "Empate"

    df["vencedor"] = df.apply(definir_vencedor, axis=1)

    selecoes = sorted(set(df[time_1_col].dropna()) | set(df[time_2_col].dropna()))

    selecao_filtro = st.sidebar.multiselect(
        "Selecione as seleções:",
        selecoes,
        default=selecoes
    )

    df_filtrado = df[
        df[time_1_col].isin(selecao_filtro) |
        df[time_2_col].isin(selecao_filtro)
    ]

    if fase_col:
        fases = sorted(df[fase_col].dropna().unique())

        fase_filtro = st.sidebar.multiselect(
            "Selecione as fases:",
            fases,
            default=fases
        )

        df_filtrado = df_filtrado[df_filtrado[fase_col].isin(fase_filtro)]

    # Métricas principais
    total_partidas = len(df_filtrado)
    total_gols = int(df_filtrado["total_gols"].sum())
    media_gols = round(df_filtrado["total_gols"].mean(), 2)

    vitorias = df_filtrado[df_filtrado["vencedor"] != "Empate"]["vencedor"].value_counts()

    if not vitorias.empty:
        selecao_mais_vitorias = vitorias.idxmax()
        quantidade_vitorias = int(vitorias.max())
    else:
        selecao_mais_vitorias = "Sem dados"
        quantidade_vitorias = 0

    gols_time_1 = df_filtrado.groupby(time_1_col)[gols_1_col].sum()
    gols_time_2 = df_filtrado.groupby(time_2_col)[gols_2_col].sum()
    gols_por_selecao = gols_time_1.add(gols_time_2, fill_value=0).sort_values(ascending=False)

    if not gols_por_selecao.empty:
        selecao_mais_gols = gols_por_selecao.idxmax()
    else:
        selecao_mais_gols = "Sem dados"

    st.subheader("📊 Métricas gerais")

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Total de partidas", total_partidas)
    col2.metric("Total de gols", total_gols)
    col3.metric("Média de gols por partida", media_gols)
    col4.metric("Seleção com mais vitórias", selecao_mais_vitorias)
    col5.metric("Seleção com mais gols", selecao_mais_gols)

    st.divider()

    # Gráfico 1: gols por seleção
    st.subheader("⚽ Gols por seleção")

    gols_df = gols_por_selecao.reset_index()
    gols_df.columns = ["Seleção", "Gols"]

    fig_gols = px.bar(
        gols_df,
        x="Seleção",
        y="Gols",
        title="Total de gols por seleção",
        text="Gols"
    )

    st.plotly_chart(fig_gols, use_container_width=True)

    # Gráfico 2: vitórias por seleção
    st.subheader("🏆 Vitórias por seleção")

    vitorias_df = vitorias.reset_index()
    vitorias_df.columns = ["Seleção", "Vitórias"]

    fig_vitorias = px.bar(
        vitorias_df,
        x="Seleção",
        y="Vitórias",
        title="Total de vitórias por seleção",
        text="Vitórias"
    )

    st.plotly_chart(fig_vitorias, use_container_width=True)

    # Gráfico 3: partidas por fase
    if fase_col:
        st.subheader("📌 Partidas por fase da competição")

        partidas_fase = df_filtrado[fase_col].value_counts().reset_index()
        partidas_fase.columns = ["Fase", "Quantidade"]

        fig_fases = px.bar(
            partidas_fase,
            x="Fase",
            y="Quantidade",
            title="Quantidade de partidas por fase",
            text="Quantidade"
        )

        st.plotly_chart(fig_fases, use_container_width=True)

    # Tabela
    st.subheader("📋 Tabela com os dados filtrados")
    st.dataframe(df_filtrado)

else:
    st.error("Não foi possível identificar automaticamente as colunas principais da base.")

    st.warning("""
    Verifique os nomes das colunas do arquivo CSV.  
    O código precisa encontrar colunas referentes a:
    
    - seleção 1;
    - seleção 2;
    - gols da seleção 1;
    - gols da seleção 2.
    """)

    st.dataframe(df.head())
