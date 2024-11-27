import streamlit as st
import pandas as pd
import plotly.graph_objects as go
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
    tab1, tab2 = st.tabs(['Realizado x Forecast', 'Dados Brutos'])

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
            st.subheader("Realizado x Forecast")

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

            # Criar o gráfico com Plotly
            fig = go.Figure()

            # Linha de valores reais
            fig.add_trace(go.Scatter(
                x=dados_filtrados.index,
                y=dados_filtrados['Value_Realizado'],
                mode='lines',
                name='Realizado',
                line=dict(color='blue', width=2)
            ))

            # Linha de valores previstos
            fig.add_trace(go.Scatter(
                x=dados_filtrados.index,
                y=dados_filtrados['Predicted'],
                mode='lines',
                name='Forecast',
                line=dict(color='orange', width=2)
            ))

            # Área do delta
            fig.add_trace(go.Scatter(
                x=dados_filtrados.index.tolist() + dados_filtrados.index[::-1].tolist(),
                y=dados_filtrados['Value_Realizado'].tolist() + dados_filtrados['Predicted'][::-1].tolist(),
                fill='toself',
                fillcolor='rgba(255, 165, 0, 0.2)',  # Cor laranja transparente
                line=dict(color='rgba(255,255,255,0)'),
                hoverinfo="skip",
                showlegend=False
            ))

            # Configurar layout do gráfico
            fig.update_layout(
                title="Realizado x Forecast com Delta",
                xaxis_title="Data",
                yaxis_title="Valores",
                legend_title="Legenda",
                template="plotly_white",
                height=600
            )

            # Exibir o gráfico
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.error("Os dados combinados estão vazios após o processamento.")

    with tab2:
        # Exibindo os dados brutos
        st.subheader("Dados Brutos")
        st.dataframe(dados)

        st.subheader("Dados de Previsões")
        st.dataframe(forecast)

# Exibir o aplicativo
if __name__ == "__main__":
    show()
