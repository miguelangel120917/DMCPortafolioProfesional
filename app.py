import io
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.image('Logo.png')
modulo = st.sidebar.selectbox("Seleccione un Módulo", ["Home","Carga de Dataset"])

if modulo == "Home":
        st.title("🏦 Análisis Exploratorio de Datos: BankMarketing")
        st.divider()
        st.markdown("### 🎯 Objetivo del análisis")
        st.write(
            "Esta aplicación tiene como propósito explorar el dataset de la "
            "última campaña de marketing de una institución financiera, "
            "con el fin de identificar relaciones y comportamientos entre variables"  
        )
        st.markdown("### 👤 Datos del autor")

        st.write("- Nombre: Miguel Angel Limaquispe Huaman\n- Especialización: Especialización en Python for Analytics\n- Año: Junio 2026")
        
        st.markdown("### 📊 Sobre el Dataset")
        st.write(
            "El dataset **BankMarketing.csv** contiene 21 variables que "
            "describen características demográficas, financieras y de "
            "contacto de los clientes contactados durante la campaña, "
            "junto con la variable objetivo `y`, que indica si el cliente "
            "aceptó (`yes`) o no (`no`) la oferta."
        )

        st.markdown("### 🛠️ Tecnologías utilizadas")
        st.write("- Python 3\n- Pandas / NumPy\n- Streamlit\n- Matplotlib / Seaborn")

        st.markdown("---")
        st.caption(
            "Usa el menú de la izquierda para cargar el dataset y comenzar "
            "el análisis exploratorio."
        )

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
                label="📥 Haz clic aquí para descargar el dataset oficial",
                data=file,
                file_name="BankMarketing.csv",
                mime="text/csv",
                help="Descarga este archivo y luego súbelo en el recuadro de abajo."
            )
    except FileNotFoundError:
        st.error("⚠️ Error técnico: Asegúrate de renombrar tu archivo como 'BankMarketing.csv' en tu repositorio de GitHub.")
    archivo=st.sidebar.file_uploader("Cargue su archivo")
   # (Este bloque se ejecuta una vez cargado el archivo con éxito)
    if archivo is not None:
    
        # 1. Optimización con Caché para lectura eficiente
        @st.cache_data
        def cargar_datos(file):
            if file.name.endswith(".csv"):
                return pd.read_csv(file, sep=";")
            elif file.name.endswith(".xlsx"):
                return pd.read_excel(file)
            return None
    
        datos_originales = cargar_datos(archivo)
    
        if datos_originales is not None:
            # Copia local para manipulación de datos
            datos = datos_originales.copy()
    
            # ==========================================
            # 🛠️ COMPONENTE: st.sidebar
            # ==========================================
            st.sidebar.header("⚙️ Panel de Control y Filtros")
    
            # Requerimiento: Uso de st.checkbox
            activar_filtro = st.sidebar.checkbox(
                "Activar filtro de filas",
                value=False,
                help="Marca esta opción si deseas limitar la cantidad de datos analizados en las pestañas.",
            )
    
            if activar_filtro:
                # Requerimiento: Uso de st.slider (Filtrar dinámicamente por volumen de registros)
                max_filas = len(datos)
                rango_filas = st.sidebar.slider(
                    "Selecciona el rango de filas a procesar:",
                    min_value=1,
                    max_value=max_filas,
                    value=(1, min(1000, max_filas)),
                )
                # Aplicamos el filtro al DataFrame actual
                datos = datos.iloc[rango_filas[0] - 1 : rango_filas[1]]
                st.sidebar.info(
                    f"Dataset filtrado: mostrando desde fila {rango_filas[0]} hasta {rango_filas[1]}."
                )
    
            st.success("¡Dataset indexado en memoria correctamente!")
            st.write("### Vista previa del Dataset activo:")
            st.dataframe(datos.head(5))
    
            # ==========================================
            # 🛠️ COMPONENTE: st.tabs (Los 5 Ítems solicitados)
            # ==========================================
            tab1, tab2, tab3, tab4, tab5 = st.tabs(
                [
                    "📋 Ítem 1: Info General",
                    "🗂️ Ítem 2: Clasificación",
                    "📊 Ítem 3: Estadísticas",
                    "🔍 Ítem 4: Faltantes",
                    "📈 Ítem 5: Distribución",
                ]
            )
    
            # Extracción automática de tipos para los componentes interactivos
            num_cols = datos.select_dtypes(include=["number"]).columns.tolist()
            cat_cols = datos.select_dtypes(
                include=["object", "category", "bool"]
            ).columns.tolist()
    
            # ------------------------------------------
            # ÍTEM 1: INFORMACIÓN GENERAL DEL DATASET
            # ------------------------------------------
            with tab1:
                st.header("Ítem 1: Información General")
    
                # Requerimiento: Uso de st.columns
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total de Filas Actuales", f"{datos.shape[0]:,}")
                with col2:
                    st.metric("Total de Columnas", datos.shape[1])
    
                st.subheader("Estructura técnica de las columnas (.info())")
                buffer = io.StringIO()
                datos.info(buf=buffer)
                st.text(buffer.getvalue())
    
                st.subheader("Mapeo de Tipos de Datos nativos")
                st.dataframe(datos.dtypes.astype(str).to_frame(name="Tipo de Dato"))
                st.subheader("Conteo de valores Nulos")
                st.dataframe(datos.isnull().sum().reset_index(name='Cantidad_Nulos'))
    
            # ------------------------------------------
            # ÍTEM 2: CLASIFICACIÓN DE VARIABLES
            # ------------------------------------------
            with tab2:
                st.header("Ítem 2: Clasificación de Variables")
    
                # Función personalizada requerida en la rúbrica
                def clasificar_columnas_custom(df):
                    numericas = df.select_dtypes(include=["number"]).columns.tolist()
                    categoricas = df.select_dtypes(
                        include=["object", "category", "bool"]
                    ).columns.tolist()
                    return numericas, categoricas
    
                vars_num, vars_cat = clasificar_columnas_custom(datos)
    
                col_a, col_b = st.columns(2)
                with col_a:
                    st.subheader(f"🔢 Numéricas ({len(vars_num)})")
                    st.dataframe(pd.Series(vars_num, name="Nombre Variable"))
                with col_b:
                    st.subheader(f"🔤 Categóricas ({len(vars_cat)})")
                    st.dataframe(pd.Series(vars_cat, name="Nombre Variable"))
    
            # ------------------------------------------
            # ÍTEM 3: ESTADÍSTICAS DESCRIPTIVAS
            # ------------------------------------------
            with tab3:
                st.header("Ítem 3: Estadísticas Descriptivas")
    
                st.subheader("Matriz de resumen analítico (.describe())")
                st.dataframe(datos.describe())
    
                # Requerimiento: Uso de st.multiselect (Análisis estadístico específico de columnas elegidas)
                if vars_num:
                    st.subheader("🔍 Comparador específico de variables")
                    columnas_seleccionadas = st.multiselect(
                        "Selecciona columnas numéricas específicas para aislar sus estadísticas:",
                        options=vars_num,
                        default=vars_num[:2] if len(vars_num) >= 2 else vars_num,
                    )
    
                    if columnas_seleccionadas:
                        st.dataframe(datos[columnas_seleccionadas].describe())
                    else:
                        st.warning("Selecciona al menos una variable en el recuadro superior.")
    
            # ------------------------------------------
            # ÍTEM 4: ANÁLISIS DE VALORES FALTANTES
            # ------------------------------------------
            with tab4:
                st.header("Ítem 4: Análisis de Valores Faltantes")
    
                df_nulos = datos.isnull().sum().to_frame(name="Cantidad Nulos")
                df_nulos["Porcentaje (%)"] = round(
                    (df_nulos["Cantidad Nulos"] / len(datos)) * 100, 2
                )
    
                st.subheader("Frecuencia de nulos por entidad")
                st.dataframe(df_nulos)
    
                total_nulos = datos.isnull().sum().sum()
                if total_nulos > 0:
                    st.subheader("Mapa de calor de la distribución de nulos")
                    fig_null, ax_null = plt.subplots(figsize=(10, 3))
                    sns.heatmap(
                        datos.isnull(),
                        cbar=False,
                        yticklabels=False,
                        cmap="mako",
                        ax=ax_null,
                    )
                    st.pyplot(fig_null)
                    plt.close(fig_null)
                else:
                    st.success("🎉 Datos completamente limpios. No se registran vacíos.")
    
            # ------------------------------------------
            # ÍTEM 5: DISTRIBUCIÓN DE VARIABLES NUMÉRICAS
            # ------------------------------------------
            with tab5:
                st.header("Ítem 5: Distribución de Variables Numéricas")
    
                if vars_num:
                    # Requerimiento: Uso de st.selectbox (Elegir dinámicamente la variable a graficar)
                    var_target = st.selectbox(
                        "Selecciona la columna numérica para renderizar el Histograma:",
                        options=vars_num,
                        key="sb_histograma",
                    )
    
                    # Renderizado controlado usando Matplotlib y Seaborn
                    fig, ax = plt.subplots(figsize=(10, 4))
                    sns.histplot(datos[var_target], kde=True, color="#1f77b4", ax=ax)
                    ax.set_title(f"Histograma de Frecuencias e Densidad (KDE): {var_target}")
                    ax.set_xlabel(var_target)
                    ax.set_ylabel("Frecuencia")
    
                    st.pyplot(fig)
                    plt.close(fig)  # Evitamos fugas de memoria en el servidor web
                else:
                    st.error("No existen propiedades de formato numérico para graficar.")
