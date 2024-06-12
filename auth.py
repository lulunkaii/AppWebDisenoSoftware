import requests
import streamlit as st

def register_user():    
    with st.form(key='signup', clear_on_submit=True):
        st.subheader(':blue[Ingresa tus datos de envío]')
        st.write(':blue[Los datos marcados con (*) son obligatorios.]')
        rut = st.text_input('RUT', placeholder='Ex: 12345678-9 *', )
        first_name = st.text_input('Primer nombre', placeholder='Ingresa tu primer nombre *')
        second_name = st.text_input('Segundo nombre', placeholder='Ingresa tu segundo nombre')
        first_last_name = st.text_input('Primer apellido', placeholder='Ingresa tu primer apellido *')
        second_last_name = st.text_input('Segundo apellido', placeholder='Ingresa tu segundo apellido *')
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
            if response.status_code == 201:
                st.success("Usuario creado con éxito. Inicia sesión para continuar.", icon="🎉")
            elif response.status_code == 400:
                st.warning("Error en los datos ingresados", icon="🚨")
            elif response.status_code == 409:
                st.warning("Ya existe un usuario con ese rut, correo o número", icon="🚨")

            print(response.status_code)
            if not response.ok:
                print(response.json())

def login_user():
    st.title("Inicia sesión")

    with st.form(key='login', clear_on_submit=True):
        email = st.text_input('Email', placeholder='Ingresa tu correo electrónico')
        password = st.text_input("Contraseña", placeholder="Escribe tu contraseña", type="password")
        b_login = st.form_submit_button('Iniciar sesión')

        if b_login:
            response_login = requests.post('http://localhost:3000/api/v1/users/session', headers={
                "Content-Type": "application/json"
            }, json={
                'email' : email,'password' : password
            })
            if response_login.status_code == 200:
                st.success("Inicio de sesión exitoso", icon="🎉")
                return True
            elif response_login.status_code == 401:
                st.warning("Contraseña incorrecta", icon="🚨")
            elif response_login.status_code == 404:
                st.warning(body="No existen usuarios con el correo ingresado", icon="🚨")
            elif response_login.status_code == 400:
                st.warning("Contraseña incorrecta", icon="🚨")
            return False
            