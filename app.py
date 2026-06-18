import io
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from data_analyzer import DataAnalyzer

# ----------------------------------------------------------------------
# ESTADO DE SESIÓN
# ----------------------------------------------------------------------
if "df" not in st.session_state:
    st.session_state.df = None


# ========================================================================
# MÓDULO 1: HOME
# ========================================================================
def mostrar_home():
    st.title("🏦 Análisis Exploratorio de Datos: BankMarketing")
    st.subheader("Caso de Estudio N°1 — Especialización en Python for Analytics")

    st.markdown("---")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### 🎯 Objetivo del análisis")
        st.write(
            "Esta aplicación tiene como propósito explorar el dataset de la "
            "última campaña de marketing de una institución financiera, "
            "con el fin de identificar relaciones y comportamientos entre "
            "variables que ayuden a entender la caída en la efectividad "
            "de la campaña (de 12% a 8% en los últimos 6 meses). "
            "El enfoque está orientado a la **toma de decisiones**, no a la "
            "construcción de modelos predictivos."
        )

        st.markdown("### 📊 Sobre el dataset")
        st.write(
            "El dataset **BankMarketing.csv** contiene 21 variables que "
            "describen características demográficas, financieras y de "
            "contacto de los clientes contactados durante la campaña, "
            "junto con la variable objetivo `y`, que indica si el cliente "
            "aceptó (`yes`) o no (`no`) la oferta."
        )

    with col2:
        st.markdown("### 👤 Datos del autor")
        st.info(
            f"**Nombre:** {AUTOR['nombre']}\n\n"
            f"**Curso:** {AUTOR['curso']}\n\n"
            f"**Año:** {AUTOR['anio']}"
        )

        st.markdown("### 🛠️ Tecnologías utilizadas")
        st.write("- Python 3\n- Pandas / NumPy\n- Streamlit\n- Matplotlib / Seaborn")

    st.markdown("---")
    st.caption(
        "Usa el menú de la izquierda para cargar el dataset y comenzar "
        "el análisis exploratorio."
    )

def cargar_dataset():
    st.header("📂 Carga del dataset")

    archivo = st.file_uploader("Sube el archivo BankMarketing.csv", type=["csv"])

    if archivo is None:
        st.warning("⚠️ Ningún análisis se ejecutará hasta que cargues el archivo CSV.")
        return None

    try:
        # El dataset original usa ';' como separador; se intenta autodetectar
        # por compatibilidad con otras variantes del archivo.
        df = pd.read_csv(archivo, sep=None, engine="python")
    except Exception as e:
        st.error(f"❌ No se pudo leer el archivo: {e}")
        return None

    st.success(f"✅ Archivo cargado correctamente: **{archivo.name}**")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Filas", df.shape[0])
    with col2:
        st.metric("Columnas", df.shape[1])

    st.markdown("**Vista previa del dataset (primeras filas):**")
    st.dataframe(df.head(), use_container_width=True)

    return df


def item_1_info_general(analyzer: DataAnalyzer):
    st.subheader("1️⃣ Información general del dataset")
    st.write(
        "Resumen estructural del dataset: tipo de dato por columna y "
        "conteo de valores nulos, equivalente a `.info()`."
    )

    buffer = io.StringIO()
    analyzer.df.info(buf=buffer)
    with st.expander("Ver salida de .info()"):
        st.text(buffer.getvalue())

    st.dataframe(analyzer.get_dtypes_table(), use_container_width=True)


def item_2_clasificacion_variables(analyzer: DataAnalyzer):
    st.subheader("2️⃣ Clasificación de variables")
    st.write(
        "Las columnas se clasifican automáticamente en **numéricas** y "
        "**categóricas** mediante el método `classify_variables()` de la "
        "clase `DataAnalyzer`."
    )

    numericas, categoricas = analyzer.classify_variables()

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Variables numéricas", len(numericas))
        st.write(numericas)
    with col2:
        st.metric("Variables categóricas", len(categoricas))
        st.write(categoricas)


