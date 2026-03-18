# Bibliotecas e pacotes necessarios para realização da análise
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
import base64
from PIL import Image
import io
import plotly.colors as colors
from matplotlib import colors as mcolors
import plotly.graph_objects as go
import numpy as np
from scipy.stats import gaussian_kde

# CONFIGURAÇÃO GERAL
st.set_page_config(page_title="Indicadores de Mortalidade no Brasil", layout="wide")

# Logo UEPB
image1 = Image.open("Logo uepb.png")
buffered1 = io.BytesIO()
image1.save(buffered1, format="PNG")
img_base64_uepb = base64.b64encode(buffered1.getvalue()).decode()

# Logo EPBEST
#image2 = Image.open("EPBEST.png")
#buffered2 = io.BytesIO()
#image2.save(buffered2, format="PNG")
#img_base64_epbest = base64.b64encode(buffered2.getvalue()).decode()

# Tema e titulo do Streamilt
st.markdown(f"""
    <style>
        /* Fundo geral da página */
        body {{
            background-color: #c5974a;
            color: white;
        }}

        .stApp {{
            background-color: #1a2c5b;
        }}

        /* Barra do topo */
        .top-bar {{
            background-color: #1a2c5b;
            color: white;
            padding: 20px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-radius: 8px;
            box-shadow: 0px 4px 8px rgba(0,0,0,0.3);
        }}

        .text-content {{
            display: flex;
            flex-direction: column;
            max-width: 70%;
        }}

        .top-bar h1 {{
            margin: 0;
            font-size: 30px;
            font-weight: bold;
        }}

        .top-bar img {{
            height: 90px;
            margin-left: 15px; /* espaço entre as imagens */
        }}

        /* Container das imagens (lado a lado) */
        .logo-container {{
            display: flex;
            flex-direction: row;
            align-items: center;
        }}
    </style>

    <div class="top-bar">
        <div class="text-content">
            <h1>📊 Análise de Suicídio, Notificações e Hospitalizações por automutilação - CID-10 X60-X84</h1>
            <p></p>
        </div>
        <div class="logo-container">
            <img src="data:image/png;base64,{img_base64_uepb}" alt="Logo UEPB">
        </div>
    </div>
""", unsafe_allow_html=True)

# FUNÇÃO PARA CARREGAR AS BASES
@st.cache_data
def load_data():
    # Carregar Excel
    brasil = pd.read_excel("brasil.xlsx")

    # Idade
    notif_brasil = pd.read_excel("notif_brasil.xlsx")
    hosp_idade = pd.read_excel("hosp_idade.xlsx")
    notif_idade = pd.read_excel("notif_idade.xlsx")
    taxa_idade = pd.read_excel("taxa_idade.xlsx")

    # Raça/Cor
    hosp_racacor = pd.read_excel("hosp_racacor.xlsx")
    notif_racacor = pd.read_excel("notif_racacor.xlsx")
    taxa_racacor = pd.read_excel("taxa_racacor.xlsx")

    # Região
    hosp_regiao = pd.read_excel("hosp_regiao.xlsx")
    notif_regiao = pd.read_excel("notif_regiao.xlsx")
    taxa_regiao = pd.read_excel("taxa_regiao.xlsx")

    # Sexo
    hosp_Sexo = pd.read_excel("hosp_Sexo.xlsx")
    notif_Sexo = pd.read_excel("notif_Sexo.xlsx")
    taxa_Sexo = pd.read_excel("taxa_Sexo.xlsx")



    return (brasil, notif_brasil,
            hosp_idade, notif_idade, taxa_idade,
            hosp_racacor, notif_racacor, taxa_racacor,
            hosp_regiao, notif_regiao, taxa_regiao,
            hosp_Sexo, notif_Sexo, taxa_Sexo)

# Carregando os dados
(brasil, notif_brasil,
 hosp_idade, notif_idade, taxa_idade,
 hosp_racacor, notif_racacor, taxa_racacor,
 hosp_regiao, notif_regiao, taxa_regiao,
 hosp_Sexo, notif_Sexo, taxa_Sexo) = load_data()

