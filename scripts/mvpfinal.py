import streamlit as st
import pandas as pd

# Layout com colunas
left, cent, right = st.columns(3)
with right:
    st.image('imagens/fiap.png')  # Certifique-se de que o caminho para a imagem está correto

# Leitura dos dados
dados = pd.read_csv("dataset/Europe_Brent_Spot_Price_FOB.csv")
forecast = pd.read_csv("dataset/xgboost_results.csv")

# Exibindo as primeiras linhas para verificar os dados
st.write("### Visualização do Dataset Histórico")
st.write(dados.head())  # Inspecione os nomes das colunas aqui

# Tipando coluna de data e filtrando dados
dados['Date'] = pd.to_datetime(dados['Date'], format='%Y-%m-%d', errors='coerce')
dados = dados[dados['Date'] >= '2000-01-01']

# Tratando as previsões
forecast['Date'] = pd.to_datetime(forecast['Date'], format='%Y-%m-%d', errors='coerce')

# Verificando colunas do dataset de previsões
st.write("### Visualização do Dataset de Previsões")
st.write(forecast.head())  # Inspecione os nomes das colunas aqui

# Gráfico 1: Histórico do petróleo
if 'Date' in dados.columns:
    st.subheader("Histórico de Preços do Petróleo")
    st.line_chart(dados.rename(columns={"Date": "index"}).set_index("index")["Value"], 
                  use_container_width=True)
else:
    st.error("A coluna 'Price' não foi encontrada no dataset histórico.")

# Gráfico 2: Previsões
if 'Predicted' in forecast.columns:
    st.subheader("Previsões de Preço")
    st.line_chart(forecast.rename(columns={"Date": "index"}).set_index("index")["Predicted"], 
                  use_container_width=True)
else:
    st.error("A coluna 'Forecast' não foi encontrada no dataset de previsões.")
