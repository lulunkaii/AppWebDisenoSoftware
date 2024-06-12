import pickle
from pathlib import Path

import auth
import utils
import streamlit as st
import requests
import re
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie

#To-do 
    #Incluir posibles códigos de salida (error o success) 201, 400 y 409  para registro y login de usuario
    #Junto a esto, un recurso gráfico que notifique al usuario de estos errores o aciertos
    #Guiar despues del exito de login a la web de envios
    #Vincular la pagina a GitHub para dejar de hostear remoto
    #Implementar acceso a la plataforma según sea admin o usuario
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    
st.set_page_config(page_title="NotStarken", page_icon=":package:", layout="centered")

lottie_coding = utils.load_lottieurl("https://lottie.host/8e37b779-c2df-49fa-a4f7-7e68ce8af9bf/MVbA5uZEbq.json")
lottie_package = utils.load_lottieurl("https://lottie.host/04a19095-661b-41c1-be0b-0f3df12b29a2/iwAl8rEub2.json")
# Sidebar Menu
show_pre_login_sidebar = True
if st.session_state['logged_in']:
    show_pre_login_sidebar = False

if show_pre_login_sidebar:
    with st.sidebar:
        selected = option_menu(
            menu_title= None,
            options=["Home", "Crea tu cuenta", "Ya tengo una cuenta"],
            icons=["house", "person-plus", "door-open"],
            menu_icon="cast",
            default_index=0,
        )
    if selected == "Home":
        # Header section
        with st.container():
            st.subheader("Envia y recibe encomiendas 📬")
            st.title("NotStarken App")
            st.write("Esta es una pagina web para enviar y recibir pedidos.")
            st.write("¿Quieres enviar algo?")
        # Who are we?
        with st.container():
            st.write("---")
            left_column, right_column = st.columns(2)
            with left_column: 
                st.title("¿Quiénes somos?")
                st.write("Somos una empresa dedicada al servicio de envío de sobres y encomiendas. Crea una cuenta o inicia sesión para concretar un envío. ")
            with right_column:
                st_lottie(lottie_coding, height=300, key = "delivery")

    if selected == "Crea tu cuenta":
        # Register form
        st.title("Regístrate aquí")
        auth.register_user()

    if selected == "Ya tengo una cuenta":
        if auth.login_user():
            st.session_state['logged_in'] = True

else:
    with st.sidebar:
            new_selected = option_menu(
                menu_title= None,
                options=["Nueva encomienda", "Seguir mi envío", "Cerrar sesión"],
                icons=["plus-circle", "search", "box-arrow-right"],
                menu_icon="new_icon",
                default_index=0,
            )
    if new_selected == "Nueva encomienda":
        st.write("---")
        left_column, right_column = st.columns(2)
        with left_column: 
            st_lottie(lottie_package, height=300, key = "package")
        with right_column:
            st.title("Nueva encomienda")
            st.write("¿Qué deseas enviar?")
            st.write("Completa el formulario para crear tu envío.")
            st.write("Los campos marcados con (*) son obligatorios.")

        