import io
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


modulo = st.sidebar.selectbox("Seleccione un Módulo", ["Home","Carga de Dataset"])

if modulo == "Home":
    st.write("Bienvenido la sesión 1")
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
    # Evitamos recargar el archivo en cada rerun usando st.cache_data
    @st.cache_data
    def cargar_datos(file):
        if file.name.endswith(".csv"):
            return pd.read_csv(file, sep=";")
        elif file.name.endswith(".xlsx"):
            return pd.read_excel(file)
        return None

    datos = cargar_datos(archivo)

    if datos is not None:
        st.success("¡Dataset cargado e indexado correctamente!")

        # Estructura limpia mediante pestañas nativas
        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            [
                "📋 Ítem 1: Info General",
                "🗂️ Ítem 2: Clasificación",
                "📊 Ítem 3: Estadísticas",
                "🔍 Ítem 4: Faltantes",
                "📈 Ítem 5: Distribución",
            ]
        )

        # ==========================================
        # ÍTEM 1: INFORMACIÓN GENERAL DEL DATASET
        # ==========================================
        with tab1:
            st.header("Ítem 1: Información General")

            # Layout con columnas para métricas clave
            filas, columnas = datos.shape
            col1, col2 = st.columns(2)
            col1.metric("Total de Registros (Filas)", f"{filas:,}")
            col2.metric("Total de Variables (Columnas)", columnas)

            st.subheader("Estructura técnica de las columnas (.info())")
            buffer = io.StringIO()
            datos.info(buf=buffer)
            st.text(buffer.getvalue())

            st.subheader("Mapeo explícito de tipos de datos")
            st.dataframe(datos.dtypes.astype(str).to_frame(name="Tipo de Dato"))

        # ==========================================
        # ÍTEM 2: CLASIFICACIÓN DE VARIABLES
        # ==========================================
        with tab2:
            st.header("Ítem 2: Clasificación de Variables")

            # Función personalizada requerida en la rúbrica
            def segmentar_columnas(df):
                num_cols = df.select_dtypes(include=["number"]).columns.tolist()
                cat_cols = df.select_dtypes(
                    include=["object", "category", "bool"]
                ).columns.tolist()
                return num_cols, cat_cols

            numericas, categoricas = segmentar_columnas(datos)

            c1, c2 = st.columns(2)
            with c1:
                st.subheader(f"🔢 Numéricas ({len(numericas)})")
                st.dataframe(pd.Series(numericas, name="Variable"))
            with c2:
                st.subheader(f"🔤 Categóricas ({len(categoricas)})")
                st.dataframe(pd.Series(categoricas, name="Variable"))

            st.markdown(
                "**Discusión:** La separación automatizada permite definir qué algoritmos o transformaciones matemáticas aplican a cada tipo de dato."
            )

        # ==========================================
        # ÍTEM 3: ESTADÍSTICAS DESCRIPTIVAS
        # ==========================================
        with tab3:
            st.header("Ítem 3: Estadísticas Descriptivas")

            st.subheader("Matriz resumen (.describe())")
            st.dataframe(datos.describe())

            st.info(
                "💡 **Guía de análisis:** Compara la media con el percentil 50% (mediana). Si difieren drásticamente, la variable posee un sesgo importante causado por valores atípicos (outliers)."
            )

        # ==========================================
        # ÍTEM 4: ANÁLISIS DE VALORES FALTANTES
        # ==========================================
        with tab4:
            st.header("Ítem 4: Análisis de Valores Faltantes")

            # Cálculo y porcentaje de nulos
            df_nulos = datos.isnull().sum().to_frame(name="Cantidad Nulos")
            df_nulos["Porcentaje (%)"] = round(
                (df_nulos["Cantidad Nulos"] / filas) * 100, 2
            )

            st.subheader("Tabla de valores nulos detectados")
            st.dataframe(df_nulos)

            total_nulos = datos.isnull().sum().sum()
            if total_nulos > 0:
                st.subheader("Visualización espacial de nulos")
                fig_null, ax_null = plt.subplots(figsize=(10, 3))
                sns.heatmap(
                    datos.isnull(),
                    cbar=False,
                    yticklabels=False,
                    cmap="plasma",
                    ax=ax_null,
                )
                st.pyplot(fig_null)
                st.warning(
                    f"Atención: Se registran {total_nulos} celdas vacías en la matriz de datos."
                )
            else:
                st.success(
                    "🎉 Conclusión: Dataset 100% íntegro. No requiere imputación de datos."
                )

        # ==========================================
        # ÍTEM 5: DISTRIBUCIÓN DE VARIABLES NUMÉRICAS
        # ==========================================
        with tab5:
            st.header("Ítem 5: Distribución de Variables")

            if numericas:
                # Selector dinámico: evita renderizar múltiples gráficos que saturan la memoria
                var_target = st.selectbox(
                    "Selecciona la columna numérica a graficar:",
                    numericas,
                    key="selector_histograma",
                )

                # Renderizado limpio aislando la figura de matplotlib
                fig, ax = plt.subplots(figsize=(10, 4))
                sns.histplot(datos[var_target], kde=True, color="#2b5c8f", ax=ax)
                ax.set_title(f"Histograma de Frecuencias: {var_target}")

                st.pyplot(fig)
                plt.close(fig)  # Liberación explícita de memoria

                st.markdown(
                    f"**Interpretación visual:** La gráfica describe el comportamiento probabilístico y la dispersión de la variable **{var_target}**."
                )
            else:
                st.error(
                    "El set de datos no contiene propiedades de tipo numérico para su graficación."
                )
