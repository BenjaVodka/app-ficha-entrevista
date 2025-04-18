import streamlit as st
import datetime
import os

# No necesitamos la función obtener_datos_entrevista() separada con Streamlit,
# los widgets recopilan la información directamente.

def formatear_salida(datos):
    """Crea el string de texto con el formato de la ficha."""
    # Esta función es casi igual que antes
    output_string = f"""
===============================================================================
                                FICHA ENTREVISTA
===============================================================================

Nombre entrevistado:      {datos.get('nombre', '')}
Mail de contacto:         {datos.get('mail', '')}
Ocupación:                {datos.get('ocupacion', '')}
Edad:                     {datos.get('edad', '')}

-------------------------------------------------------------------------------

Registro utilizado:       {datos.get('registro', '')}
Hora de inicio y término: {datos.get('hora_inicio_termino', '')}
Link de grabación:        {datos.get('link_grabacion', '')}
Lugar de entrevista:      {datos.get('lugar', '')}

-------------------------------------------------------------------------------

Notas de campo generales:
{datos.get('notas_campo', '')}

===============================================================================
Preguntas claves:
-----------------
{datos.get('preguntas_claves', '')}

===============================================================================
Citar frases relevantes (al menos 3) Post entrevistas:
----------------------------------------------------
{datos.get('frases_relevantes', '')}

===============================================================================
Principales problemas identificados:
-----------------------------------
{datos.get('problemas_identificados', '')}

-------------------------------------------------------------------------------
Describir el problema más relevante:
-----------------------------------
{datos.get('problema_relevante', '')}

===============================================================================
"""
    return output_string

# --- Interfaz de Streamlit ---

st.set_page_config(page_title="Generador Ficha Entrevista", layout="centered") # Configura título de la pestaña

st.title("📝 Generador de Ficha de Entrevista")
st.write("Ingresa los datos de la entrevista en el formulario a continuación.")

# Usamos un formulario para que la página no se recargue con cada campo
with st.form(key="ficha_form"):
    st.header("Datos Básicos")
    col1, col2 = st.columns(2) # Crear dos columnas para mejor distribución
    with col1:
        nombre = st.text_input("Nombre entrevistado:")
        mail = st.text_input("Mail de contacto:")
        ocupacion = st.text_input("Ocupación:")
        edad = st.text_input("Edad:") # Podría ser st.number_input si prefieres
        notas_campo = st.text_area("Notas de campo generales:", height=150)

    with col2:
        registro = st.text_input("Registro utilizado (Audio, Video, Notas):")
        hora_inicio_termino = st.text_input("Hora de inicio y término (ej: 10:00 - 11:30):")
        link_grabacion = st.text_input("Link de grabación (si aplica):")
        lugar = st.text_input("Lugar de entrevista:")

    st.header("Contenido de la Entrevista")
    preguntas_claves = st.text_area("Preguntas claves realizadas (una por línea):", height=200)
    frases_relevantes = st.text_area("Frases relevantes (una por línea):", height=150)
    problemas_identificados = st.text_area("Principales problemas identificados:", height=150)
    problema_relevante = st.text_area("Describe el problema más relevante:", height=100)

    # Botón para enviar el formulario
    submitted = st.form_submit_button("✅ Generar Ficha")

# --- Procesamiento después de enviar el formulario ---
if submitted:
    if not nombre: # Validación simple
        st.error("¡Por favor, ingresa al menos el nombre del entrevistado!")
    else:
        # Recopilar datos del formulario en un diccionario
        datos_recopilados = {
            'nombre': nombre,
            'registro': registro,
            'mail': mail,
            'hora_inicio_termino': hora_inicio_termino,
            'ocupacion': ocupacion,
            'link_grabacion': link_grabacion,
            'edad': edad,
            'lugar': lugar,
            'notas_campo': notas_campo,
            'preguntas_claves': preguntas_claves, # Ya está como texto multi-línea
            'frases_relevantes': frases_relevantes, # Ya está como texto multi-línea
            'problemas_identificados': problemas_identificados,
            'problema_relevante': problema_relevante
        }

        # 2. Crear el string formateado
        texto_formateado = formatear_salida(datos_recopilados)

        # 3. Mostrar el resultado y ofrecer descarga
        st.success("¡Ficha generada exitosamente!")

        st.subheader("Vista Previa del Resumen:")
        st.text_area("Texto Formateado", texto_formateado, height=400) # Muestra el texto

        # 4. Crear nombre de archivo y botón de descarga
        nombre_base = nombre.replace(' ', '_') if nombre else 'Entrevista'
        fecha_hoy = datetime.date.today().strftime("%Y%m%d")
        nombre_archivo_salida = f"Resumen_{nombre_base}_{fecha_hoy}.txt"

        st.download_button(
            label="⬇️ Descargar Ficha (.txt)",
            data=texto_formateado, # El string que quieres descargar
            file_name=nombre_archivo_salida, # Nombre del archivo descargado
            mime='text/plain' # Tipo de archivo
       )