bases = {
    "brasil": (brasil, "Ano", "Taxa"),
    "hosp_idade": (hosp_idade, "Ano", "Taxa de hospitalização"),
    "hosp_racacor": (hosp_racacor, "Ano", "Taxa de hospitalização"),
    "hosp_regiao": (hosp_regiao, "Ano", "Taxa de hospitalização"),
    "hosp_Sexo": (hosp_Sexo, "Ano", "Taxa de hospitalização"),
    "notif_brasil": (notif_brasil, "Ano", "taxa"),
    "notif_idade": (notif_idade, "Ano", "Taxa de notificação"),
    "notif_racacor": (notif_racacor, "Ano", "Taxa de notificação"),
    "notif_regiao": (notif_regiao, "Ano", "Taxa de notificação"),
    "notif_Sexo": (notif_Sexo, "Ano", "Taxa de notificação"),
    "taxa_idade": (taxa_idade, "Ano", "Taxa de suicídio"),
    "taxa_racacor": (taxa_racacor, "Ano", "Taxa de suicídio"),
    "taxa_regiao": (taxa_regiao, "Ano", "Taxa de suicídio"),
    "taxa_Sexo": (taxa_Sexo, "Ano", "Taxa de suicídio")
}


# FUNÇÃO PARA SÉRIES TEMPORAIS

def plot_series(df, Ano_col, value_col, group_col=None, title="", ylabel="Taxa por 100.000 hab."):
    plt.figure(figsize=(8,5))
    if group_col is None:
        plt.plot(df[Ano_col], df[value_col], marker="o", linewidth=2)
    else:
        for group, subset in df.groupby(group_col):
            plt.plot(subset[Ano_col], subset[value_col], marker="o", linewidth=2, label=str(group))
        plt.legend(title=group_col)
    plt.title(title, fontsize=13)
    plt.xlabel("Ano")
    plt.ylabel(ylabel)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    st.pyplot(plt.gcf())
    plt.close()

