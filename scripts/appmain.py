import sobreoprojeto  # Certifique-se de que `sobreoprojeto.py` está no mesmo diretório
import sobreonegocio
import home
import streamlit as st

# Menu lateral
st.sidebar.title("Menu")
menu = st.sidebar.radio("Selecione uma página:", ["Home", "Sobre o Negócio", "Sobre o Projeto"])

# Exibição das páginas
if menu == "Home":
    try:
        home.show()
    except AttributeError:
        st.error("Erro ao carregar a página 'Home'. Verifique se a função `show()` está definida no arquivo `home.py`.")

elif menu == "Sobre o Negócio":
    try:
        sobreonegocio.show()
    except AttributeError:
        st.error("Erro ao carregar a página 'Sobre o Negócio'. Verifique se a função `show()` está definida no arquivo `sobreonegocio.py`.")




elif menu == "Sobre o Projeto":
    try:
        sobreoprojeto.show()
    except AttributeError:
        st.error("Erro ao carregar a página 'Sobre o Projeto'. Verifique se a função `show()` está definida no arquivo `sobreoprojeto.py`.")


   






