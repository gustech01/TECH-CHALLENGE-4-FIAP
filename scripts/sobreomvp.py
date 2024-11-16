import streamlit as st
import pandas as pd
import plotly.express as px

def show():
 left, cent, right = st.columns(3)
 with right:
   st.image('imagens/fiap.png')
   
    dados = pd.read_csv("dataset/Europe_Brent_Spot_Price_FOB.csv")
    dados = dados[dados['Date'] >= '01-01-2000']
    forecast = pd.read_csv("dataset/xgboost_results.csv")

    # Tipando coluna de data
    dados['Date'] = pd.to_datetime(dados['Date'])

    # Configurando template do plotly
    template = 'ggplot2'

    # Figuras

    # Série histórica
    fig = px.line(
        data_frame=dados, 
        x=dados.Date,
        y=dados.Value,
        template=template,
        color_discrete_sequence=['#ef5350'],
        labels={
            'Value': 'Preço (US$)',
            'data': 'Data'
        }
    )
    fig.update_layout(
        title='Preço do Petróleo Brent (US$)',
        xaxis_title='Período',
        yaxis_title='Preço (US$)'
    )

    # Série prevista
    fig_previsao = px.line(
        data_frame=forecast, 
        x=forecast.Date,
        y=forecast.Predicted,
        template=template,
        color_discrete_sequence=['#ef5350'],
        labels={
            'preco_previsto': 'Preço previsto (US$)',
            'data': 'Data'
        }
    )
    fig_previsao.update_layout(
        title='Preço Previsto do Petróleo Brent (US$)',
        xaxis_title='Período',
        yaxis_title='Preço Previsto (US$)'
    )

    # Visualização no Streamlit

    # Logo FIAP
    left, cent, right = st.columns(3)
    with right:
        # st.image('img/fiap.png')
        pass

    # Título
    st.title('Petróleo Brent')
   ,
            unsafe_allow_html=True
        )
