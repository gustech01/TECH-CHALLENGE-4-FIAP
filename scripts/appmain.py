import streamlit as st


# Inicialize variáveis no session_state
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

# Menu lateral
st.sidebar.title("Menu")
menu = st.sidebar.radio("Selecione uma página:", ["Home", "Sobre o Negócio", "Sobre o Projeto","MVP"])

# Atualize o estado da página atual
st.session_state.current_page = menu

# Exibição das páginas
if st.session_state.current_page == "Home":
    import home
    home.show()

elif st.session_state.current_page == "Sobre o Negócio":
    import sobreonegocio
    sobreonegocio.show()

elif st.session_state.current_page == "Sobre o Projeto":
    import sobreoprojeto
    sobreoprojeto.show()


