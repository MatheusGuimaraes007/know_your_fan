import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

# Conecta ao banco de dados
conn = sqlite3.connect("data/users.db")

st.set_page_config(layout="centered")
st.title("📊 Painel de Administração – Fãs da FURIA")

# Lê os dados da tabela
df = pd.read_sql_query("SELECT * FROM fans_data", conn)

# Remove colunas sensíveis para exibição
df_publico = df.drop(columns=["nome", "endereco", "cpf", "instagram_username", "data_envio"])

# Contador total
st.metric("👥 Total de Fãs Cadastrados", len(df))

# Métricas adicionais
doc_validos = int(df["doc_validado"].fillna(False).sum())
doc_invalidos = int(len(df) - doc_validos)

# Gráfico de validação de documentos
if doc_validos + doc_invalidos > 0:
    st.subheader("📄 Validação de Documentos")
    fig1, ax1 = plt.subplots()
    ax1.pie(
        [doc_validos, doc_invalidos],
        labels=["Validados", "Não Validados"],
        autopct="%1.1f%%",
        startangle=90,
        colors=["#66bb6a", "#ef5350"]
    )
    ax1.axis("equal")
    st.pyplot(fig1)
else:
    st.warning("Nenhum dado disponível para gerar o gráfico de validação.")

# Interesses mais comuns
st.subheader("🎮 Interesses mais escolhidos pelos fãs")
interesses_series = df["interesses"].dropna().str.split(", ")
interesses_explodidos = interesses_series.explode().str.strip()
top_interesses = interesses_explodidos.value_counts().head(10)
fig2, ax2 = plt.subplots()
top_interesses.plot(kind="barh", ax=ax2, color="#42a5f5")
ax2.set_xlabel("Quantidade")
ax2.invert_yaxis()
st.pyplot(fig2)

# Atrações mais populares
top_atracoes = df["atracoes_furia"].dropna().str.split(", ").explode().str.strip().value_counts()
st.subheader("🔥 O que mais atrai os fãs na FURIA")
fig3, ax3 = plt.subplots()
top_atracoes.plot(kind="pie", autopct="%1.1f%%", startangle=90, ax=ax3)
ax3.set_ylabel("")
st.pyplot(fig3)

# Experiências desejadas
st.subheader("⭐ Experiência mais desejada pelos fãs")
top_exp = df["experiencia_desejada"].value_counts()
fig4, ax4 = plt.subplots()
sns.countplot(y="experiencia_desejada", data=df, order=top_exp.index, palette="magma", ax=ax4)
ax4.set_xlabel("Quantidade")
ax4.set_ylabel("")
st.pyplot(fig4)

# Produtos consumidos
st.subheader("🛍️ Produtos e serviços de e-sports consumidos")
prod_series = df["produtos_consumo"].dropna().str.split(", ")
prod_exploded = prod_series.explode().str.strip()
fig5, ax5 = plt.subplots()
prod_exploded.value_counts().head(10).plot(kind="barh", ax=ax5, color="#ab47bc")
ax5.set_xlabel("Quantidade")
ax5.invert_yaxis()
st.pyplot(fig5)

# Funcionalidades desejadas na plataforma
st.subheader("🌐 Funcionalidades desejadas na plataforma de membros")
plat_series = df["plataforma_membros"].dropna().str.split(", ")
plat_exploded = plat_series.explode().str.strip()
fig6, ax6 = plt.subplots()
plat_exploded.value_counts().plot(kind="bar", ax=ax6, color="#29b6f6")
ax6.set_ylabel("Quantidade")
ax6.set_xticklabels(ax6.get_xticklabels(), rotation=45, ha="right")
st.pyplot(fig6)

# Mostrar a tabela dos cadastros sem dados sensíveis
st.subheader("📋 Cadastros (dados públicos de análise)")
st.dataframe(df_publico)
