import streamlit as st
import datetime
import os # Aunque no se usa explícitamente aquí, es bueno tenerlo por si acaso

# --- Función para formatear la salida como HTML (Versión Corregida) ---
def formatear_salida_html(datos):
    """Crea el string de HTML con el formato de la ficha, pre-procesando el texto."""

    # Estilos CSS simples para mejorar un poco la apariencia (opcional)
    styles = """
    <style>
        body { font-family: sans-serif; margin: 15px;}
        table { width: 100%; border-collapse: collapse; margin-bottom: 15px; }
        th, td { text-align: left; padding: 8px; border: 1px solid #ddd; vertical-align: top;}
        th { background-color: #f2f2f2; font-weight: bold; }
        .header-section { background-color: #444; color: white; padding: 10px; text-align: center; font-size: 1.2em; margin-top: 15px; margin-bottom: 10px; font-weight: bold;}
        .section-title { font-weight: bold; margin-top: 15px; margin-bottom: 5px; border-bottom: 1px solid #ccc; padding-bottom: 3px;}
        pre { white-space: pre-wrap; word-wrap: break-word; background-color: #f9f9f9; border: 1px solid #eee; padding: 10px; margin-top: 0px; font-family: inherit;}
        b { font-weight: bold; }
    </style>
    """

    # --- Pre-procesamiento de los datos para HTML ---
    # Escapamos caracteres HTML básicos para evitar problemas
    def escape_html(text):
        """Función simple para escapar caracteres HTML básicos."""
        if isinstance(text, str): # Asegura que sea string antes de reemplazar
             return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        return text # Devuelve el original si no es string (ej: None)


    nombre_html = escape_html(datos.get('nombre', ''))
    mail_html = escape_html(datos.get('mail', ''))
    ocupacion_html = escape_html(datos.get('ocupacion', ''))
    edad_html = escape_html(datos.get('edad', ''))
    registro_html = escape_html(datos.get('registro', ''))
    hora_html = escape_html(datos.get('hora_inicio_termino', ''))
    link_html = escape_html(datos.get('link_grabacion', ''))
    lugar_html = escape_html(datos.get('lugar', ''))

    # Para los campos que van en <pre>, escapamos HTML y reemplazamos \n por <br>
    # Aseguramos que sea string antes de llamar a replace
    notas_campo_raw = datos.get('notas_campo', '')
    notas_campo_html = escape_html(notas_campo_raw).replace('\n', '<br>') if isinstance(notas_campo_raw, str) else notas_campo_raw

    preguntas_claves_raw = datos.get('preguntas_claves', '')
    preguntas_claves_html = escape_html(preguntas_claves_raw).replace('\n', '<br>') if isinstance(preguntas_claves_raw, str) else preguntas_claves_raw

    frases_relevantes_raw = datos.get('frases_relevantes', '')
    frases_relevantes_html = escape_html(frases_relevantes_raw).replace('\n', '<br>') if isinstance(frases_relevantes_raw, str) else frases_relevantes_raw

    problemas_identificados_raw = datos.get('problemas_identificados', '')
    problemas_identificados_html = escape_html(problemas_identificados_raw).replace('\n', '<br>') if isinstance(problemas_identificados_raw, str) else problemas_identificados_raw

    problema_relevante_raw = datos.get('problema_relevante', '')
    problema_relevante_html = escape_html(problema_relevante_raw).replace('\n', '<br>') if isinstance(problema_relevante_raw, str) else problema_relevante_raw
    # --- Fin Pre-procesamiento ---


    # Ahora usamos las variables pre-procesadas dentro de la f-string principal
    html_string = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Ficha Entrevista - {nombre_html}</title>
    {styles}
