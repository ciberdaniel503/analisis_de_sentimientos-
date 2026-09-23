
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob


st.set_page_config(
    page_title="Sentiment AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)




st.markdown("""
<style>

    /* Fondo general estilo tecnológico */
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        color: #e8e8e8;
    }

    /* Contenedor principal */
    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Títulos estilo tech */
    h1 {
        color: #00d4ff;
        font-size: 46px !important;
        font-weight: 800 !important;
        letter-spacing: -1px;
        margin-bottom: 0.5rem !important;
        text-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
    }

    h2 {
        color: #00d4ff;
        font-weight: 700 !important;
        font-size: 26px !important;
        letter-spacing: -0.5px;
        border-bottom: 2px solid #00d4ff;
        padding-bottom: 8px;
    }

    h3 {
        color: #7dd3fc;
        font-weight: 600 !important;
    }

    /* Texto */
    p, label {
        color: #94a3b8 !important;
        font-size: 15px;
    }

    /* Text Area estilo tecnológico */
    textarea {
        background: #1e293b !important;
        color: #e8e8e8 !important;
        border: 2px solid #334155 !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        transition: all 0.2s ease;
    }

    textarea:focus {
        border: 2px solid #00d4ff !important;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.4) !important;
        background: #1e293b !important;
    }

    /* Selectbox estilo tech */
    div[data-baseweb="select"] > div {
        background: #1e293b !important;
        border-radius: 8px !important;
        border: 2px solid #334155 !important;
        color: #e8e8e8 !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        transition: all 0.2s ease;
    }

    div[data-baseweb="select"] > div:hover {
        border-color: #00d4ff !important;
        box-shadow: 0 0 10px rgba(0, 212, 255, 0.3);
    }

    /* Botones estilo tech */
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        border: 2px solid #00d4ff;
        background: #0f172a;
        color: #00d4ff;
        font-weight: 700;
        padding: 0.8rem 1.2rem;
        transition: all 0.2s ease;
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.2);
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .stButton > button:hover {
        background: #00d4ff;
        color: #0f172a;
        box-shadow: 0 6px 20px rgba(0, 212, 255, 0.5);
        transform: translateY(-2px);
    }

    .stButton > button:active {
        transform: translateY(0);
    }

    /* Métricas estilo tech */
    div[data-testid="stMetric"] {
        background: #1e293b !important;
        border: 2px solid #334155 !important;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        transition: all 0.2s ease;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 212, 255, 0.3);
        border-color: #00d4ff !important;
    }

    div[data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-weight: 600;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    div[data-testid="stMetricValue"] {
        color: #00d4ff !important;
        font-weight: 700;
        font-size: 32px;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.3);
    }

    /* Expander */
    .streamlit-expanderHeader {
        background: #1e293b !important;
        border-radius: 8px;
        color: #e8e8e8 !important;
        border: 2px solid #334155 !important;
        font-weight: 600;
    }

    /* File uploader */
    section[data-testid="stFileUploaderDropzone"] {
        background: #1e293b !important;
        border: 2px dashed #475569;
        border-radius: 12px;
        transition: all 0.2s ease;
    }

    section[data-testid="stFileUploaderDropzone"]:hover {
        border-color: #00d4ff;
        background: #1e293b !important;
    }

    /* Dataframe */
    div[data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        border: 1px solid #334155;
    }

    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #00d4ff 0%, #7dd3fc 100%);
    }

    /* Success/Info/Error messages */
    .stSuccess {
        background: rgba(34, 197, 94, 0.15) !important;
        border-left: 4px solid #22c55e !important;
        border-radius: 8px;
        color: #22c55e !important;
    }

    .stError {
        background: rgba(239, 68, 68, 0.15) !important;
        border-left: 4px solid #ef4444 !important;
        border-radius: 8px;
        color: #ef4444 !important;
    }

    .stInfo {
        background: rgba(0, 212, 255, 0.15) !important;
        border-left: 4px solid #00d4ff !important;
        border-radius: 8px;
        color: #00d4ff !important;
    }

    /* Línea divisoria */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, #334155 50%, transparent 100%);
        margin-top: 35px;
        margin-bottom: 35px;
    }

    /* Pie de página */
    .footer {
        text-align: center;
        padding: 30px 20px 20px 20px;
        margin-top: 50px;
        border-top: 2px solid #334155;
        background: #1e293b;
        border-radius: 12px;
    }

    .footer-title {
        color: #00d4ff;
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .footer-text {
        color: #94a3b8;
        font-size: 14px;
        margin-top: 8px;
    }

    .footer-course {
        color: #7dd3fc;
        font-size: 13px;
        margin-top: 6px;
        font-weight: 600;
    }

    /* Ocultar menú de Streamlit */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

</style>
""", unsafe_allow_html=True)



positive_words_es = {
    'bueno', 'excelente', 'maravilloso', 'fantástico', 'increíble', 'genial', 
    'feliz', 'contento', 'alegre', 'satisfecho', 'encantado', 'emocionado',
    'amor', 'amar', 'gusta', 'gustar', 'placer', 'disfrutar', 'disfruto',
    'perfecto', 'ideal', 'mejor', 'mejorar', 'éxito', 'exitoso', 'triunfo',
    'brillante', 'hermoso', 'bonito', 'lindo', 'precioso', 'hermosa',
    'recomendar', 'recomiendo', 'gracias', 'agradecer', 'agradecido',
    'positivo', 'bien', 'fantástica', 'excelente', 'increíble', 'maravilloso',
    'genial', 'perfecto', 'increíblemente', 'fantásticamente', 'excelentemente',
    'contenta', 'felices', 'alegres', 'satisfechos', 'encantados', 'emocionados',
    'hermosa', 'bonita', 'linda', 'preciosa', 'guapa', 'bella',
    'contentos', 'felizmente', 'contentamente', 'alegremente', 'satisfactoriamente',
    'encanta', 'encantar', 'quiere', 'querer', 'maravilla', 'maravillar', 'asombroso',
    'gran', 'grande', 'impresionante', 'extraordinario', 'súper', 'increíble',
    'maravillosamente', 'perfectamente', 'excelentemente', 'genialmente'
}

negative_words_es = {
    'malo', 'terrible', 'horrible', 'pésimo', 'fatal', 'espantoso', 'aterrador',
    'triste', 'deprimido', 'descontento', 'infeliz', 'decepcionado', 'frustrado',
    'odio', 'odiar', 'disgusto', 'disgustar', 'repugnancia', 'asco',
    'peor', 'empeorar', 'fracaso', 'fracasar', 'desastre', 'catastrófico',
    'feo', 'horrible', 'asqueroso', 'repugnante', 'desagradable',
    'no recomendar', 'no recomiendo', 'queja', 'quejarse', 'lamento',
    'negativo', 'mal', 'terriblemente', 'horriblemente', 'pésimamente',
    'pesadilla', 'insoportable', 'intolerable', 'inaceptable'
}

def detect_spanish_simple(text):
    """
    Detección simple de español basada en caracteres especiales y palabras comunes.
    """
    spanish_chars = set('áéíóúüñ¿¡')
    text_lower = text.lower()
    
    
    spanish_char_count = sum(1 for char in text_lower if char in spanish_chars)
    
    
    if spanish_char_count > 0:
        return True
    

    spanish_common_words = {
        'el', 'la', 'los', 'las', 'un', 'una', 'de', 'en', 'que', 'y', 'a', 'en', 
        'por', 'para', 'con', 'sin', 'sobre', 'entre', 'hacia', 'hasta', 'desde', 
        'este', 'esta', 'estos', 'estas', 'ese', 'esa', 'esos', 'esas', 
        'aquel', 'aquella', 'aquellos', 'aquellas', 'mi', 'tu', 'su', 
        'nuestro', 'nuestra', 'vuestro', 'vuestra', 'mis', 'tus', 'sus', 
        'nuestros', 'nuestras', 'vuestros', 'vuestras',
        # Verbos comunes en español
        'estoy', 'estás', 'está', 'estamos', 'están', 'soy', 'eres', 'es', 'somos', 'son',
        'tengo', 'tienes', 'tiene', 'tenemos', 'tienen', 'tuviste', 'tuvo',
        'hago', 'haces', 'hace', 'hacemos', 'hacen', 'hice', 'hiciste',
        'voy', 'vas', 'va', 'vamos', 'van', 'fui', 'fuiste', 'fue',
        'quiero', 'quieres', 'quiere', 'queremos', 'quieren', 'quería',
        'puedo', 'puedes', 'puede', 'podemos', 'pueden', 'podía',
        'sé', 'sabes', 'sabe', 'sabemos', 'saben', 'sabía',
        'digo', 'dices', 'dice', 'decimos', 'dicen', 'decía',
        # Pronombres y artículos
        'yo', 'tú', 'él', 'ella', 'nosotros', 'nosotras', 'vosotros', 'vosotras', 'ellos', 'ellas',
        'me', 'te', 'se', 'nos', 'os', 'le', 'les', 'lo', 'la', 'los', 'las',
        'al', 'del', 'un', 'uno', 'una', 'unos', 'unas',
        # Palabras básicas de sentimiento en español
        'contento', 'feliz', 'alegre', 'triste', 'enfadado', 'muy', 'bien', 'mal'
    }
    
    words = text_lower.split()
    spanish_word_count = sum(1 for word in words if word in spanish_common_words)
    
    # Si más del 20% de las palabras son comunes en español, asumir español
    # (bajado del 30% para ser más permisivo con frases cortas)
    if len(words) > 0 and spanish_word_count / len(words) > 0.2:
        return True
    
    # Si hay al menos una palabra de español en frases cortas (menos de 5 palabras)
    if len(words) <= 5 and spanish_word_count > 0:
        return True
    
    return False

def analyze_spanish_sentiment(text):
    """
    Análisis de sentimiento básico para español usando diccionario de palabras.
    """
    text_lower = text.lower()
    words = text_lower.split()
    
    positive_count = sum(1 for word in words if word in positive_words_es)
    negative_count = sum(1 for word in words if word in negative_words_es)
    
    # Calcular polaridad básica
    total_words = len(words)
    if total_words == 0:
        return 0.0, 0.0
    
    if positive_count > negative_count:
        polarity = min(0.8, (positive_count - negative_count) / max(1, total_words) * 2)
    elif negative_count > positive_count:
        polarity = max(-0.8, -(negative_count - positive_count) / max(1, total_words) * 2)
    else:
        polarity = 0.0
    
    # Subjetividad simple (basada en palabras emocionales)
    emotional_words = positive_count + negative_count
    subjectivity = min(1.0, emotional_words / max(1, total_words) * 1.5)
    
    return polarity, subjectivity



def detect_and_translate(text):
    """
    Detecta el idioma del texto y lo traduce si es necesario.
    Devuelve el texto traducido y el idioma detectado.
    """
    if not text or not str(text).strip():
        return text, "unknown"
    
    text = str(text)
    
    # Usar detección simple de español
    is_spanish = detect_spanish_simple(text)
    
    if is_spanish:
        return text, "es"
    else:
        # Asumir que es inglés u otro idioma que TextBlob puede manejar
        return text, "en"




def predict_sentiment(text, target_lang='es'):

    if not text or not str(text).strip():
        return None

    text = str(text)

   
    detected_lang = "en"  
    is_spanish = detect_spanish_simple(text)
    
    if is_spanish:
        detected_lang = "es"
       
        polarity, subjectivity = analyze_spanish_sentiment(text)
        translated_text = None
    else:
        
        detected_lang = "en"
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        translated_text = None

    if polarity > 0.1:
        sentiment = "Positivo" if target_lang == 'es' else "Positive"
        emoji = "😊"

    elif polarity < -0.1:
        sentiment = "Negativo" if target_lang == 'es' else "Negative"
        emoji = "😞"

    else:
        sentiment = "Neutral" if target_lang == 'es' else "Neutral"
        emoji = "😐"

    return {
        "sentiment": sentiment,
        "emoji": emoji,
        "polarity": polarity,
        "subjectivity": subjectivity,
        "detected_lang": detected_lang,
        "translated_text": translated_text
    }




st.markdown(
    "<h1>🧠 Sentiment AI</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "Análisis inteligente de comentarios mediante procesamiento de texto. Soporta múltiples idiomas con traducción automática.",
)

st.write("")




st.header("💬 Analizar un comentario")

with st.container(border=True):

    user_text = st.text_area(
        "Escribe el comentario",
        placeholder="Ejemplo: La aplicación funciona excelente...",
        height=130
    )


if user_text.strip():

    result = predict_sentiment(user_text)

    st.write("")

    # Resultado
    col1, col2 = st.columns([1, 4])

    with col1:
        st.markdown(
            f"<div style='font-size:55px;text-align:center;'>{result['emoji']}</div>",
            unsafe_allow_html=True
        )

    with col2:

        if result["sentiment"] == "Positivo":
            st.success("POSITIVO")

        elif result["sentiment"] == "Negativo":
            st.error("NEGATIVO")

        else:
            st.info("NEUTRAL")

    # Mostrar información de idioma detectado
    if result.get('detected_lang'):
        lang_name = "Español" if result['detected_lang'] == 'es' else "Inglés"
        st.info(f"🌍 Idioma detectado: {lang_name}")

    st.write("")

    # Métricas
    m1, m2 = st.columns(2)

    with m1:

        st.metric(
            "Polaridad",
            f"{result['polarity']:.3f}"
        )

        progress = (result["polarity"] + 1) / 2

        st.progress(
            progress
        )

        st.caption(
            "Negativo ← Polaridad → Positivo"
        )


    with m2:

        st.metric(
            "Subjetividad",
            f"{result['subjectivity']:.3f}"
        )

        st.progress(
            result["subjectivity"]
        )

        st.caption(
            "Objetivo ← Subjetividad → Subjetivo"
        )




st.divider()

st.header("📁 Analizar varios comentarios")

st.write(
    "Carga un archivo CSV para analizar automáticamente un conjunto de comentarios."
)

archivo = st.file_uploader(
    "Selecciona tu archivo CSV",
    type=["csv"]
)


if archivo is not None:

    try:

        df = pd.read_csv(archivo)

        st.success(
            f"Archivo cargado correctamente · {len(df)} comentarios"
        )

        st.subheader("Vista previa")

        st.dataframe(
            df,
            use_container_width=True
        )

        columna = st.selectbox(
            "Selecciona la columna que contiene los comentarios:",
            df.columns
        )

        if st.button(
            "Analizar comentarios"
        ):

            resultados = []

            for comentario in df[columna]:

                resultado = predict_sentiment(
                    comentario
                )

                if resultado:

                    resultados.append(resultado)

                else:

                    resultados.append({
                        "sentiment": "Neutral",
                        "emoji": "😐",
                        "polarity": 0,
                        "subjectivity": 0,
                        "detected_lang": "unknown",
                        "translated_text": None
                    })


            

            df["Sentimiento"] = [
                r["sentiment"]
                for r in resultados
            ]

            df["Polaridad"] = [
                r["polarity"]
                for r in resultados
            ]

            df["Subjetividad"] = [
                r["subjectivity"]
                for r in resultados
            ]

            df["Idioma Detectado"] = [
                r["detected_lang"]
                for r in resultados
            ]

            df["Texto Traducido"] = [
                r["translated_text"] if r["translated_text"] else "No requerido"
                for r in resultados
            ]


           

            positivos = sum(
                df["Sentimiento"] == "Positivo"
            )

            negativos = sum(
                df["Sentimiento"] == "Negativo"
            )

            neutrales = sum(
                df["Sentimiento"] == "Neutral"
            )


            st.subheader("Resumen")

            c1, c2, c3 = st.columns(3)

            with c1:
                st.metric(
                    "😊 Positivos",
                    positivos
                )

            with c2:
                st.metric(
                    "😞 Negativos",
                    negativos
                )

            with c3:
                st.metric(
                    "😐 Neutrales",
                    neutrales
                )


            

            st.subheader("Resultados")

            st.dataframe(
                df,
                use_container_width=True
            )


           

            st.subheader("📊 Análisis visual de sentimientos")

            
            col_graficos1, col_graficos2 = st.columns(2)

            with col_graficos1:
                datos = pd.DataFrame({
                    "Sentimiento": [
                        "Positivo",
                        "Negativo",
                        "Neutral"
                    ],
                    "Cantidad": [
                        positivos,
                        negativos,
                        neutrales
                    ]
                })

                fig, ax = plt.subplots(figsize=(8, 5))
                fig.patch.set_facecolor("#0f172a")
                ax.set_facecolor("#0f172a")

               
                colors = ['#00d4ff', '#ef4444', '#7dd3fc']
                bars = ax.bar(
                    datos["Sentimiento"],
                    datos["Cantidad"],
                    color=colors,
                    edgecolor='#334155',
                    linewidth=2,
                    alpha=0.9
                )

                ax.set_title(
                    "Comentarios por sentimiento",
                    color="#00d4ff",
                    fontsize=14,
                    fontweight='bold',
                    pad=15
                )

                ax.set_xlabel(
                    "Sentimiento",
                    color="#94a3b8",
                    fontsize=11
                )

                ax.set_ylabel(
                    "Cantidad",
                    color="#94a3b8",
                    fontsize=11
                )

                ax.tick_params(
                    colors="#94a3b8",
                    labelsize=10
                )

                for spine in ax.spines.values():
                    spine.set_color("#334155")
                    spine.set_linewidth(1.5)

               
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height,
                           f'{int(height)}',
                           ha='center', va='bottom',
                           color='#00d4ff',
                           fontsize=11,
                           fontweight='bold')

                plt.tight_layout()
                st.pyplot(fig)

            with col_graficos2:
                if sum([
                    positivos,
                    negativos,
                    neutrales
                ]) > 0:

                    fig2, ax2 = plt.subplots(figsize=(8, 5))
                    fig2.patch.set_facecolor("#0f172a")
                    ax2.set_facecolor("#0f172a")

                   
                    colors = ['#00d4ff', '#ef4444', '#7dd3fc']
                    explode = (0.05, 0.05, 0.05)

                    wedges, texts, autotexts = ax2.pie(
                        [
                            positivos,
                            negativos,
                            neutrales
                        ],
                        labels=[
                            "Positivos",
                            "Negativos",
                            "Neutrales"
                        ],
                        autopct="%1.1f%%",
                        startangle=90,
                        colors=colors,
                        explode=explode,
                        textprops={
                            "color": "#e8e8e8",
                            "fontsize": 10,
                            "fontweight": "bold"
                        },
                        wedgeprops={
                            "edgecolor": "#334155",
                            "linewidth": 2
                        }
                    )

                    ax2.set_title(
                        "Distribución porcentual",
                        color="#00d4ff",
                        fontsize=14,
                        fontweight='bold',
                        pad=15
                    )

                    # Mejorar el aspecto de los porcentajes
                    for autotext in autotexts:
                        autotext.set_color("#00d4ff")
                        autotext.set_fontsize(11)
                        autotext.set_fontweight('bold')

                    plt.tight_layout()
                    st.pyplot(fig2)


    

            st.subheader("⬇️ Descargar resultados")

            csv = df.to_csv(
                index=False
            ).encode("utf-8-sig")

            st.download_button(
                "Descargar resultados CSV",
                csv,
                "resultados_sentimiento.csv",
                "text/csv",
                use_container_width=True
            )


    except Exception as e:

        st.error(
            f"Error al procesar el archivo: {e}"
        )




st.markdown("""
<div class="footer">

    <div class="footer-title">
        🧠 Sentiment AI
    </div>

    <div class="footer-text">
        Integrantes: Jose Daniel Salas  · Jonathan Cristian Constanza 
    </div>

    <div class="footer-course">
        Sistema Experto
    </div>

</div>
""", unsafe_allow_html=True)


### 👥 Para el pie de página