def item_3_estadisticas_descriptivas(analyzer: DataAnalyzer):
    st.subheader("3️⃣ Estadísticas descriptivas")
    numericas, _ = analyzer.classify_variables()

    st.dataframe(analyzer.descriptive_stats(numericas), use_container_width=True)

    columna = st.selectbox(
        "Selecciona una variable numérica para ver su tendencia central:",
        numericas,
        key="item3_select",
    )
    stats = analyzer.central_tendency(columna)
    cols = st.columns(len(stats))
    for c, (k, v) in zip(cols, stats.items()):
        c.metric(k, v)

    st.caption(
        "**Interpretación:** cuando la media y la mediana están muy "
        "alejadas entre sí, suele indicar la presencia de valores "
        "extremos (outliers) o una distribución asimétrica."
    )


def item_4_valores_faltantes(analyzer: DataAnalyzer):
    st.subheader("4️⃣ Análisis de valores faltantes")
    st.write(
        "El dataset no contiene valores `NaN` técnicos, pero varias "
        "columnas categóricas usan la etiqueta **\"unknown\"** como "
        "marcador de dato faltante. Se contabilizan ambos casos."
    )

    resumen = analyzer.missing_values_summary()

    if resumen.empty:
        st.success("No se detectaron valores faltantes ni categorías 'unknown'.")
        return

    st.dataframe(resumen, use_container_width=True)

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x=resumen.index, y=resumen["Total faltantes"], ax=ax, color="#4C72B0")
    ax.set_ylabel("Cantidad de faltantes")
    ax.set_xlabel("")
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig)

    st.caption(
        "**Discusión:** columnas como `default` concentran la mayor "
        "proporción de valores 'unknown', lo que sugiere reticencia de "
        "los clientes a declarar esta información durante el contacto."
    )


def item_5_distribucion_numericas(analyzer: DataAnalyzer):
    st.subheader("5️⃣ Distribución de variables numéricas")
    numericas, _ = analyzer.classify_variables()

    columna = st.selectbox("Selecciona una variable numérica:", numericas, key="item5_select")
    bins = st.slider("Número de bins del histograma:", 5, 100, 30, key="item5_slider")

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.histplot(analyzer.df[columna], bins=bins, kde=True, ax=ax, color="#55A868")
    ax.set_title(f"Distribución de {columna}")
    st.pyplot(fig)

    st.caption(
        "**Interpretación visual:** observa si la distribución es "
        "simétrica, sesgada, o si presenta colas largas (posibles "
        "outliers) que podrían afectar la interpretación de la media."
    )


def item_6_variables_categoricas(analyzer: DataAnalyzer):
    st.subheader("6️⃣ Análisis de variables categóricas")
    _, categoricas = analyzer.classify_variables()

    columna = st.selectbox("Selecciona una variable categórica:", categoricas, key="item6_select")
    resumen = analyzer.categorical_summary(columna)
    st.dataframe(resumen, use_container_width=True)

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x=resumen.index, y=resumen["Conteo"], ax=ax, color="#C44E52")
    ax.set_ylabel("Conteo")
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig)


def item_7_bivariado_num_cat(analyzer: DataAnalyzer):
    st.subheader("7️⃣ Análisis bivariado: numérico vs categórico")
    numericas, categoricas = analyzer.classify_variables()

    col1, col2 = st.columns(2)
    with col1:
        num_col = st.selectbox("Variable numérica:", numericas, index=0, key="item7_num")
    with col2:
        cat_default = categoricas.index("y") if "y" in categoricas else 0
        cat_col = st.selectbox("Variable categórica:", categoricas, index=cat_default, key="item7_cat")

    st.dataframe(analyzer.bivariate_num_cat(num_col, cat_col), use_container_width=True)

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.boxplot(data=analyzer.df, x=cat_col, y=num_col, ax=ax)
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig)

    st.caption(
        f"**Lectura:** compara cómo se distribuye `{num_col}` entre las "
        f"categorías de `{cat_col}`, identificando diferencias en la "
        "tendencia central y dispersión entre grupos."
    )


