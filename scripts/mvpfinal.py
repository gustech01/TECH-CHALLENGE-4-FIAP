import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
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
    tab1, tab2 = st.tabs(['Histórico x Forecast', 'Dados Brutos'])

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

    # Combinando dados históricos e forecast em um único DataFrame
    dados_comb = pd.merge(dados, forecast, on='Date', how='outer', suffixes=('_Realizado', '_Forecast'))
    dados_comb = dados_comb.set_index('Date').sort_index()

    with tab1:
        # Gráfico personalizado usando matplotlib
        if not dados_comb.empty:
            st.subheader("Histórico x Forecast de Preços do Petróleo")

            # Criando o gráfico com matplotlib
            plt.figure(figsize=(12, 6))
            plt.plot(
                dados_comb.index, 
                dados_comb['Value'], 
                label="Realizado", 
                color='blue', 
                linewidth=2, 
                alpha=0.8
            )
            plt.plot(
                dados_comb.index, 
                dados_comb['Predicted'], 
                label="Forecast", 
                color='orange', 
                linewidth=2, 
                alpha=0.8
            )
            plt.title("Preços do Petróleo: Histórico vs Forecast", fontsize=16, weight='bold')
            plt.xlabel("Ano", fontsize=12)
            plt.ylabel("Preço (USD)", fontsize=12)
            plt.legend(loc='upper left', fontsize=12)
            plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)
            plt.tight_layout()

            # Exibindo o gráfico no Streamlit
            st.pyplot(plt)
        else:
            st.error("Os dados combinados estão vazios após o processamento.")

    with tab2:
        # Exibindo os dados brutos
        st.subheader("Dados Históricos")
        st.dataframe(dados)

        st.subheader("Dados de Previsões")
        st.dataframe(forecast)

# Exibir o aplicativo
if __name__ == "__main__":
    show()
