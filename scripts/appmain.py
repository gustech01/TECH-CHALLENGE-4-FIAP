  # Certifique-se de que `sobreoprojeto.py` está no mesmo diretório
import home
import sobreonegocio
import sobreoprojeto
import streamlit as st

# Menu lateral
st.sidebar.title("Menu")
menu = st.sidebar.radio("Selecione uma página:", ["Home", "Sobre o Negócio", "Sobre o Projeto"])

# Exibição das páginas
if menu == "Home":
    home.show()

elif menu == "Sobre o Negócio":
    sobreonegocio.show()

elif menu == "Sobre o Projeto":
    sobreoprojeto.show()
