# Certifique-se de que `sobreoprojeto.py`, `home.py`, e `sobreonegocio.py` estão no mesmo diretório
import streamlit as st
import home
import sobreonegocio
import sobreoprojeto


# Menu lateral
st.sidebar.title("Menu")
menu = st.sidebar.radio("Selecione uma página:", ["Home", "Sobre o Negócio", "Sobre o Projeto"])

# Exibição das páginas
if menu == "Home":
    sobreoprojeto.show()

elif menu == "Sobre o Negócio":
    sobreoprojeto.show()

elif menu == "Sobre o Projeto":
    sobreoprojeto.show()



