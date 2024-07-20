import streamlit as st  # Biblioteca para construir os dashboards
import pandas as pd  # Biblioteca para manipulação de dados, ler os arquivos
import plotly.express as px  # Biblioteca para construir os gráficos

st.set_page_config(layout='wide')

df = pd.read_csv("C:/Repositorios_GitHube/MeusProjetos/DASH_PYTHON/ICCP.csv", encoding='ISO-8859-1')
df['data_fato'] = pd.to_datetime(df['data_fato'])  # Converte a data para o tipo datetime64[ns]
df = df.sort_values('data_fato')

df["month"] = df['data_fato'].apply(lambda x: str(x.year) + "-" + str(x.month))

# Adiciona seletores de múltiplos itens no sidebar
selected_months = st.sidebar.multiselect("Mês", df['month'].unique(), default=df['month'].unique())
selected_cia_pm = st.sidebar.multiselect("CIA PM", df['cia_pm'].unique(), default=df['cia_pm'].unique())
selected_pelotao = st.sidebar.multiselect("PELOTÃO", df['pelotao'].unique(), default=df['pelotao'].unique())
selected_municipio = st.sidebar.multiselect("MUNICÍPIO", df['nome_municipio'].unique(), default=df['nome_municipio'].unique())

# Filtra os dados com base nas seleções
df_filtred = df[
    (df['month'].isin(selected_months)) &
    (df['cia_pm'].isin(selected_cia_pm)) &
    (df['pelotao'].isin(selected_pelotao)) &
    (df['nome_municipio'].isin(selected_municipio))
]

# Exibe os dados filtrados
st.dataframe(df_filtred)

# Cria um gráfico de exemplo usando os dados filtrados (substitua pelas suas colunas reais)
fig = px.bar(df_filtred, x='data_fato', y='furto', title='Título do Gráfico', color='cia_pm',)
st.plotly_chart(fig)

# Cria uma nova coluna que seja a soma das colunas 'furto', 'roubo' e 'extorsao'
df_filtred['total_crimes'] = df_filtred[['furto', 'roubo', 'extorsao']].sum(axis=1)

# Agrupa os dados por 'cia_pm' e calcula a soma de 'total_crimes'
df_grouped = df_filtred.groupby('cia_pm')['total_crimes'].sum().reset_index()

# Cria um gráfico de barras com base nos dados agrupados e adiciona rótulos
fig = px.bar(df_filtred, x='cia_pm', y='natureza_ocorrencia_descricao_longa', title='Soma de Crimes por CIA PM', color='natureza_ocorrencia_descricao_longa', text='total_crimes')

# Atualiza o layout do gráfico para mostrar os rótulos
fig.update_traces(texttemplate='%{text:.0s}', textposition='outside')

# Exibe o gráfico no Streamlit
st.plotly_chart(fig)

col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)

col1.plotly_chart(fig)