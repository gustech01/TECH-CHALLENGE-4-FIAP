import streamlit as st
import pandas as pd
##import plotly.graph_objects as go  # Usando plotly.graph_objects

def show():
   
    # Leitura dos dados
    dados = pd.read_csv("dataset/Europe_Brent_Spot_Price_FOB.csv")
    forecast = pd.read_csv("dataset/xgboost_results.csv")
    
    # Tipando coluna de data e filtrando dados
    dados['Date'] = pd.to_datetime(dados['Date'], format='%Y-%m-%d', errors='coerce')
    dados = dados[dados['Date'] >= '2000-01-01']

    forecast['Date'] = pd.to_datetime(forecast['Date'], format='%Y-%m-%d', errors='coerce')

    # Criando o gráfico de série histórica usando plotly.graph_objects
    print(forecast)
    print(dados)

    
        
  


