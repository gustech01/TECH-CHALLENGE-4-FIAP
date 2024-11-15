import streamlit as st

def show():
 left, cent, right = st.columns(3)
 with right:
   st.image('imagens/fiap.png')
  
st.title('Sobre o Negócio')
st.markdown(
    '''
        <div style="text-align: justify;">
    <p>
        A cotação do petróleo, medida em dólares por barril, é definida pela oferta e demanda internacional da commodity. 
        As duas principais referências comerciais são o Brent e o West Texas Intermediate (WTI). O Brent é extraído no Mar 
        do Norte e negociado na Bolsa de Londres, enquanto o WTI vem dos Estados Unidos e, historicamente, possui um valor 
        inferior devido ao excesso de oferta no mercado americano.
    </p>
    <p>
        O petróleo é classificado pela densidade e teor de enxofre: leve e doce (com menor teor de enxofre) são os tipos 
        mais valorizados, pois demandam menos processamento. Tanto o Brent quanto o WTI são leves e doces, sendo o Brent 
        amplamente utilizado como referência de preços, pois sua extração no mar reduz os custos logísticos.
    </p>
    <p>
        A negociação do petróleo ocorre em mercados à vista e futuros. No mercado futuro, contratos de "barris de papel" 
        são transacionados para especulação ou proteção contra volatilidade de preços, sem que haja troca física do produto. 
        Fatores como o valor do dólar, políticas da OPEC, níveis de produção e estoque, além do estado da economia global, 
        impactam os preços do petróleo.
    </p>
    <p>
        Soluções de Inteligência Artificial, como as propostas neste projeto, contribuem com previsões de curto prazo, 
        auxiliando na tomada de decisão dos investidores.
    </p>
</div>''',
    unsafe_allow_html=True
)
