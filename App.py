
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

# ============================================================
# DICCIONARIO DE POLARIDADES (ESPECIFICADO POR EL DOCENTE)
# ============================================================

# Diccionario principal de polaridades con valores entre -1.0 y +1.0
# Organizado para facilitar la adición de nuevas palabras
polaridad_palabras = {
    # PALABRAS POSITIVAS ALTO (+0.9)
    'excelente': 0.9,
    'deliciosa': 0.9,
    'riquísima': 0.9,

    # PALABRAS POSITIVAS MEDIO (+0.7)
    'caliente': 0.7,
    'buena': 0.7,
    'bueno': 0.7,

    # PALABRAS POSITIVAS MODERADO (+0.6)
    'rápido': 0.6,
    'limpio': 0.6,
    'limpia': 0.6,

    # PALABRAS NEGATIVAS MODERADO (-0.5)
    'frío': -0.5,
    'fría': -0.5,
    'aceptable': -0.5,

    # PALABRAS NEGATIVAS MEDIO (-0.6)
    'lento': -0.6,
    'lenta': -0.6,
    'feo': -0.6,
    'fea': -0.6,

    # PALABRAS NEGATIVAS ALTO (-0.7)
    'mala gana': -0.7,
    'sucio': -0.7,
    'sucia': -0.7,

    # PALABRAS NEGATIVAS SEVERO (-0.9)
    'grosero': -0.9,
    'grosera': -0.9,
    'pésimo': -0.9,
    'pésima': -0.9
}

# Sustantivos neutros (valor 0.0) - no aportan carga emocional por sí mismos
sustantivos_neutros = {
    'comida', 'servicio', 'mesero', 'postre', 'ambiente',
    'hamburguesa', 'pizza', 'restaurante', 'local', 'lugar',
    'plato', 'bebida', 'atención', 'precio', 'calidad'
}

