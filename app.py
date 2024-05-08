import pickle
from pathlib import Path

import streamlit as st
import requests
import streamlit_authenticator as stauth
import re
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie

st.set_page_config(page_title="My webpage", page_icon=":package:", layout="centered")


#To-do 
    #Incluir posibles códigos de salida (error o success) 201, 400 y 409  para registro y login de usuario
    #Junto a esto, un recurso gráfico que notifique al usuario de estos errores o aciertos
    #Guiar despues del exito de login a la web de envios
    #Vincular la pagina a GitHub para dejar de hostear remoto
    #Implementar acceso a la plataforma según sea admin o usuario


# Loading assets
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_coding = load_lottieurl("https://lottie.host/8e37b779-c2df-49fa-a4f7-7e68ce8af9bf/MVbA5uZEbq.json")

# Sidebar Menu
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
    with st.form(key='signup', clear_on_submit=True):
        st.subheader(':blue[Ingresa tus datos de envío]')
        st.write(':blue[Los datos marcados con (*) son obligatorios.]')
        rut = st.text_input('RUT', placeholder='Ex: 12345678-9 *', )
        first_name = st.text_input('Primer nombre', placeholder='Ingresa tu primer nombre *')
        second_name = st.text_input('Segundo nombre', placeholder='Ingresa tu segundo nombre')
        first_last_name = st.text_input('Primer apellido', placeholder='Ingresa tu primer apellido *')
        second_last_name = st.text_input('Primer apellido', placeholder='Ingresa tu segundo apellido *')
        email = st.text_input('Email', placeholder='Ingresa tu correo electrónico *')
        phone = st.text_input('Número de contacto', placeholder='Ex: 912345678 *')
        adress_region = st.text_input('Región', placeholder='Ex: Biobío *')
        adress_city = st.text_input('Ciudad', placeholder='Ex: Concepción *')
        adress_street = st.text_input('Calle', placeholder='Ex: Tucapel *')
        adress_number = st.text_input('Número de dirección', placeholder='Ex: 123 *')
        adress_secondary = st.text_input('Dirección secundaria', placeholder='Dirección secundaria en caso de ausencia')
        password = st.text_input("Contraseña", placeholder="Escribe tu contraseña (mín. 8 caracteres) *", type="password")

        b_signup = st.form_submit_button('Registrarse')
        if b_signup:
            password = st.session_state["password"]
            response = requests.post('http://localhost:3000/api/v1/users', headers={
                "Content-Type": "application/json"
            }, json={
                'rut' : rut, 'first_name' : first_name, 'second_name' : second_name,
                'first_last_name' : first_last_name, 'second_last_name' : second_last_name,
                'email' : email, 'phone' : int(phone),
                'address' : {
                    'region' : adress_region, 'city' : adress_city, 'street' : adress_street,
                    'number' : int(adress_number), 'secondary' : adress_secondary},
                'password' : password
            })
            print(response.status_code)
            if not response.ok:
                print(response.json())

        
if selected == "Ya tengo una cuenta":
    # User Authentication
    st.title("Inicia sesión")

    with st.form(key='login', clear_on_submit=True):
        email = st.text_input('Email', placeholder='Ingresa tu correo electrónico')
        password = st.text_input("Contraseña", placeholder="Escribe tu contraseña", type="password")
        b_login = st.form_submit_button('Iniciar sesión')

        if b_login:
            response_login = requests.post('http://localhost:3000/api/v1/users/login', headers={
                "Content-Type": "application/json"
            }, json={
                'email' : email,'password' : password
            })
            print(response_login.status_code)
            if not response_login.ok:
                print(response_login.json())