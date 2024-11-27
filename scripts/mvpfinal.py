import streamlit as st
import pandas as pd
from pathlib import Path

@st.cache_data(show_spinner=True)
def carregar_dados(caminho):
    """Carrega um dataset CSV, retorna o DataFrame ou erro."""
    try:
        return pd.read_csv(caminho)
    except FileNotFoundError:
        st.error(f"Arquivo não encontrado: {caminho}")
        return pd.DataFrame()

@st.cache_resource(show_spinner=True)
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
        dados = dados[dados['Date'].between('2000-01-01', '2025-12-31')]
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

    # Substituir valores NaN por interpolação para evitar problemas no gráfico
    dados_comb = dados_comb.interpolate(method='linear')

    with tab1:
        # Filtro de datas dinâmico
        if not dados_comb.empty:
            st.subheader("Histórico x Forecast de Preços do Petróleo")

            # Obter o intervalo de datas disponível
            min_date = dados_comb.index.min().date()
            max_date = dados_comb.index.max().date()

            # Slider para selecionar o intervalo de datas
            date_range = st.slider(
                "Selecione o período:",
                min_value=min_date,
                max_value=max_date,
                value=(min_date, max_date)
                
            )

            # Filtrar os dados com base no intervalo selecionado
            dados_filtrados = dados_comb.loc[date_range[0]:date_range[1]]

            # Exibir o gráfico filtrado
            st.line_chart(dados_filtrados, use_container_width=True)
            # Texto explicativo
            st.markdown("""
            ### Eventos Relevantes:
            - **2008**: Crise financeira global provocada pelo colapso do mercado imobiliário dos EUA, afetando fortemente o consumo e os preços do petróleo.
            - **2014**: Queda dos preços devido à superprodução nos EUA e desaceleração da demanda na Europa e Ásia.
            - **2020**: Redução drástica no consumo devido à pandemia de COVID-19, gerando desequilíbrios significativos entre oferta e demanda.
            - **2022**: Invasão da Ucrânia pela Rússia, que resultou em sanções econômicas severas à Rússia e causou um aumento abrupto no preço do petróleo Brent, ultrapassando US$ 120 o barril em março.
            """)
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
