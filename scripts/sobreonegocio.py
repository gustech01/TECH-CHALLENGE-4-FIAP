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
        </div>
        ''',
        unsafe_allow_html=True
    )



