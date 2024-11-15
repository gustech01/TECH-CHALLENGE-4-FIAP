import streamlit as st
from scripts import home
from scripts import sobreoprojeto
from scripts import sobreonegocio

# Função principal
def main():
    st.set_page_config(page_title="Navegação com Streamlit", layout="wide")

    # Título do aplicativo
    st.title("Aplicação Streamlit")
    
    # Menu lateral
    menu = st.sidebar.radio(
        "Menu de Navegação",
        options=["Home", "Sobre o Negócio", "Sobre o Projeto"]
    )
    
    # Direcionamento para páginas
    if menu == "Home":
        st.subheader("Bem-vindo à Home!")
        st.info("Você está visualizando a página inicial.")
        sobreoprojeto()  # Mostrando "Sobre o Projeto" na Home como padrão
    elif menu == "Sobre o Negócio":
        sobreonegocio()
    elif menu == "Sobre o Projeto":
        sobreoprojeto()
    

# Rodar a aplicação
if __name__ == "__main__":
    main()