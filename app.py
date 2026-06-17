import streamlit as st
import pandas as pd
import numpy as np
#import libreria_funciones_proyecto1 as lfp

# st.sidebar.image('DMC.png')
app_mode = st.sidebar.selectbox('_Secciones_',['Home','Carga Dataset','Conclusiones'])

if app_mode == 'Home':
  st.title ('Primer Proyecto de Portafolio Profesional')
  st.subheader("_Streamlit_ is :blue[cool] :sunglasses:")
  # st.image('Python_logo.png')
  st.markdown(
    '''
    Breve descripción del objetivo del análisis: Basado en la estadística Descriptiva para analizar los Datos y obtener conclusiones
    Estudiante: Miguel Angel Limaquispe Huaman
    Especialización: Especialización con Python potenciado con la Inteligencia Artificial
    Año: Abril - Mayo 2026
    Descripción del Dataset: Contiene datos de una entidad bancaria
    Tecnologías utilizadas (Python, Pandas, Streamlit, etc.)
    '''
    )
elif app_mode == 'Carga Dataset':
    
  # --- Configuración de la página ---
  st.set_page_config(page_title="Ejercicio 1 - Flujo de Caja", page_icon="💰")
  
  # --- Descripción del ejercicio ---
  st.markdown("""
  ## Flujo de caja con listas
  Dataset contiene información Bancaria
  """)
  
  st.divider()
  st.file_uploader()
else app_mode == 'Conclusiones':
  st.markdown(
    '''
    Breve descripción del objetivo del análisis: Basado en la estadística Descriptiva para analizar los Datos y obtener conclusiones
    Estudiante: Miguel Angel Limaquispe Huaman
    Especialización: Especialización con Python potenciado con la Inteligencia Artificial
    Año: Abril - Mayo 2026
    Descripción del Dataset: Contiene datos de una entidad bancaria
    Tecnologías utilizadas (Python, Pandas, Streamlit, etc.)
    '''
    )

 
