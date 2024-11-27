novo 22:43


import streamlit as st
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

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

            # Plotando as duas linhas
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(dados_filtrados.index, dados_filtrados['Value_Realizado'], label='Realizado', color='blue')
            ax.plot(dados_filtrados.index, dados_filtrados['Predicted_Forecast'], label='α (Forecast)', color='red')

            # Personalizando legendas
            ax.legend()

            # Exibir o gráfico
            st.pyplot(fig)

            # Texto explicativo
            st.markdown("""
            ### Eventos Históricos:
            - **2008**: Crise financeira global provocada pelo colapso do mercado imobiliário dos EUA, afetando fortemente o consumo e os preços do petróleo.
            - **2014**: Queda dos preços devido à superprodução nos EUA e desaceleração da demanda na Europa e Ásia.
            - **2020**: Redução drástica no consumo devido à pandemia de COVID-19, gerando desequilíbrios significativos entre oferta e demanda.
            - **2022**: Invasão da Ucrânia pela Rússia, que resultou em sanções econômicas severas à Rússia e causou um aumento abrupto no preço do petróleo Brent, ultrapassando US$ 120 o barril em março.
            """)

            # Texto explicativo sobre o modelo XGBoost
            st.write("""
            ### Informações do Modelo Xboost:
            O modelo utilizou 1000 iterações com um early stop de 50 (para evitar overfitting, caso o valor de erro das iterações subsequentes parasse de cair). O modelo XGBoost apresentou um resultado bem satisfatório, capturando bem a alteração de tendências e sazonalidade dos dados, gerando um MAPE de 1.48%.
            
            O **MAPE** (Mean Absolute Percentage Error, ou Erro Percentual Absoluto Médio) é uma métrica amplamente utilizada para avaliar a precisão de modelos preditivos.  
            Ele mede a porcentagem média de erro entre os valores reais e os valores previstos, fornecendo uma indicação clara do desempenho do modelo em termos percentuais.
            """)

            # Fórmula do MAPE
            st.write("""
            ### Fórmula do MAPE:
            """)

            # Exibindo a fórmula
            left, cent, right = st.columns(3)
            with cent:
                imagem_2 = carregar_imagem('imagens/formula_black_background.png')
                if imagem_2:
                    st.image(imagem_2)

            # Continuação do texto explicativo
            st.write("""
            ### Componentes da Fórmula:
            - **n**: Total de observações.  
            - **yᵢ**: Valor real da i-ésima observação.  
            - **ŷᵢ**: Valor previsto para a i-ésima observação.  
            - O resultado final é multiplicado por 100 para ser expresso em percentual.
            
            ### Importância do MAPE:
            O MAPE é fácil de interpretar e fornece uma métrica clara e intuitiva. No entanto, é importante lembrar que o MAPE pode ser sensível a valores reais muito próximos de zero, o que pode distorcer os resultados.
            No contexto de modelos como o XGBoost, ele é frequentemente usado como métrica de avaliação para otimizar o desempenho preditivo.
            """)
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
