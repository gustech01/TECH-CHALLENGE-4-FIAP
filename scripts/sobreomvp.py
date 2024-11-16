import streamlit as st
import pandas as pd
import plotly.express as px

def show():
    # Layout inicial com imagem
    left, cent, right = st.columns(3)
    with right:
        st.image('imagens/fiap.png')

    # Leitura dos dados
    dados = pd.read_csv("dataset/Europe_Brent_Spot_Price_FOB.csv")
    forecast = pd.read_csv("dataset/xgboost_results.csv")

    # Tipando coluna de data e filtrando dados
    dados['Date'] = pd.to_datetime(dados['Date'], format='%Y-%m-%d', errors='coerce')
    dados = dados[dados['Date'] >= '2000-01-01']

    forecast['Date'] = pd.to_datetime(forecast['Date'], format='%Y-%m-%d', errors='coerce')

    # Configurando template do Plotly
    template = 'ggplot2'

    # Criando figuras
    # Série histórica
    fig = px.line(
        data_frame=dados,
        x='Date',
        y='Value',
        template=template,
        color_discrete_sequence=['#ef5350'],
        labels={
            'Value': 'Preço (US$)',
            'Date': 'Data'
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
        x='Date',
        y='Predicted',
        template=template,
        color_discrete_sequence=['#ef5350'],
        labels={
            'Predicted': 'Preço previsto (US$)',
            'Date': 'Data'
        }
    )
    fig_previsao.update_layout(
        title='Preço Previsto do Petróleo Brent (US$)',
        xaxis_title='Período',
        yaxis_title='Preço Previsto (US$)'
    )

    # Visualização no Streamlit
    st.title('Petróleo Brent')

    # Layout do aplicativo com abas
    tab1, tab2 = st.tabs(['Forecast', 'Histórico'])

    with tab1:
        # Série prevista
        st.plotly_chart(fig_previsao, use_container_width=True)
        st.markdown(
            'O gráfico acima mostra o forecast para as próximas 5 cotações do barril de petróleo Brent '
            'gerado com o modelo AutoARIMA implementado.'
        )

    with tab2:
        # Série histórica
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(
            '''
            <div style='text-align: justify;'>
                <p>
                    O gráfico acima ilustra a série histórica do preço do barril de petróleo Brent desde os anos 2000. 
                    Verifica-se três grandes oscilações negativas na série, com inícios em 2008, 2014 e 2020.
                </p>
                <ul>
                    <li>
                        <strong>2008:</strong> A chamada terceira crise do petróleo está relacionada à especulação imobiliária nos Estados Unidos...
                    </li>
                    <li>
                        <strong>2014:</strong> É o pior tombo de preços desde 2008, causada pelo aumento de produção...
                    </li>
                    <li>
                        <strong>2020:</strong> O setor petrolífero viveu um momento de instabilidade em razão da pandemia do novo coronavírus...
                    </li>
                </ul>
            </div>
            ''',
            unsafe_allow_html=True
        )
