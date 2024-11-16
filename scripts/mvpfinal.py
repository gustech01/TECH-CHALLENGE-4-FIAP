import streamlit as st
import pandas as pd

# Layout com colunas
left, cent, right = st.columns(3)
with right:
    st.image('imagens/fiap.png')  # Certifique-se de que o caminho para a imagem está correto

# Leitura dos dados
dados = pd.read_csv("dataset/Europe_Brent_Spot_Price_FOB.csv")
forecast = pd.read_csv("dataset/xgboost_results.csv")

# Tipando coluna de data e filtrando dados
dados['Date'] = pd.to_datetime(dados['Date'], format='%Y-%m-%d', errors='coerce')
dados = dados[dados['Date'] >= '2000-01-01']

# Tratando as previsões
forecast['Date'] = pd.to_datetime(forecast['Date'], format='%Y-%m-%d', errors='coerce')

# Layout principal
st.title("Análise de Preços do Petróleo e Previsões")
st.write("Este dashboard mostra o histórico de preços do petróleo Brent e as previsões baseadas em modelos.")

# Gráfico 1: Histórico do petróleo
st.subheader("Histórico de Preços do Petróleo")
st.line_chart(dados.rename(columns={"Date": "index"}).set_index("index")["Price"], 
              use_container_width=True)

# Gráfico 2: Previsões
st.subheader("Previsões de Preço")
st.line_chart(forecast.rename(columns={"Date": "index"}).set_index("index")["Forecast"], 
              use_container_width=True)

    
        
  


