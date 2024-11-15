# Certifique-se de que `sobreoprojeto.py`, `home.py`, e `sobreonegocio.py` estão no mesmo diretório
import streamlit as st
from streamlit_option_menu import option_menu
import home
import sobreonegocio
import sobreoprojeto


with st.sidebar:

    selected = option_menu(
        menu_title = "Menu",
        options=["Home","Sobre o Negócio", "Sobre o Projeto"],
    )


if selected == "Home":
   st.title(f"{selected}")

if selected == "Sobre o Negócio":
   st.title(f"{selected}")

if selected == "Sobre o Projeto":
   st.title(f"{selected}")


