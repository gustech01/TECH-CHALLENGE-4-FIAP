import streamlit as st

# Menu lateral
st.sidebar.title("Menu")
menu = st.sidebar.radio("Selecione uma página:", ["Home", "Sobre o Negócio", "Sobre o Projeto"])

# Exibição das páginas
if menu == "Home":
    import home
    home.show()

elif menu == "Sobre o Negócio":
    import sobreonegocio
    sobreonegocio.show()

elif menu == "Sobre o Projeto":
    import sobreoprojeto
    sobreoprojeto.show()

@st.cache
def get_data():
    return {"key": "dados carregados"}  # Simulando carregamento de dados

# Apenas chamar a função em cada página
data = get_data()
st.write(data)