def item_8_bivariado_cat_cat(analyzer: DataAnalyzer):
    st.subheader("8️⃣ Análisis bivariado: categórico vs categórico")
    _, categoricas = analyzer.classify_variables()

    col1, col2 = st.columns(2)
    with col1:
        cat1_default = categoricas.index("education") if "education" in categoricas else 0
        cat_col1 = st.selectbox("Primera variable categórica:", categoricas, index=cat1_default, key="item8_cat1")
    with col2:
        cat2_default = categoricas.index("y") if "y" in categoricas else 0
        cat_col2 = st.selectbox("Segunda variable categórica:", categoricas, index=cat2_default, key="item8_cat2")

    tabla = analyzer.bivariate_cat_cat(cat_col1, cat_col2)
    st.write("Proporciones por fila (%):")
    st.dataframe(tabla, use_container_width=True)

    fig, ax = plt.subplots(figsize=(9, 4))
    tabla.plot(kind="bar", stacked=True, ax=ax, colormap="viridis")
    ax.set_ylabel("Proporción (%)")
    plt.xticks(rotation=45, ha="right")
    plt.legend(title=cat_col2, bbox_to_anchor=(1.02, 1), loc="upper left")
    st.pyplot(fig)


def item_9_analisis_dinamico(analyzer: DataAnalyzer):
    st.subheader("9️⃣ Análisis dinámico según parámetros seleccionados")
    st.write(
        "Selecciona columnas y aplica filtros para explorar subconjuntos "
        "del dataset de forma interactiva."
    )

    numericas, categoricas = analyzer.classify_variables()
    todas_columnas = analyzer.df.columns.tolist()

    columnas_sel = st.multiselect(
        "Columnas a mostrar:", todas_columnas, default=todas_columnas[:6], key="item9_multiselect"
    )

    filtros = {}
    with st.expander("🔧 Filtros adicionales"):
        cat_filtro = st.selectbox("Filtrar por variable categórica:", ["(ninguna)"] + categoricas, key="item9_catf")
        if cat_filtro != "(ninguna)":
            valores = st.multiselect(
                f"Valores de {cat_filtro}:",
                analyzer.df[cat_filtro].unique().tolist(),
                key="item9_valores",
            )
            if valores:
                filtros[cat_filtro] = valores

        num_filtro = st.selectbox("Filtrar por variable numérica:", ["(ninguna)"] + numericas, key="item9_numf")
        if num_filtro != "(ninguna)":
            min_v, max_v = float(analyzer.df[num_filtro].min()), float(analyzer.df[num_filtro].max())
            rango = st.slider(f"Rango de {num_filtro}:", min_v, max_v, (min_v, max_v), key="item9_rango")
            filtros[num_filtro] = rango

        incluir_solo_yes = st.checkbox("Mostrar solo clientes que aceptaron la campaña (y = yes)", key="item9_check")
        if incluir_solo_yes and "y" in analyzer.df.columns:
            filtros["y"] = ["yes"]

    resultado = analyzer.filter_dataframe(columnas_sel if columnas_sel else None, filtros)
    st.write(f"**{resultado.shape[0]} filas** después de aplicar los filtros.")
    st.dataframe(resultado.head(50), use_container_width=True)