def plot_series(df, x_col, y_col, group_col=None, title=""):
    fig = px.line(
        df,
        x=x_col,
        y=y_col,
        color=group_col,
        markers=True,
        template="plotly_white",
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    # Aqui Força todos os anos no eixo X
    fig.update_xaxes(
        tickmode="array",
        tickvals=sorted(df[x_col].unique()),  # todos os anos únicos da base para o gráfico
        tickangle=0                           # ângulo das labels (0 = horizontal) - fica melhor assim acredito
    )

    fig.update_traces(line=dict(width=2))
    fig.update_layout(
        title=title,
        title_x=0.5,
        height=350,
        margin=dict(l=20, r=20, t=40, b=60),  # aumenta espaço p/ legenda abaixo e deixa melhor a visualização
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(
            orientation="h",        # horizontal
            yanchor="top",          # colocar no topo da legenda
            y=-0.25,                # move para baixo do eixo X
            xanchor="center",
            x=0.5,
            title=""
        )
    )

    st.plotly_chart(fig, use_container_width=True)

  

# Abas do app 
abas = st.tabs([
    "Documentação",
    "Introdução",
    "Metodologia",
    "Descritiva",
    "Comparitivo",
    "Séries Temporais",
    "Correlação",
    "Referências"
])


# DOCUMENTAÇÃO

with abas[0]:
    st.subheader("Sobre o Painel")
    st.markdown("""
  <div style="text-align: justify;">
                
📘 Documentação das Bases de Dados

As taxas foram calculadas utilizando como denominador a população residente em cada ano, Sexo, faixa etária, raça/cor e Região do Brasil. As estimativas populacionais foram obtidas junto ao Instituto Brasileiro de Geografia e Estatística (IBGE). Nos anos intercensitários, em que não havia dados diretos provenientes de censo ou projeções oficiais, foram aplicados métodos de extrapolação e interpolação linear para estimar a população de referência, conforme procedimento descrito por Alves et al. (2024), que detalham a metodologia de ajuste populacional e cálculo das taxas no contexto de análises de autolesão no Brasil. 

Observação geral: (Taxas padronizadas por 100.000 habitantes.)

Quadro 1: Descrição das Bases de Dados e sua Origem
                
| Bases de dados    | Origem                            | Variáveis de cada base de dados                  |
| ----------------- | --------------------------------- | ------------------------------------------------ |
| **brasil**        | SIH, SINAN, SIM                   | Ano, Brazil, Rate                               |
| **hospitalização**| SIH (Sistema de hospitalizações)  | Ano, Age, groups, n, pop, Taxa de hospitalização |
| **hospitalização por raça/cor**  | SIH (Sistema de hospitalizações)  | Ano, Race-color, n, pop, Taxa de hospitalização  |
| **hospitalização por Região**   | SIH (Sistema de hospitalizações)  | Ano, Região, n, pop, Taxa de hospitalização      |
| **hospitalização por Sexo**     | SIH (Sistema de hospitalizações)  | Ano, Sexo, n, pop, Taxa de hospitalização         | 
| **notificações por brasil**  | SINAN (Sist. de notificações)     | id, Ano, n, x, Taxa                              |
| **notificações por idade**   | SINAN (Sist. de notificações)     | Ano, Faixa etária, n, pop, Taxa de notificação     |
| **notificações por raça/cor** | SINAN (Sist. de notificações)     | Ano, Race-color, Taxa de notificação             |
| **notificações por Região**  | SINAN (Sist. de notificações)     | Ano, Região, n, pop, Taxa de notificação         |
| **notificações por Sexo**    | SINAN (Sist. de notificações)     | Ano, Sexo, n, pop, Taxa de notificação            |
| **Óbitos por idade**  | SIM (Sistema de mortalidade)      | Ano, n, Faixa etária, pop, Taxa de suicídio          |
| **Óbitos por raça/cor**| SIM (Sistema de mortalidade)      | Ano, Race-color, Taxa de suicídio                  |
| **Óbitos por Região** | SIM (Sistema de mortalidade)      | Ano, Região, n, pop, Taxa de suicídio              |
| **Óbitos por Sexo**   | SIM (Sistema de mortalidade)      | Ano, Sexo, n, pop, Taxa de suicídio                 |


</div>
                """, unsafe_allow_html=True)



# INTRODUÇÃO

with abas[1]:
    st.subheader("Introdução")
    st.markdown(
        """
<div style="text-align: justify; line-height: 1.6; font-size: 17px; color: white;">

A compreensão das tendências de autolesões, hospitalizações por automutilação e mortalidade por suicídio é essencial para o planejamento de políticas públicas, alocação de recursos e formulação de intervenções em saúde mental. A magnitude do problema é significativa em escala global, estimando-se que cerca de 700 mil pessoas morrem por suicídio anualmente, sendo o suicídio uma das principais causas de morte entre jovens (OMS, 2019). No Brasil, estudos indicam aumento das taxas de suicídio nas últimas décadas, com heterogeneidade Regiãoal, especialmente na Região Sul e em determinados grupos demográficos (Soares, 2022).

Além disso, fatores sociais, como a desigualdade de renda, foram apontados como importantes determinantes das variações nas taxas de suicídio (Machado et al., 2015). Neste estudo, foram consideradas notificações e hospitalizações por automutilação, uma vez que não é possível determinar com precisão a intenção do dano, isto é, se o evento era uma tentativa de suicídio ou outro tipo de autolesão. O uso combinado de diferentes sistemas de informação em saúde (notificações, internações e óbitos) permite captar múltiplas dimensões do problema e identificar lacunas no acesso a serviços de urgência e emergência.

Para caracterizar o comportamento das séries e as relações entre os indicadores, foram utilizados métodos exploratórios gráficos e estatísticos, como boxplots, histogramas, séries temporais e análises de dados, que auxiliaram na identificação de outliers, padrões temporais e associações entre variáveis.

</div>
        """,
        unsafe_allow_html=True
    )



# METODOLOGIA

with abas[2]:
    st.subheader("Materiais e Métodos")
    st.markdown("""
<div style="text-align: justify;">

A pesquisa foi conduzida no ambiente de programação Python, amplamente utilizado em análises de dados e ciência aberta (Van Rossum e Drake, 2022). O desenvolvimento dos scripts foi realizado no Visual Studio Code (VS Code), uma plataforma gratuita e multiplataforma que oferece integração com ambientes virtuais, depuração e suporte a Python, facilitando a organização e a reprodutibilidade do código (Microsoft, 2024).
                
O foco metodológico foi a análise exploratória de dados secundários provenientes de sistemas públicos de informação em saúde, com o objetivo de descrever distribuições, identificar padrões e construir representações gráficas e interativas. As etapas incluíram a limpeza, o tratamento e a padronização das variáveis, com a criação de boxplots, histogramas e séries temporais para análise de tendências e outliers, além da aplicação de análises para investigar associações entre variáveis (Silva, 2022).
                
Os resultados foram apresentados por meio de painéis digitais interativos desenvolvidos com o framework Streamlit, uma ferramenta open-source voltada para a criação de aplicações de ciência de dados de forma ágil e transparente (Streamlit, 2023). Essa combinação de Python, VS Code e Streamlit assegurou reprodutibilidade e clareza nas etapas da pesquisa, em conformidade com as boas práticas de ciência aberta (Serrapilheira, 2021).

</div>
                """, unsafe_allow_html=True)



# 2) BOXPLOTS E HISTOGRAMAS

with abas[3]:
    st.subheader("Boxplots e Histogramas Comparativos")

    # Dicionário de nomes mais legíveis para títulos
    nomes_legiveis = {
        "brasil": "Taxas gerais no Brasil",
        "hosp_idade": "Hospitalizações por faixa etária",
        "hosp_racacor": "Hospitalizações por raça/cor",
        "hosp_regiao": "Hospitalizações por Região",
        "hosp_Sexo": "Hospitalizações por Sexo",
        "notif_brasil": "Notificações gerais no Brasil",
        "notif_idade": "Notificações por faixa etária",
        "notif_racacor": "Notificações por raça/cor",
        "notif_regiao": "Notificações por Região",
        "notif_Sexo": "Notificações por Sexo",
        "taxa_idade": "Óbitos por suicídio - faixa etária",
        "taxa_racacor": "Óbitos por suicídio - raça/cor",
        "taxa_regiao": "Óbitos por suicídio - Região",
        "taxa_Sexo": "Óbitos por suicídio - Sexo"
    }

    # Agrupamento por dimensão temática
    grupos = {
        "Idade": {
            "Notificações": bases["notif_idade"],
            "Hospitalizações": bases["hosp_idade"],
            "Óbitos": bases["taxa_idade"]
        },
        "Raça/Cor": {
            "Notificações": bases["notif_racacor"],
            "Hospitalizações": bases["hosp_racacor"],
            "Óbitos": bases["taxa_racacor"]
        },
        "Sexo": {
            "Notificações": bases["notif_Sexo"],
            "Hospitalizações": bases["hosp_Sexo"],
            "Óbitos": bases["taxa_Sexo"]
        },
        "Região": {
            "Notificações": bases["notif_regiao"],
            "Hospitalizações": bases["hosp_regiao"],
            "Óbitos": bases["taxa_regiao"]
        }
    }

    # por dimensão (Raça/Cor, Sexo, etc.)
    for dimensao, sub_bases in grupos.items():
        st.markdown(f"## 📊 {dimensao}")

        cols = st.columns(len(sub_bases))

        for i, (tipo_base, (df, ano, taxa)) in enumerate(sub_bases.items()):
            with cols[i]:
                st.markdown(f"#### {tipo_base}")

                # BOXPLOT
                fig_box = px.box(
                    df,
                    y=taxa,
                    points="all",
                    color_discrete_sequence=["#1f77b4"],
                    template="plotly_white"
                )
                fig_box.update_layout(
                    title=f"Boxplot - {tipo_base}",
                    title_x=0.5,
                    height=300,
                    margin=dict(l=20, r=20, t=50, b=20),
                    showlegend=False,
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)"
                )
                st.plotly_chart(fig_box, use_container_width=True)

                # HISTOGRAMA 
                x_vals = df[taxa].dropna()
                if len(x_vals) > 1:
                    kde = gaussian_kde(x_vals)
                    x_range = np.linspace(x_vals.min(), x_vals.max(), 200)

                    fig_hist = px.histogram(
                        df,
                        x=taxa,
                        nbins=20,
                        histnorm="probability density",
                        opacity=0.6,
                        color_discrete_sequence=["#1f77b4"],
                        template="plotly_white"
                    )

                    fig_hist.add_trace(
                        go.Scatter(
                            x=x_range,
                            y=kde(x_range),
                            mode="lines",
                            line=dict(color="darkred", width=2),
                            name="Densidade"
                        )
                    )

                    fig_hist.update_layout(
                        title=f"Histograma - {tipo_base}",
                        title_x=0.5,
                        height=300,
                        margin=dict(l=20, r=20, t=50, b=20),
                        yaxis_title="Densidade",
                        plot_bgcolor="rgba(0,0,0,0)",
                        paper_bgcolor="rgba(0,0,0,0)"
                    )
                    st.plotly_chart(fig_hist, use_container_width=True)
                else:
                    st.warning("Dados insuficientes para gerar o histograma.")