# Rangos para clasificación de resultados (basados en escala estándar de -1.0 a +1.0)
# Estos rangos permiten una clasificación detallada del sentimiento
rangos_clasificacion = {
    'muy_positivo': 0.7,      # >= 0.7
    'positivo': 0.3,          # 0.3 a 0.69
    'neutral': -0.3,           # -0.29 a 0.29
    'negativo': -0.7,         # -0.3 a -0.69
    'muy_negativo': -1.0      # <= -0.7
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

# ============================================================
# FUNCIÓN DE ANÁLISIS CON PONDERACIÓN (NUEVA FUNCIONALIDAD)
# ============================================================

def analyze_weighted_sentiment(text):
    """
    Análisis de sentimiento usando ponderación de palabras según diccionario del docente.
    
    Esta función:
    1. Detecta palabras del diccionario de polaridades en el texto
    2. Calcula la ponderación promedio de las palabras detectadas
    3. Clasifica el resultado según los rangos establecidos
    4. Devuelve información detallada del análisis
    
    Args:
        text: Texto a analizar
        
    Returns:
        dict: {
            'ponderacion': float (valor entre -1.0 y +1.0),
            'clasificacion': str (Muy positivo, Positivo, Neutral, Negativo, Muy negativo),
            'palabras_detectadas': list (palabras encontradas con sus valores),
            'total_palabras': int (cantidad de palabras del diccionario encontradas)
        }
    """
    if not text or not str(text).strip():
        return {
            'ponderacion': 0.0,
            'clasificacion': 'Neutral',
            'palabras_detectadas': [],
            'total_palabras': 0
        }
    
    text_lower = text.lower()
    palabras_detectadas = []
    
    # Buscar palabras individuales del diccionario
    for palabra, valor in polaridad_palabras.items():
        if palabra in text_lower:
            palabras_detectadas.append({
                'palabra': palabra,
                'valor': valor
            })
    
    # Si no se encontraron palabras del diccionario, usar análisis tradicional
    if not palabras_detectadas:
        # Usar el análisis existente como respaldo
        polarity, _ = analyze_spanish_sentiment(text)
        clasificacion = clasificar_ponderacion(polarity)
        
        return {
            'ponderacion': polarity,
            'clasificacion': clasificacion,
            'palabras_detectadas': [],
            'total_palabras': 0,
            'metodo': 'tradicional'
        }
    
    # Calcular ponderación promedio de las palabras detectadas
    total_valor = sum(p['valor'] for p in palabras_detectadas)
    ponderacion = total_valor / len(palabras_detectadas)
    
    # Asegurar que el resultado esté en el rango -1.0 a +1.0
    ponderacion = max(-1.0, min(1.0, ponderacion))
    
    # Clasificar según los rangos establecidos
    clasificacion = clasificar_ponderacion(ponderacion)
    
    return {
        'ponderacion': ponderacion,
        'clasificacion': clasificacion,
        'palabras_detectadas': palabras_detectadas,
        'total_palabras': len(palabras_detectadas),
        'metodo': 'ponderacion'
    }

def clasificar_ponderacion(ponderacion):
    """
    Clasifica una ponderación según los rangos establecidos.
    
    Rangos utilizados:
    - Muy positivo: >= 0.7
    - Positivo: 0.3 a 0.69
    - Neutral: -0.29 a 0.29
    - Negativo: -0.3 a -0.69
    - Muy negativo: <= -0.7
    
    Estos rangos se basan en una distribución equilibrada de la escala -1.0 a +1.0,
    permitiendo una clasificación detallada y diferenciada de los sentimientos.
    """
    if ponderacion >= rangos_clasificacion['muy_positivo']:
        return 'Muy positivo'
    elif ponderacion >= rangos_clasificacion['positivo']:
        return 'Positivo'
    elif ponderacion >= rangos_clasificacion['neutral']:
        return 'Neutral'
    elif ponderacion >= rangos_clasificacion['negativo']:
        return 'Negativo'
    else:
        return 'Muy negativo'

def obtener_emoji_clasificacion(clasificacion):
    """
    Devuelve el emoji correspondiente a cada clasificación.
    """
    emojis = {
        'Muy positivo': '🤩',
        'Positivo': '😊',
        'Neutral': '😐',
        'Negativo': '😞',
        'Muy negativo': '😠'
    }
    return emojis.get(clasificacion, '😐')



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
    
    # NUEVO: Análisis con ponderación
    weighted_result = analyze_weighted_sentiment(user_text)

    st.write("")

    # Resultado del análisis tradicional
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

    # Métricas del análisis tradicional
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
    
    # NUEVO: Sección de análisis con ponderación
    st.divider()
    st.subheader("⚖️ Análisis con Ponderación")
    
    # Resultado de ponderación
    col_p1, col_p2 = st.columns([1, 4])
    
    with col_p1:
        emoji_ponderacion = obtener_emoji_clasificacion(weighted_result['clasificacion'])
        st.markdown(
            f"<div style='font-size:55px;text-align:center;'>{emoji_ponderacion}</div>",
            unsafe_allow_html=True
        )
    
    with col_p2:
        if weighted_result['clasificacion'] == 'Muy positivo':
            st.success("MUY POSITIVO")
        elif weighted_result['clasificacion'] == 'Positivo':
            st.success("POSITIVO")
        elif weighted_result['clasificacion'] == 'Negativo':
            st.error("NEGATIVO")
        elif weighted_result['clasificacion'] == 'Muy negativo':
            st.error("MUY NEGATIVO")
        else:
            st.info("NEUTRAL")
    
    st.write("")
    
    # Métricas de ponderación
    mp1, mp2 = st.columns(2)
    
    with mp1:
        st.metric(
            "Ponderación",
            f"{weighted_result['ponderacion']:.3f}"
        )
        
        progress_pond = (weighted_result['ponderacion'] + 1) / 2
        st.progress(progress_pond)
        st.caption("Muy negativo ← Ponderación → Muy positivo")
    
    with mp2:
        st.metric(
            "Palabras detectadas",
            weighted_result['total_palabras']
        )
        st.caption(f"Método: {weighted_result['metodo']}")
    
    # Mostrar palabras detectadas
    if weighted_result['palabras_detectadas']:
        st.write("**Palabras del diccionario detectadas:**")
        for p in weighted_result['palabras_detectadas']:
            valor_color = "🟢" if p['valor'] > 0 else "🔴"
            st.caption(f"{valor_color} '{p['palabra']}' = {p['valor']:.1f}")
    else:
        st.info("No se detectaron palabras del diccionario de polaridades. Se usó análisis tradicional.")




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
            resultados_ponderacion = []

            for comentario in df[columna]:

                resultado = predict_sentiment(
                    comentario
                )
                
                # NUEVO: Análisis con ponderación
                resultado_pond = analyze_weighted_sentiment(comentario)

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
                
                # Agregar resultado de ponderación
                resultados_ponderacion.append(resultado_pond)


            

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
            
            # NUEVO: Agregar columnas de ponderación
            df["Ponderación"] = [
                r["ponderacion"] for r in resultados_ponderacion
            ]
            
            df["Clasificación Ponderada"] = [
                r["clasificacion"] for r in resultados_ponderacion
            ]
            
            df["Palabras Detectadas"] = [
                ", ".join([p["palabra"] for p in r["palabras_detectadas"]]) if r["palabras_detectadas"] else "Ninguna"
                for r in resultados_ponderacion
            ]
            
            df["Método Análisis"] = [
                r["metodo"] for r in resultados_ponderacion
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
            
            # NUEVO: Estadísticas de ponderación
            ponderacion_promedio = df["Ponderación"].mean()
            
            # Contar clasificaciones ponderadas
            muy_positivos = sum(df["Clasificación Ponderada"] == "Muy positivo")
            positivos_pond = sum(df["Clasificación Ponderada"] == "Positivo")
            neutrales_pond = sum(df["Clasificación Ponderada"] == "Neutral")
            negativos_pond = sum(df["Clasificación Ponderada"] == "Negativo")
            muy_negativos = sum(df["Clasificación Ponderada"] == "Muy negativo")
            
            total_comentarios = len(df)
            
            # Calcular porcentajes
            porcentaje_positivos = ((muy_positivos + positivos_pond) / total_comentarios * 100) if total_comentarios > 0 else 0
            porcentaje_neutrales = (neutrales_pond / total_comentarios * 100) if total_comentarios > 0 else 0
            porcentaje_negativos = ((negativos_pond + muy_negativos) / total_comentarios * 100) if total_comentarios > 0 else 0


            st.subheader("Resumen (Análisis Tradicional)")

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
            
            # NUEVO: Resumen de ponderación
            st.subheader("📊 Resumen (Análisis con Ponderación)")
            
            # Primera fila: métricas principales
            cp1, cp2, cp3 = st.columns(3)
            
            with cp1:
                total_positivos_pond = muy_positivos + positivos_pond
                st.metric(
                    "🤩 Positivos",
                    total_positivos_pond,
                    f"{porcentaje_positivos:.1f}%"
                )
            
            with cp2:
                st.metric(
                    "😐 Neutrales",
                    neutrales_pond,
                    f"{porcentaje_neutrales:.1f}%"
                )
            
            with cp3:
                total_negativos_pond = negativos_pond + muy_negativos
                st.metric(
                    "😠 Negativos",
                    total_negativos_pond,
                    f"{porcentaje_negativos:.1f}%"
                )
            
            # Segunda fila: ponderación promedio e interpretación
            cp4, cp5 = st.columns(2)
            
            with cp4:
                st.metric(
                    "⚖️ Ponderación Promedio",
                    f"{ponderacion_promedio:.3f}"
                )
            
            with cp5:
                # Interpretación general basada en ponderación promedio
                if ponderacion_promedio >= 0.5:
                    interpretacion = "🎉 Excelente - Feedback muy positivo"
                    color = "green"
                elif ponderacion_promedio >= 0.2:
                    interpretacion = "👍 Buena - Feedback mayormente positivo"
                    color = "blue"
                elif ponderacion_promedio >= -0.2:
                    interpretacion = "😐 Neutral - Feedback equilibrado"
                    color = "gray"
                elif ponderacion_promedio >= -0.5:
                    interpretacion = "👎 Regular - Feedback mayormente negativo"
                    color = "orange"
                else:
                    interpretacion = "⚠️ Crítica - Feedback muy negativo"
                    color = "red"
                
                st.info(f"**Interpretación:** {interpretacion}")
            
            # Tercera fila: desglose detallado
            st.write("**Desglose detallado por clasificación:**")
            cp6, cp7, cp8, cp9, cp10 = st.columns(5)
            
            with cp6:
                st.metric("🤩 Muy positivo", muy_positivos)
            with cp7:
                st.metric("😊 Positivo", positivos_pond)
            with cp8:
                st.metric("😐 Neutral", neutrales_pond)
            with cp9:
                st.metric("😞 Negativo", negativos_pond)
            with cp10:
                st.metric("😠 Muy negativo", muy_negativos)


            

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
                    "Comentarios por sentimiento (Tradicional)",
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
                        "Distribución porcentual (Tradicional)",
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
            
            # NUEVO: Gráficos de análisis con ponderación
            st.subheader("📈 Análisis visual con ponderación")
            
            col_graficos3, col_graficos4 = st.columns(2)
            
            with col_graficos3:
                datos_pond = pd.DataFrame({
                    "Clasificación": [
                        "Muy positivo",
                        "Positivo", 
                        "Neutral",
                        "Negativo",
                        "Muy negativo"
                    ],
                    "Cantidad": [
                        muy_positivos,
                        positivos_pond,
                        neutrales_pond,
                        negativos_pond,
                        muy_negativos
                    ]
                })
                
                fig3, ax3 = plt.subplots(figsize=(8, 5))
                fig3.patch.set_facecolor("#0f172a")
                ax3.set_facecolor("#0f172a")
                
                # Colores para las 5 categorías
                colors_pond = ['#00ff88', '#00d4ff', '#7dd3fc', '#ff6b6b', '#ef4444']
                bars_pond = ax3.bar(
                    datos_pond["Clasificación"],
                    datos_pond["Cantidad"],
                    color=colors_pond,
                    edgecolor='#334155',
                    linewidth=2,
                    alpha=0.9
                )
                
                ax3.set_title(
                    "Distribución por clasificación ponderada",
                    color="#00d4ff",
                    fontsize=14,
                    fontweight='bold',
                    pad=15
                )
                
                ax3.set_xlabel(
                    "Clasificación",
                    color="#94a3b8",
                    fontsize=11
                )
                
                ax3.set_ylabel(
                    "Cantidad",
                    color="#94a3b8",
                    fontsize=11
                )
                
                ax3.tick_params(
                    colors="#94a3b8",
                    labelsize=9
                )
                
                for spine in ax3.spines.values():
                    spine.set_color("#334155")
                    spine.set_linewidth(1.5)
                
                # Añadir valores sobre las barras
                for bar in bars_pond:
                    height = bar.get_height()
                    if height > 0:
                        ax3.text(bar.get_x() + bar.get_width()/2., height,
                               f'{int(height)}',
                               ha='center', va='bottom',
                               color='#00d4ff',
                               fontsize=10,
                               fontweight='bold')
                
                plt.tight_layout()
                st.pyplot(fig3)
            
            with col_graficos4:
                if total_comentarios > 0:
                    fig4, ax4 = plt.subplots(figsize=(8, 5))
                    fig4.patch.set_facecolor("#0f172a")
                    ax4.set_facecolor("#0f172a")
                    
                    colors_pond = ['#00ff88', '#00d4ff', '#7dd3fc', '#ff6b6b', '#ef4444']
                    explode_pond = (0.05, 0.05, 0.05, 0.05, 0.05)
                    
                    wedges_pond, texts_pond, autotexts_pond = ax4.pie(
                        [muy_positivos, positivos_pond, neutrales_pond, negativos_pond, muy_negativos],
                        labels=["Muy positivo", "Positivo", "Neutral", "Negativo", "Muy negativo"],
                        autopct="%1.1f%%",
                        startangle=90,
                        colors=colors_pond,
                        explode=explode_pond,
                        textprops={
                            "color": "#e8e8e8",
                            "fontsize": 9,
                            "fontweight": "bold"
                        },
                        wedgeprops={
                            "edgecolor": "#334155",
                            "linewidth": 2
                        }
                    )
                    
                    ax4.set_title(
                        "Distribución porcentual ponderada",
                        color="#00d4ff",
                        fontsize=14,
                        fontweight='bold',
                        pad=15
                    )
                    
                    for autotext in autotexts_pond:
                        autotext.set_color("#00d4ff")
                        autotext.set_fontsize(10)
                        autotext.set_fontweight('bold')
                    
                    plt.tight_layout()
                    st.pyplot(fig4)


    

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