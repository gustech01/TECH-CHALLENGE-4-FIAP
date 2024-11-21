import streamlit as st
import pandas as pd
from pathlib import Path

@st.cache_data
def carregar_dados(caminho):
    """Carrega um dataset CSV, retorna o DataFrame ou erro."""
    try:
        return pd.read_csv(caminho)
    except FileNotFoundError:
        st.error(f"Arquivo não encontrado: {caminho}")
        return pd.DataFrame()

@st.cache_resource
def carregar_imagem(caminho):
    """Carrega o caminho da imagem."""
    imagem_path = Path(caminho)
    if imagem_path.is_file():
        return str(imagem_path)
    else:
        st.error(f"Imagem não encontrada: {caminho}")
        return None

def show():
    # Logo FIAP
    left, cent, right = st.columns(3)
    with right:
        imagem = carregar_imagem('imagens/fiap.png')
        if imagem:
            st.image(imagem)

    # Título
    st.title('MVP Petróleo Brent')

    # Layout do aplicativo
    tab1, tab2 = st.tabs(['Histórico', 'Forecast'])

    # Leitura dos dados
    dados = carregar_dados("dataset/Europe_Brent_Spot_Price_FOB.csv")
    forecast = carregar_dados("dataset/xgboost_results.csv")

    if dados.empty or forecast.empty:
        st.error("Os arquivos de dataset não foram carregados corretamente.")
        return

    # Tratando dados históricos
    if 'Date' in dados.columns and 'Value' in dados.columns:
        dados['Date'] = pd.to_datetime(dados['Date'], errors='coerce')
        dados = dados[dados['Date'] >= '2000-01-01']
    else:
        st.error("Colunas 'Date' ou 'Value' ausentes no dataset histórico.")
        return

    # Tratando dados de previsões
    if 'Date' in forecast.columns and 'Predicted' in forecast.columns:
        forecast['Date'] = pd.to_datetime(forecast['Date'], errors='coerce')
    else:
        st.error("Colunas 'Date' ou 'Predicted' ausentes no dataset de previsões.")
        return

    with tab1:
        # Gráfico 1: Histórico do petróleo
        if not dados.empty:
            st.subheader("Histórico de Preços do Petróleo")
            st.line_chart(dados.set_index("Date")["Value"], use_container_width=True)
        else:
            st.error("Dados de histórico do petróleo estão vazios após o filtro.")

    with tab2:
        # Gráfico 2: Previsões
        if not forecast.empty:
            st.subheader("Previsões de Preço")
            st.line_chart(forecast.set_index("Date")["Predicted"], use_container_width=True)
        else:
            st.error("Dados de previsões estão vazios após o processamento.")

# Exibir o aplicativo
if __name__ == "__main__":
    show()