# Comparativos

with abas[4]:
    st.subheader("Boxplots e Histogramas Comparativos")

    grupos = {
        "Idade": {
            "Notificações": bases["notif_idade"],
            "Hospitalizações": bases["hosp_idade"],
            "Óbitos": bases["taxa_idade"]
        },
        "Raça/Cor": {
            "Notificações": bases["notif_racacor"],
            "Hospitalizações": bases["hosp_racacor"],
            "Óbitos": bases["taxa_racacor"]
        },
        "Sexo": {
            "Notificações": bases["notif_Sexo"],
            "Hospitalizações": bases["hosp_Sexo"],
            "Óbitos": bases["taxa_Sexo"]
        },
        "Região": {
            "Notificações": bases["notif_regiao"],
            "Hospitalizações": bases["hosp_regiao"],
            "Óbitos": bases["taxa_regiao"]
        }
    }

    for dimensao, sub_bases in grupos.items():
        st.markdown(f"## 📊 {dimensao}")
        cols = st.columns(len(sub_bases))

        for i, (tipo_base, tupla_base) in enumerate(sub_bases.items()):
            df, ano, taxa = tupla_base

            with cols[i]:
                st.markdown(f"#### {tipo_base}")

                cat_col = df.select_dtypes(include=["object", "category"]).columns[0]
                df[cat_col] = df[cat_col].astype(str)
                categorias = df[cat_col].unique().tolist()
                valor_col = taxa

                # ===== BOXPLOTS =====
                fig_box = px.box(
                    df,
                    x=cat_col,
                    y=valor_col,
                    points="all",
                    color=cat_col,
                    category_orders={cat_col: categorias},
                    template="plotly_dark",
                    color_discrete_sequence=px.colors.qualitative.Set2
                )
                fig_box.update_layout(
                    title=f"Boxplot por {cat_col}",
                    title_x=0.5,
                    height=300,
                    margin=dict(l=20, r=20, t=50, b=20),
                    showlegend=False,
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)"
                )
                st.plotly_chart(fig_box, use_container_width=True)

                # ===== APENAS DENSIDADES (sem barras) =====
                fig_kde = go.Figure()
                all_vals = df[valor_col].dropna()
                x_min, x_max = all_vals.min(), all_vals.max()

                for cat in categorias:
                    x_vals = df[df[cat_col] == cat][valor_col].dropna()
                    if len(x_vals) > 1:
                        kde = gaussian_kde(x_vals)
                        x_range = np.linspace(x_min, x_max, 200)
                        fig_kde.add_trace(go.Scatter(
                            x=x_range,
                            y=kde(x_range),
                            mode="lines",
                            line=dict(width=2),
                            name=str(cat)
                        ))

                fig_kde.update_layout(
                    title=f"Distribuição por {cat_col}",
                    title_x=0.5,
                    height=300,
                    margin=dict(l=20, r=20, t=50, b=70),
                    yaxis_title="Densidade",
                    xaxis_title=None,
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    legend=dict(
                        orientation="h",
                        y=-0.3,
                        x=0.5,
                        xanchor="center",
                        yanchor="top",
                        font=dict(size=11),
                        bgcolor="rgba(0,0,0,0)"
                    )
                )
                fig_kde.update_xaxes(range=[x_min, x_max])
                st.plotly_chart(fig_kde, use_container_width=True)