def item_10_hallazgos_clave(analyzer: DataAnalyzer):
    st.subheader("🔟 Hallazgos clave")

    df = analyzer.df
    tasa_global = (df["y"] == "yes").mean() * 100 if "y" in df.columns else None

    if tasa_global is not None:
        st.metric("Tasa de conversión global de la campaña", f"{tasa_global:.2f}%")

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    if "duration" in df.columns and "y" in df.columns:
        sns.boxplot(data=df, x="y", y="duration", ax=axes[0])
        axes[0].set_title("Duración del contacto vs resultado")

    if "month" in df.columns and "y" in df.columns:
        tasa_mes = df.groupby("month")["y"].apply(lambda s: (s == "yes").mean() * 100)
        tasa_mes.plot(kind="bar", ax=axes[1], color="#8172B2")
        axes[1].set_title("Tasa de conversión por mes")
        axes[1].set_ylabel("% aceptación")

    plt.tight_layout()
    st.pyplot(fig)

    st.markdown(
        """
        **Insights principales:**
        - La duración del contacto tiende a ser mayor entre los clientes que sí aceptaron la oferta,
          sugiriendo que conversaciones más largas se asocian a mayor interés del cliente.
        - La tasa de aceptación varía notablemente según el mes de contacto, lo que indica
          estacionalidad en la efectividad de la campaña.
        - Explora los ítems anteriores con distintos filtros para identificar otros patrones
          relevantes para tu propio análisis.
        """
    )


def mostrar_eda():
    st.header("📊 Análisis Exploratorio de Datos (EDA)")

    df = cargar_dataset()
    if df is None:
        return

    st.session_state.df = df
    analyzer = DataAnalyzer(df)

    tabs = st.tabs([
        "1. Info general", "2. Clasificación", "3. Descriptivas", "4. Faltantes",
        "5. Dist. numéricas", "6. Categóricas", "7. Bivariado num-cat",
        "8. Bivariado cat-cat", "9. Dinámico", "10. Hallazgos",
    ])

    with tabs[0]:
        item_1_info_general(analyzer)
    with tabs[1]:
        item_2_clasificacion_variables(analyzer)
    with tabs[2]:
        item_3_estadisticas_descriptivas(analyzer)
    with tabs[3]:
        item_4_valores_faltantes(analyzer)
    with tabs[4]:
        item_5_distribucion_numericas(analyzer)
    with tabs[5]:
        item_6_variables_categoricas(analyzer)
    with tabs[6]:
        item_7_bivariado_num_cat(analyzer)
    with tabs[7]:
        item_8_bivariado_cat_cat(analyzer)
    with tabs[8]:
        item_9_analisis_dinamico(analyzer)
    with tabs[9]:
        item_10_hallazgos_clave(analyzer)


# ========================================================================
# CONCLUSIONES
# ========================================================================
def mostrar_conclusiones():
    st.header("✅ Conclusiones finales")

    if st.session_state.df is None:
        st.info(
            "Carga el dataset en el módulo **Datos & EDA** para contextualizar "
            "mejor estas conclusiones con tus propios hallazgos."
        )

    st.markdown(
        """
        1. **La duración del contacto es el indicador más asociado a la conversión.** Los clientes que
           aceptaron la oferta sostuvieron, en promedio, llamadas más largas, lo que sugiere que el
           tiempo de conversación refleja interés genuino más que simple cortesía telefónica.

        2. **La efectividad de la campaña varía fuertemente según el mes de contacto.** Existen meses
           con tasas de aceptación notablemente superiores al promedio, lo que indica una oportunidad
           de concentrar esfuerzos comerciales en los periodos de mayor receptividad.

        3. **El nivel educativo y la situación laboral del cliente se relacionan con la probabilidad de
           aceptación.** Segmentar la oferta según estos perfiles podría mejorar la eficiencia de los
           contactos futuros.

        4. **Una proporción relevante de clientes no declara información sobre crédito en mora
           (`default`).** Esta opacidad podría estar ocultando un segmento de riesgo que merece un
           tratamiento diferenciado en próximas campañas.

        5. **La caída de efectividad de 12% a 8% no parece explicarse por un solo factor, sino por una
           combinación de timing de contacto, perfil del cliente y canal utilizado.** Un enfoque de
           segmentación más fino, apoyado en este tipo de herramientas de EDA, puede ayudar a revertir
           la tendencia sin necesidad de construir modelos predictivos complejos.
        """
    )

    st.caption(
        "Estas conclusiones están redactadas con fines orientativos; "
        "personalízalas con los hallazgos específicos que observes al "
        "explorar el dataset en el módulo de EDA."
    )

