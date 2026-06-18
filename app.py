import io
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


modulo = st.sidebar.selectbox("Seleccione un Módulo", ["Home","Carga de Dataset"])

if modulo == "Home":
    else:

    
    st.title("Módulo 2: Carga del dataset")
    
    # =========================================================================
    # SUGERENCIA Y DESCARGA DEL DATASET OFICIAL
    # =========================================================================
    st.info("💡 **Nota para el usuario:** Para utilizar esta aplicación, debes cargar el dataset oficial del proyecto.")
    
    try:
        # Leemos tu archivo que ya está guardado en tu repositorio de GitHub
        with open("BankMarketing.csv", "rb") as file:
            st.download_button(
                label="📥 Haz clic aquí para descargar el dataset oficial (.csv)",
                data=file,
                file_name="BankMarketing.csv",
                mime="text/csv",
                help="Descarga este archivo y luego súbelo en el recuadro de abajo."
            )
    except FileNotFoundError:
        st.error("⚠️ Error técnico: Asegúrate de renombrar tu archivo como 'BankMarketing.csv' en tu repositorio de GitHub.")