# SÉRIES TEMPORAIS

with abas[5]:
    st.subheader("📈 Séries Temporais por Categoria")
    col1, col2 = st.columns(2)

    with col1:
        plot_series(taxa_Sexo, "Ano", "Taxa de suicídio", group_col="Sexo", title="Taxa de suicídio por Sexo")
        plot_series(notif_Sexo, "Ano", "Taxa de notificação", group_col="Sexo", title="Notificações por Sexo")
        plot_series(hosp_Sexo, "Ano", "Taxa de hospitalização", group_col="Sexo", title="Hospitalizações por Sexo")

        plot_series(taxa_idade, "Ano", "Taxa de suicídio", group_col="Faixa etária", title="Taxa de suicídio por idade")
        plot_series(notif_idade, "Ano", "Taxa de notificação", group_col="Faixa etária", title="Notificações por idade")
        plot_series(hosp_idade, "Ano", "Taxa de hospitalização", group_col="Faixa etária", title="Hospitalizações por idade")

    with col2:
        plot_series(taxa_racacor, "Ano", "Taxa de suicídio", group_col="Raça/cor", title="Taxa de suicídio por raça/cor")
        plot_series(notif_racacor, "Ano", "Taxa de notificação", group_col="Raça/cor", title="Notificações por raça/cor")
        plot_series(hosp_racacor, "Ano", "Taxa de hospitalização", group_col="Raça/cor", title="Hospitalizações por raça/cor")

        plot_series(taxa_regiao, "Ano", "Taxa de suicídio", group_col="Região", title="Taxa de suicídio por Região")
        plot_series(notif_regiao, "Ano", "Taxa de notificação", group_col="Região", title="Notificações por Região")
        plot_series(hosp_regiao, "Ano", "Taxa de hospitalização", group_col="Região", title="Hospitalizações por Região")



