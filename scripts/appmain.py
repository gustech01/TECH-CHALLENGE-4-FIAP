# Certifique-se de que `sobreoprojeto.py`, `home.py`, e `sobreonegocio.py` estão no mesmo diretório
import streamlit as st
from sobreoprojeto home sobreonegocio import scripts

# Menu lateral com a página "Home" selecionada como padrão
st.sidebar.title("Menu")
menu = st.sidebar.radio(
    "Selecione uma página:", 
    ["Home", "Sobre o Negócio", "Sobre o Projeto"], 
    index=0  # Define "Home" como padrão (índice 0)
)

# Exibição das páginas
if menu == "Home":
    home.show()

elif menu == "Sobre o Negócio":
    sobreonegocio.show()

elif menu == "Sobre o Projeto":
    sobreoprojeto.show()
