import streamlit as st
import pandas as pd

def show():
    # Visualização no Streamlit

    # Logo FIAP
    left, cent, right = st.columns(3)
    with right:
        st.image('imagens/fiap.png')

    # Título
    st.title('MVP Petróleo Brent')

    # Layout do aplicativo
    tab1, tab2 = st.tabs(['Histórico', 'Forecast'])

    # Leitura dos dados
    try:
        dados = pd.read_csv("dataset/Europe_Brent_Spot_Price_FOB.csv")
        forecast = pd.read_csv("dataset/xgboost_results.csv")
    except FileNotFoundError:
        st.error("Os arquivos de dataset não foram encontrados. Verifique os caminhos.")
        return

    # Exibindo as primeiras linhas para verificar os dados
    #st.write("### Dados Carregados")
   # st.write(dados.head())
    #st.write(forecast.head())

    # Tratando dados históricos
    dados['Date'] = pd.to_datetime(dados['Date'], errors='coerce')
    dados = dados[dados['Date'] >= '2000-01-01']

    if dados.empty:
        st.error("O dataset de histórico de preços está vazio após o filtro.")
        return

    # Tratando dados de previsões
    forecast['Date'] = pd.to_datetime(forecast['Date'], format='%Y-%m-%d', errors='coerce')

    with tab1:
        # Gráfico 1: Histórico do petróleo
        if 'Value' in dados.columns:
            st.subheader("Histórico de Preços do Petróleo")
            st.line_chart(dados.set_index("Date")["Value"], use_container_width=True)
        else:
            st.error("A coluna 'Value' não foi encontrada no dataset histórico.")

    with tab2:
        # Gráfico 2: Previsões
        if 'Predicted' in forecast.columns:
            st.subheader("Previsões de Preço")
            st.line_chart(forecast.set_index("Date")["Predicted"], use_container_width=True)
        else:
            st.error("A coluna 'Predicted' não foi encontrada no dataset de previsões.")

# Exibir o aplicativo
#if __name__ == "__main__":
 #   show()