# CORRELAÇÕES

# =========================================================
#  ABA 6 — CORRELAÇÃO POR CATEGORIA
# =========================================================
with abas[6]:
    st.subheader("🔗 Correlação por Categoria - Óbitos, Notificações e Hospitalizações")

    import seaborn as sns
    import matplotlib.pyplot as plt

    # =========================================================
    # FUNÇÃO DE HEATMAP PADRONIZADA
    # =========================================================
    def plot_corr_heatmap(df, title):
        expected_cols = ["Óbitos", "Notificações", "Hospitalizações"]
        existing = [c for c in expected_cols if c in df.columns]

        # Verificação de colunas
        if len(existing) < 3:
            st.warning(f"⚠️ Colunas ausentes em {title}: faltando {set(expected_cols) - set(existing)}")
            return

        # Filtragem de dados
        df_numeric = df[existing].dropna()
        if df_numeric.shape[0] < 2:
            st.warning(f"⚠️ Dados insuficientes para gerar heatmap: {title}")
            return

        # Cálculo da correlação
        corr = df_numeric.corr()

        # Plotagem
        fig, ax = plt.subplots(figsize=(3, 3), facecolor="none")
        sns.heatmap(
            corr,
            annot=True,
            cmap="coolwarm",
            fmt=".2f",
            cbar=True,
            square=True,
            ax=ax
        )
        ax.set_title(title, fontsize=9, pad=8, weight="bold", color="white")
        fig.patch.set_alpha(0)
        ax.set_facecolor("none")

        # Remove bordas
        for spine in ax.spines.values():
            spine.set_visible(False)

        st.pyplot(fig)
        plt.close(fig)

    # =========================================================
    # 1️⃣ CORRELAÇÃO POR REGIÃO
    # =========================================================
    st.markdown("### 📊 Correlação por Região")

    try:
        df_regiao = (
            taxa_regiao.merge(notif_regiao, on=["Ano", "Região"], how="inner")
            .merge(hosp_regiao, on=["Ano", "Região"], how="inner")
        )

        df_regiao.rename(columns={
            "Taxa de suicídio": "Óbitos",
            "Taxa de notificação": "Notificações",
            "Taxa de hospitalização": "Hospitalizações"
        }, inplace=True)

        categorias_regiao = df_regiao["Região"].unique()

        for j in range(0, len(categorias_regiao), 2):
            row_cols = st.columns(2)
            for k, cat in enumerate(categorias_regiao[j:j+2]):
                df_cat = df_regiao[df_regiao["Região"] == cat]
                with row_cols[k]:
                    plot_corr_heatmap(df_cat, f"Região: {cat}")
    except Exception as e:
        st.error(f"Erro ao gerar correlação por Região: {e}")

    st.divider()

    # =========================================================
    # 2️⃣ CORRELAÇÃO POR SEXO
    # =========================================================
    st.markdown("### 📊 Correlação por Sexo")

    try:
        df_sexo = (
            taxa_Sexo.merge(notif_Sexo, on=["Ano", "Sexo"], how="inner")
            .merge(hosp_Sexo, on=["Ano", "Sexo"], how="inner")
        )

        df_sexo.rename(columns={
            "Taxa de suicídio": "Óbitos",
            "Taxa de notificação": "Notificações",
            "Taxa de hospitalização": "Hospitalizações"
        }, inplace=True)

        categorias_sexo = sorted(df_sexo["Sexo"].unique())

        for j in range(0, len(categorias_sexo), 2):
            row_cols = st.columns(2)
            for k, cat in enumerate(categorias_sexo[j:j+2]):
                df_cat = df_sexo[df_sexo["Sexo"] == cat]
                with row_cols[k]:
                    plot_corr_heatmap(df_cat, f"Sexo: {cat}")
    except Exception as e:
        st.error(f"Erro ao gerar correlação por Sexo: {e}")

    st.divider()

    # =========================================================
    # 3️⃣ CORRELAÇÃO POR FAIXA ETÁRIA
    # =========================================================
    st.markdown("### 📊 Correlação por Faixa Etária")

    try:
        # Padroniza faixas etárias nas notificações
        notif_idade["Faixa etária"] = notif_idade["Faixa etária"].replace({
            "10-24": "10-24",
            "20-24": "25-59"
        })

        df_idade = (
            taxa_idade.merge(notif_idade, on=["Ano", "Faixa etária"], how="inner")
            .merge(hosp_idade, on=["Ano", "Faixa etária"], how="inner")
        )

        df_idade.rename(columns={
            "Taxa de suicídio": "Óbitos",
            "Taxa de notificação": "Notificações",
            "Taxa de hospitalização": "Hospitalizações"
        }, inplace=True)

        categorias_idade = df_idade["Faixa etária"].unique()

        for j in range(0, len(categorias_idade), 2):
            row_cols = st.columns(2)
            for k, cat in enumerate(categorias_idade[j:j+2]):
                df_cat = df_idade[df_idade["Faixa etária"] == cat]
                with row_cols[k]:
                    plot_corr_heatmap(df_cat, f"Faixa Etária: {cat}")
    except Exception as e:
        st.error(f"Erro ao gerar correlação por Faixa Etária: {e}")

    st.divider()

    # =========================================================
    # 4️⃣ CORRELAÇÃO POR RAÇA/COR
    # =========================================================
    st.markdown("### 📊 Correlação por Raça/Cor")

    try:
        df_racacor = (
            taxa_racacor.merge(notif_racacor, on=["Ano", "Raça/cor"], how="inner")
            .merge(hosp_racacor, on=["Ano", "Raça/cor"], how="inner")
        )

        df_racacor.rename(columns={
            "Taxa de suicídio": "Óbitos",
            "Taxa de notificação": "Notificações",
            "Taxa de hospitalização": "Hospitalizações"
        }, inplace=True)

        categorias_racacor = df_racacor["Raça/cor"].unique()

        for j in range(0, len(categorias_racacor), 2):
            row_cols = st.columns(2)
            for k, cat in enumerate(categorias_racacor[j:j+2]):
                df_cat = df_racacor[df_racacor["Raça/cor"] == cat]
                with row_cols[k]:
                    plot_corr_heatmap(df_cat, f"Raça/Cor: {cat}")
    except Exception as e:
        st.error(f"Erro ao gerar correlação por Raça/Cor: {e}")