</head>
<body>
    <div class="header-section">FICHA ENTREVISTA</div>

    <table>
        <tr>
            <th style="width:50%;">Datos Personales</th>
            <th style="width:50%;">Detalles de la Entrevista</th>
        </tr>
        <tr>
            <td>
                <b>Nombre entrevistado:</b> {nombre_html}<br>
                <b>Mail de contacto:</b> {mail_html}<br>
                <b>Ocupación:</b> {ocupacion_html}<br>
                <b>Edad:</b> {edad_html}
            </td>
            <td>
                <b>Registro utilizado:</b> {registro_html}<br>
                <b>Hora de inicio y término:</b> {hora_html}<br>
                <b>Link de grabación:</b> {link_html}<br>
                <b>Lugar de entrevista:</b> {lugar_html}
            </td>
        </tr>
    </table>

    <div class="section-title">Notas de campo generales:</div>
    <pre>{notas_campo_html}</pre>

    <div class="section-title">Preguntas claves:</div>
    <pre>{preguntas_claves_html}</pre>

    <div class="section-title">Citar frases relevantes (al menos 3) Post entrevistas:</div>
    <pre>{frases_relevantes_html}</pre>

    <div class="section-title">Principales problemas identificados:</div>
    <pre>{problemas_identificados_html}</pre>

    <div class="section-title">Describir el problema más relevante:</div>
    <pre>{problema_relevante_html}</pre>

</body>
</html>
"""
    return html_string


# --- Interfaz de Streamlit ---

st.set_page_config(page_title="Generador Ficha Entrevista", layout="wide") # 'wide' puede verse mejor

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

    with col2:
        # Usamos selectbox para el registro
        registro_opciones = ["", "Audio", "Video", "Notas Presenciales", "Videoconferencia", "Otro"] # Añadida opción vacía
        registro = st.selectbox("Registro utilizado:", registro_opciones)
        hora_inicio_termino = st.text_input("Hora de inicio y término (ej: 10:00 - 11:30):")
        link_grabacion = st.text_input("Link de grabación (si aplica):")
        lugar = st.text_input("Lugar de entrevista:")

    # Notas generales fuera de las columnas
    notas_campo = st.text_area("Notas de campo generales:", height=100)

    st.header("Contenido de la Entrevista")
    preguntas_claves = st.text_area("Preguntas claves realizadas (una por línea):", height=150)
    frases_relevantes = st.text_area("Frases relevantes (una por línea):", height=150)
    problemas_identificados = st.text_area("Principales problemas identificados:", height=150)
    problema_relevante = st.text_area("Describe el problema más relevante:", height=100)

    # Botón para enviar el formulario
    submitted = st.form_submit_button("✅ Generar Ficha HTML")

# --- Procesamiento después de enviar el formulario ---
if submitted:
    if not nombre: # Validación simple
        st.error("¡Por favor, ingresa al menos el nombre del entrevistado!")
    else:
        # Recopilar datos del formulario en un diccionario
        datos_recopilados = {
            'nombre': nombre,
            'registro': registro, # Toma el valor del selectbox
            'mail': mail,
            'hora_inicio_termino': hora_inicio_termino,
            'ocupacion': ocupacion,
            'link_grabacion': link_grabacion,
            'edad': edad,
            'lugar': lugar,
            'notas_campo': notas_campo,
            'preguntas_claves': preguntas_claves,
            'frases_relevantes': frases_relevantes,
            'problemas_identificados': problemas_identificados,
            'problema_relevante': problema_relevante
        }

        # 2. Crear el string HTML formateado llamando a la función correcta
        html_formateado = formatear_salida_html(datos_recopilados)

        st.success("¡Ficha HTML generada exitosamente!")

        # 3. Mostrar vista previa y botón de descarga HTML
        st.subheader("Vista Previa (Renderizado HTML):")
        # Usamos markdown con unsafe_allow_html para intentar mostrarlo
        st.markdown(html_formateado, unsafe_allow_html=True)

        # st.subheader("Código HTML Generado:") # Opcional: mostrar el código crudo
        # st.code(html_formateado, language='html')

        # 4. Crear nombre de archivo y botón de descarga HTML
        nombre_base_archivo = ''.join(filter(str.isalnum, nombre.replace(' ', '_'))) if nombre else 'Entrevista' # Limpia nombre para archivo
        fecha_hoy = datetime.date.today().strftime("%Y%m%d")
        nombre_archivo_salida = f"Resumen_{nombre_base_archivo}_{fecha_hoy}.html" # Extensión .html

        st.download_button(
            label="⬇️ Descargar Ficha (.html)",
            data=html_formateado, # El string HTML
            file_name=nombre_archivo_salida, # Nombre del archivo .html
            mime='text/html' # Indicamos que es HTML
        )