# REFERÊNCIAS

with abas[7]:
    st.subheader("Referências")
    st.markdown("""
                <div style="text-align: justify;">
                
•	WORLD HEALTH ORGANIZATION (WHO). Suicide worldwide in 2019: global health estimates. Geneva: WHO, 2019. Disponível em: https://www.who.int/publications/i/item/9789240026643. Acesso em: 02 out. 2025. 
                
•	SOARES, F. C. et al. Trends in Taxa de suicídio in Brazil from 2011 to 2020: special focus on the COVID-19 pandemic. Revista Panamericana de Salud Pública / Pan American Journal of Public Health, 2022. Disponível em: https://pubmed.ncbi.nlm.nih.gov/36569581/. Acesso em: 02 out. 2025 
                
•	MACHADO, D. B.; RASELLA, D.; DOS SANTOS, D. N. Impact of income inequality and other social determinants on suicide rate in Brazil. PLOS ONE, v.10, n.4, e0124934, 2015. DOI: https://doi.org/10.1371/journal.pone.0124934. Disponível em: https://pmc.ncbi.nlm.nih.gov/articles/PMC4416030/. Acesso em: 02 out. 2025. 
                
•	DATASUS — Ministério da Saúde. Informações de Saúde (TABNET): SINAN, SIH, SIM. Disponível em: https://datasus.saude.gov.br/informacoes-de-saude-tabnet/. Acesso em: 02 out. 2025. 
                
•	VOLPE, F. M.; LACERDA, D. R. N. Reanalyzing self-harm notifications trends in Brazil, 2011–2022. The Lancet Regiãoal Health – Americas (comentário/reanálise), 2024. Disponível em: https://pmc.ncbi.nlm.nih.gov/articles/PMC11192789/. Acesso em: 02 out. 2025. 
                
•	OUR WORLD IN DATA. Suicides — dados agregados e análises globais (página com dados e visualizações). Disponível em: https://ourworldindata.org/suicide. Acesso em: 02 out. 2025.
                
•	PYTHON SOFTWARE FOUNDATION. Python: a programming language. Versão 3.12. Disponível em: https://www.python.org/. Acesso em: 03 out. 2025
                
•	MICROSOFT CORPORATION. Visual Studio Code. 2025. Disponível em: https://code.visualstudio.com/. Acesso em: 03 out. 2025.

•   ALVES, Flávia José Oliveira et al. The rising trends of self-harm in Brazil: an ecological analysis of notifications, hospitalisations, and mortality between 2011 and 2022. The Lancet Regiãoal Health – Americas, v. 31, p. 100691, 2024. DOI: 10.1016/j.lana.2024.100691 

•   MICROSOFT. Visual Studio Code Documentation. Disponível em: https://code.visualstudio.com/docs. Acesso em: 9 out. 2025.

•   SERRAPILHEIRA. Guia de Ciência Aberta e Reprodutível. Rio de Janeiro: Instituto Serrapilheira, 2021. Disponível em: https://serrapilheira.org/wp-content/uploads/2019/11/serrapilheira-guia-ciencia-aberta-e-reprodutivel.pdf. Acesso em: 9 out. 2025.

•   SILVA, A. Análise exploratória de dados em saúde pública com Python: práticas e aplicações. São Paulo: FAPESP, 2022.

•   STREAMLIT INC. Streamlit Documentation. 2023. Disponível em: https://docs.streamlit.io . Acesso em: 9 out. 2025.

•   VAN ROSSUM, G.; DRAKE, F. L. Python 3 Reference Manual. Scotts Valley: CreateSpace, 2022.
</div>
                """, unsafe_allow_html=True)