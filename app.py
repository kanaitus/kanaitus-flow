import streamlit as st
import pandas as pd
import plotly.express as px
import importlib
import sys
import requests
import json
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, f1_score, mean_absolute_error, r2_score
from streamlit_lottie import st_lottie

def load_lottieurl(url: str):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()
    except:
        return None

# Принудительно перезагружаем модуль локализации, чтобы подхватить новые переводы без перезапуска сервера
if 'locales' in sys.modules:
    importlib.reload(sys.modules['locales'])
from locales import get_translator

# Настраиваем конфигурацию страницы
st.set_page_config(page_title="kanaitus-flow", layout="wide", initial_sidebar_state="expanded")

def inject_custom_css(theme):
    toggle_off_bg = '#C7C7CC' if theme == 'light' else '#48484A'
    
    if theme == "light":
        theme_css = """
        /* LIGHT THEME (White-Gold) */
        .stApp, .stApp [data-testid="stAppViewContainer"] {
            background: radial-gradient(circle at 50% 0%, #ffffff 0%, #fdfbf5 60%) !important;
        }
        /* Умный селектор для текста, чтобы не ломать встроенные компоненты (selectbox, buttons и тд) */
        h1, h2, h3, h4, h5, h6, 
        .stMarkdown p, .stMarkdown li,
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] label,
        [data-testid="stMetricLabel"], [data-testid="stWidgetLabel"] p, 
        [data-testid="stRadio"] label, [data-testid="stCheckbox"] label,
        [data-testid="stFileUploader"] p, [data-testid="stFileUploader"] small {
            color: #1c1c1e !important;
        }
        [data-testid="stFileUploaderDropzone"] * {
            color: #1c1c1e !important;
        }
        [data-testid="stFileUploaderDropzone"] button {
            background-color: rgba(0,0,0,0.05) !important;
            border: 1px solid rgba(0,0,0,0.1) !important;
        }
        /* Умная расцветка для текста тумблеров и чекбоксов */
        [data-testid="stToggle"] label p,
        [data-testid="stToggle"] label span,
        [data-testid="stCheckbox"] label p,
        [data-testid="stCheckbox"] label span,
        [data-testid="stToggle"] input:checked ~ div p,
        [data-testid="stCheckbox"] input:checked ~ div p {{
            color: #1c1c1e !important;
            background-color: transparent !important;
            background: none !important;
        }}
        
        [data-testid="stSidebar"] > div:first-child {
            background: rgba(255, 255, 255, 0.7) !important;
            border-right: 1px solid rgba(212, 175, 55, 0.3) !important;
        }
        [data-testid="stFileUploader"], [data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.6) !important;
            border: 1px solid rgba(212, 175, 55, 0.3) !important;
            box-shadow: 0 8px 32px 0 rgba(212, 175, 55, 0.1) !important;
        }
        [data-testid="stDataFrame"] {
            background: rgba(255, 255, 255, 0.9) !important;
        }
        .stTabs [data-baseweb="tab"] {
            color: #666666 !important;
        }
        .stTabs [data-baseweb="tab"]:hover {
            color: #1a1a1a !important;
            background-color: rgba(212, 175, 55, 0.15) !important;
        }
        [data-testid="stMetricValue"] {
            color: #B8860B !important;
            text-shadow: none !important;
        }
        [data-testid="stFileUploader"]:hover, [data-testid="stFileUploader"]:focus-within {
            background: rgba(212, 175, 55, 0.1) !important;
            box-shadow: 0 20px 45px rgba(212, 175, 55, 0.2), inset 0 0 15px rgba(212, 175, 55, 0.05) !important;
        }
        """
    else:
        theme_css = """
        /* DARK THEME */
        .stApp {
            background: radial-gradient(circle at 50% 0%, #1a1500 0%, #0a0a0a 60%) !important;
        }
        [data-testid="stSidebar"] > div:first-child {
            background: rgba(10, 10, 10, 0.4) !important;
            border-right: 1px solid rgba(212, 175, 55, 0.1) !important;
        }
        [data-testid="stFileUploader"], [data-testid="stDataFrame"], [data-testid="stMetric"] {
            background: rgba(20, 20, 20, 0.4) !important;
            border: 1px solid rgba(212, 175, 55, 0.15) !important;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important;
        }
        .stTabs [data-baseweb="tab"]:hover {
            color: #FFFFFF;
            background-color: rgba(212, 175, 55, 0.1);
        }
        [data-testid="stFileUploader"]:hover, [data-testid="stFileUploader"]:focus-within {
            background: rgba(212, 175, 55, 0.12) !important;
            box-shadow: 0 25px 50px rgba(212, 175, 55, 0.2), inset 0 0 25px rgba(212, 175, 55, 0.1) !important;
        }
        [data-testid="stMetricValue"] {
            color: #FFD700 !important;
            text-shadow: 0 0 15px rgba(255, 215, 0, 0.4);
        }
        /* Умная расцветка для текста тумблеров и чекбоксов */
        [data-testid="stToggle"] label p,
        [data-testid="stToggle"] label span,
        [data-testid="stCheckbox"] label p,
        [data-testid="stCheckbox"] label span,
        [data-testid="stToggle"] input:checked ~ div p,
        [data-testid="stCheckbox"] input:checked ~ div p {{
            color: #ffffff !important;
            background-color: transparent !important;
            background: none !important;
        }}
        """

    base_css = f"""
        <style>
        /* Premium Typography & Header */
        .premium-title {{
            font-size: 2.5rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            background: linear-gradient(135deg, #FFD700 0%, #D4AF37 50%, #8B6508 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1.5rem;
        }}
        
        /* iOS 26 Toggles Alignment */
        [data-testid="stToggle"] label,
        [data-testid="stCheckbox"] label {{
            min-height: 40px !important;
            display: flex !important;
            align-items: center !important;
            margin-bottom: 12px !important;
            width: 100% !important;
            cursor: pointer !important;
        }}

        /* Buttons with Shadows */
        .stButton > button {{
            background-color: #D4AF37 !important;
            color: #000000 !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.5rem 1rem !important;
            font-weight: 700 !important;
            transition: all 0.2s ease-in-out !important;
            box-shadow: 0 2px 4px rgba(212, 175, 55, 0.1) !important;
        }}
        .stButton > button:hover {{
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(212, 175, 55, 0.25) !important;
            background-color: #E6C24A !important; 
        }}

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 24px;
            border-bottom: 1px solid #333333;
        }}
        .stTabs [data-baseweb="tab"] {{
            height: 3rem;
            white-space: pre-wrap;
            background-color: transparent;
            border-radius: 8px 8px 0 0;
            gap: 1px;
            padding: 8px 16px;
            color: #888888;
            font-weight: 600;
            transition: all 0.2s ease;
        }}
        .stTabs [aria-selected="true"] {{
            color: #D4AF37 !important;
            border-bottom-color: #D4AF37 !important;
            border-bottom-width: 3px !important;
        }}

        /* Glass Base Common */
        [data-testid="stSidebar"] > div:first-child {{
            backdrop-filter: blur(20px) saturate(180%) !important;
            -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
        }}

        [data-testid="stFileUploader"], [data-testid="stDataFrame"], [data-testid="stMetric"] {{
            backdrop-filter: blur(16px) saturate(200%) !important;
            -webkit-backdrop-filter: blur(16px) saturate(200%) !important;
            transition: all 0.6s cubic-bezier(0.2, 1.2, 0.4, 1) !important;
            border-radius: 16px !important;
        }}

        /* Magnetic Liquid interaction for File Uploader */
        [data-testid="stFileUploader"] {{
            border: 2px dashed rgba(212, 175, 55, 0.4) !important;
            overflow: hidden;
            position: relative;
            border-radius: 20px !important;
        }}
        
        [data-testid="stFileUploaderDropzone"] {{
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 120px;
            background: transparent !important;
            background-color: transparent !important;
        }}
        
        h2, h3, h4 {{
            font-weight: 600 !important;
            letter-spacing: -0.01em !important;
        }}
        
        {theme_css}
        </style>
    """
    st.markdown(base_css, unsafe_allow_html=True)

def remove_outliers_iqr(df):
    numeric_cols = df.select_dtypes(include='number').columns
    initial_shape = df.shape[0]
    if not numeric_cols.empty:
        Q1 = df[numeric_cols].quantile(0.25)
        Q3 = df[numeric_cols].quantile(0.75)
        IQR = Q3 - Q1
        condition = ~((df[numeric_cols] < (Q1 - 1.5 * IQR)) | (df[numeric_cols] > (Q3 + 1.5 * IQR))).any(axis=1)
        df = df[condition]
    return df, initial_shape - df.shape[0]

def generate_notebook_json(history):
    cells = [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# kanaitus-flow Data Analysis\n",
                "This notebook was automatically generated by kanaitus-flow."
            ]
        }
    ]
    for code_snippet in history:
        # Add newlines back to the source array elements
        source_lines = [line + "\n" for line in code_snippet.split('\n')]
        # Remove trailing newline from the last line to be clean
        if source_lines:
            source_lines[-1] = source_lines[-1].rstrip('\n')
        cells.append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": source_lines
        })
    
    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.8.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    return json.dumps(notebook, indent=1)

def process_uploaded_file(uploaded_file, t):
    if uploaded_file is not None:
        if st.session_state.uploaded_filename != uploaded_file.name:
            with st.spinner(t("loading")):
                try:
                    if uploaded_file.name.endswith('.csv'):
                        df = pd.read_csv(uploaded_file)
                        st.session_state.code_history = ["import pandas as pd\nimport numpy as np\n\ndf = pd.read_csv('your_dataset.csv')"]
                    else:
                        df = pd.read_excel(uploaded_file)
                        st.session_state.code_history = ["import pandas as pd\nimport numpy as np\n\ndf = pd.read_excel('your_dataset.xlsx')"]
                    st.session_state.df = df
                    st.session_state.uploaded_filename = uploaded_file.name
                    st.toast(t("file_loaded"), icon="✅")
                    if hasattr(st, 'rerun'):
                        st.rerun()
                    else:
                        st.experimental_rerun()
                except pd.errors.EmptyDataError:
                    st.error(t("file_empty"))
                except pd.errors.ParserError:
                    st.error(t("parse_error"))
                except ValueError as e:
                    st.error(f'{t("format_error")}: {e}')
                except Exception as e:
                    st.error(f'{t("error")}: {e}')

def init_app():
    # Инициализация стейта
    if 'df' not in st.session_state:
        st.session_state.df = None
    if 'uploaded_filename' not in st.session_state:
        st.session_state.uploaded_filename = None
    if 'lang' not in st.session_state:
        st.session_state.lang = 'ru'
    if 'theme' not in st.session_state:
        st.session_state.theme = 'dark'
    if 'code_history' not in st.session_state:
        st.session_state.code_history = []

    render_sidebar()
    inject_custom_css(st.session_state.theme)
    render_main_content()

def render_sidebar():
    with st.sidebar:
        # Выбор языка и темы
        lang_label = "🇬🇧 English" if st.session_state.lang == 'en' else "🇷🇺 Русский"
        is_en = st.toggle(lang_label, value=st.session_state.lang == 'en', key="lang_toggle")
        if is_en != (st.session_state.lang == 'en'):
            st.session_state.lang = 'en' if is_en else 'ru'
            if hasattr(st, 'rerun'):
                st.rerun()
            else:
                st.experimental_rerun()
                
        theme_label = "Светлая тема" if st.session_state.lang == 'ru' else "Light Theme"
        is_light = st.toggle(theme_label, value=st.session_state.theme == 'light', key="theme_toggle")
        if is_light != (st.session_state.theme == 'light'):
            st.session_state.theme = 'light' if is_light else 'dark'
            if hasattr(st, 'rerun'):
                st.rerun()
            else:
                st.experimental_rerun()
                    
        t = get_translator(st.session_state.lang)
        
        st.markdown(f'<h2 style="color: #D4AF37; margin-bottom: 2rem;">{t("sidebar_title")}</h2>', unsafe_allow_html=True)
        
        if st.session_state.df is not None:
            # File Cancel Section
            file_col, cancel_col = st.columns([5, 1])
            with file_col:
                st.markdown(f"📄 **{st.session_state.uploaded_filename}**")
            with cancel_col:
                if st.button("✖", key="cancel_file", help="Удалить файл" if st.session_state.lang == 'ru' else "Remove file"):
                    st.session_state.df = None
                    st.session_state.uploaded_filename = None
                    st.session_state.code_history = []
                    if hasattr(st, 'rerun'):
                        st.rerun()
                    else:
                        st.experimental_rerun()
            
            st.divider()
            st.markdown(t("export"))
            csv = st.session_state.df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label=t("download_csv"),
                data=csv,
                file_name='cleaned_data.csv',
                mime='text/csv',
                use_container_width=True
            )
            
            if st.session_state.code_history:
                nb_json = generate_notebook_json(st.session_state.code_history)
                st.download_button(
                    label=t("export_notebook"),
                    data=nb_json,
                    file_name='kanaitus_analysis.ipynb',
                    mime='application/x-ipynb+json',
                    use_container_width=True
                )
        else:
            msg = "Загрузите файл в главном окне для начала работы." if st.session_state.lang == 'ru' else "Upload a file in the main window to begin."
            st.info(f"👈 {msg}")

def render_main_content():
    t = get_translator(st.session_state.lang)
    
    if st.session_state.df is None:
        st.write("<br><br><br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 4, 1])
        with col2:
            st.write("<br>", unsafe_allow_html=True)
                
            st.markdown(f'<h1 class="premium-title" style="text-align: center; font-size: 4rem;">{t("title")}</h1>', unsafe_allow_html=True)
            subtitle = "Перетащите ваш CSV или Excel файл прямо сюда для начала анализа" if st.session_state.lang == "ru" else "Drag and drop your CSV or Excel file right here to begin analysis"
            st.markdown(f'<p style="text-align: center; color: #888; font-size: 1.2rem; margin-bottom: 3rem;">{subtitle}</p>', unsafe_allow_html=True)
            
            st.markdown("""
                <style>
                [data-testid="stFileUploaderDropzone"] {
                    min-height: 300px !important;
                }
                [data-testid="stFileUploader"] {
                    padding: 2rem !important;
                }
                </style>
            """, unsafe_allow_html=True)
            
            uploaded_file = st.file_uploader("", type=['csv', 'xlsx'], key="main_uploader", label_visibility="collapsed")
            process_uploaded_file(uploaded_file, t)
        return
        
    st.markdown(f'<h1 class="premium-title">{t("title")}</h1>', unsafe_allow_html=True)
    
    df = st.session_state.df
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(t("total_rows"), df.shape[0])
    with col2:
        st.metric(t("total_cols"), df.shape[1])
        
    st.write("") 
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([t("tab_data"), t("tab_viz"), t("tab_viz_manual"), t("tab_eda"), t("tab_ml")])
    
    with tab1:
        st.write(f"### {t('quality_score')}")
        
        # Calculate quality metrics
        total_cells = df.size
        missing_cells = df.isnull().sum().sum()
        duplicates_count = df.duplicated().sum()
        
        quality_score = 100
        if total_cells > 0:
            quality_score -= (missing_cells / total_cells) * 50
            if len(df) > 0:
                quality_score -= (duplicates_count / len(df)) * 50
        quality_score = max(0, min(100, quality_score))
        
        # Display Metrics
        met1, met2, met3 = st.columns(3)
        met1.metric(t("quality_score"), f"{quality_score:.1f}/100")
        met2.metric(t("missing_cells"), f"{missing_cells}")
        met3.metric(t("duplicates_count"), f"{duplicates_count}")
        
        st.write("---")
        
        # Auto-analytics: Correlation Heatmap and Distributions
        numeric_df = df.select_dtypes(include='number')
        if not numeric_df.empty:
            col_heat, col_dist = st.columns([1, 1])
            font_color = "#1a1a1a" if st.session_state.theme == 'light' else "#FFFFFF"
            
            with col_heat:
                st.write(f"#### {t('corr_matrix')}")
                if len(numeric_df.columns) > 1:
                    corr = numeric_df.corr()
                    fig_corr = px.imshow(corr, color_continuous_scale=['#0A0A0A', '#8B6508', '#FFD700'], text_auto=".2f")
                    fig_corr.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color=font_color)
                    st.plotly_chart(fig_corr, use_container_width=True)
                else:
                    st.info("Недостаточно числовых признаков для корреляции." if st.session_state.lang == 'ru' else "Not enough numeric features for correlation.")
                
            with col_dist:
                st.write(f"#### {t('distributions')}")
                # Plot distribution for up to 2 numeric columns
                dist_cols = numeric_df.columns[:2]
                for col in dist_cols:
                    fig_dist = px.histogram(df, x=col, color_discrete_sequence=['#D4AF37'])
                    fig_dist.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color=font_color, height=250, margin=dict(l=20, r=20, t=30, b=20))
                    st.plotly_chart(fig_dist, use_container_width=True)
        else:
            st.info("No numeric columns available for auto-analytics." if st.session_state.lang == 'en' else "Нет числовых колонок для авто-аналитики.")

    with tab2:
        st.write(t("data_cleaning"))
        col_dup, col_na, col_out = st.columns(3)
        
        with col_dup:
            st.markdown("#### 🗑️ Дубликаты" if st.session_state.lang == 'ru' else "#### 🗑️ Duplicates")
            st.write("Удалить полностью дублирующиеся строки." if st.session_state.lang == 'ru' else "Remove completely duplicated rows.")
            if st.button(t("drop_duplicates"), use_container_width=True, key="main_drop_dup"):
                with st.spinner(t("deleting")):
                    initial_rows = st.session_state.df.shape[0]
                    st.session_state.df = st.session_state.df.drop_duplicates()
                    st.session_state.code_history.append("df = df.drop_duplicates()")
                    deleted = initial_rows - st.session_state.df.shape[0]
                st.success(f'{t("duplicates_deleted")}: {deleted}')
                
        with col_na:
            st.markdown("#### ✨ Пропуски" if st.session_state.lang == 'ru' else "#### ✨ Missing Values")
            st.write("Заполнить пустые ячейки средним значением." if st.session_state.lang == 'ru' else "Fill empty cells with mean value.")
            if st.button(t("fill_na"), use_container_width=True, key="main_fill_na"):
                with st.spinner(t("filling")):
                    df = st.session_state.df
                    numeric_cols = df.select_dtypes(include='number').columns
                    if not numeric_cols.empty:
                        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    df = df.fillna("Пропуск" if st.session_state.lang == 'ru' else "Missing")
                    st.session_state.df = df
                    code = "numeric_cols = df.select_dtypes(include='number').columns\ndf[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())\ndf = df.fillna('Missing')"
                    st.session_state.code_history.append(code)
                st.success(t("na_filled"))
                st.balloons()
                
        with col_out:
            st.markdown("#### 🚨 Аномалии" if st.session_state.lang == 'ru' else "#### 🚨 Outliers")
            st.write("Удалить выбросы по методу межквартильного размаха." if st.session_state.lang == 'ru' else "Remove outliers using IQR method.")
            if st.button(t("remove_outliers"), use_container_width=True, key="main_remove_outliers"):
                with st.spinner(t("deleting")):
                    st.session_state.df, removed = remove_outliers_iqr(st.session_state.df)
                    code = "numeric_cols = df.select_dtypes(include='number').columns\nQ1 = df[numeric_cols].quantile(0.25)\nQ3 = df[numeric_cols].quantile(0.75)\nIQR = Q3 - Q1\ncondition = ~((df[numeric_cols] < (Q1 - 1.5 * IQR)) | (df[numeric_cols] > (Q3 + 1.5 * IQR))).any(axis=1)\ndf = df[condition]"
                    st.session_state.code_history.append(code)
                st.success(f'{t("outliers_removed")}: {removed}')
                
        st.write("---")
        st.info("💡 После применения очистки результаты автоматически обновятся на вкладках Дашборд и Визуализация." if st.session_state.lang == 'ru' else "💡 After applying cleaning, results will automatically update in Dashboard and Visualization tabs.")
        
    with tab3:
        st.write(t("viz_settings"))
        columns = df.columns.tolist()
        
        col_type, col_x, col_y, col_c = st.columns(4)
        with col_type:
            plot_type = st.selectbox(t("plot_type"), ["Scatter", "Line", "Bar", "Boxplot", "Histogram", "Correlation Heatmap"])
        with col_x:
            x_col = st.selectbox(t("select_x"), columns)
        with col_y:
            y_options = [t("none")] + columns
            y_col = st.selectbox(t("select_y"), y_options)
            real_y = None if y_col == t("none") else y_col
        with col_c:
            c_options = [t("none")] + columns
            c_col = st.selectbox(t("select_color"), c_options)
            real_c = None if c_col == t("none") else c_col
            
        st.write("---")
        
        try:
            fig = None
            if plot_type == "Scatter":
                fig = px.scatter(df, x=x_col, y=real_y, color=real_c, color_discrete_sequence=['#D4AF37', '#8B6508', '#FFD700', '#E6C24A'])
            elif plot_type == "Line":
                fig = px.line(df, x=x_col, y=real_y, color=real_c, color_discrete_sequence=['#D4AF37', '#8B6508'])
            elif plot_type == "Bar":
                fig = px.bar(df, x=x_col, y=real_y, color=real_c, color_discrete_sequence=['#D4AF37'])
            elif plot_type == "Boxplot":
                fig = px.box(df, x=x_col, y=real_y, color=real_c, color_discrete_sequence=['#D4AF37'])
            elif plot_type == "Histogram":
                fig = px.histogram(df, x=x_col, color=real_c, color_discrete_sequence=['#D4AF37'])
            elif plot_type == "Correlation Heatmap":
                numeric_df = df.select_dtypes(include='number')
                if not numeric_df.empty:
                    corr = numeric_df.corr()
                    fig = px.imshow(corr, color_continuous_scale=['#0A0A0A', '#8B6508', '#FFD700'], text_auto=True)
                else:
                    st.warning("No numeric columns for correlation heatmap." if st.session_state.lang == 'en' else "Нет числовых колонок для матрицы корреляций.")
            
            if fig:
                font_color = "#1a1a1a" if st.session_state.theme == 'light' else "#FFFFFF"
                fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color=font_color)
                st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f'{t("error")}: {e}')

    with tab4:
        st.write(t("dataset_preview"))
        st.dataframe(df.head(50), use_container_width=True)
        
        st.write(t("missing_stats"))
        missing_stats = df.isnull().sum()
        missing_stats = missing_stats[missing_stats > 0]
        
        if missing_stats.empty:
            st.success(t("no_missing"))
        else:
            missing_df = pd.DataFrame({
                t("col_name"): missing_stats.index, 
                t("missing_count"): missing_stats.values
            })
            st.dataframe(missing_df, hide_index=True)
        
        st.write("### Descriptive Statistics" if st.session_state.lang == 'en' else "### Описательная статистика")
        numeric_df_raw = df.select_dtypes(include='number')
        if not numeric_df_raw.empty:
            st.dataframe(numeric_df_raw.describe().T, use_container_width=True)
        else:
            st.info("No numeric columns available." if st.session_state.lang == 'en' else "Нет числовых колонок.")

    with tab5:
        st.write(f"### {t('tab_ml')}")
        
        # Check for NaNs
        if df.isnull().sum().sum() > 0:
            st.warning(t("ml_na_warning"))
        else:
            col_t, col_f = st.columns(2)
            with col_t:
                target_col = st.selectbox(t("ml_target"), [t("none")] + list(df.columns))
            
            if target_col != t("none"):
                features = [c for c in df.columns if c != target_col]
                with col_f:
                    selected_features = st.multiselect(t("ml_features"), features, default=features)
                
                if selected_features:
                    # ML Task type detection
                    is_numeric_target = pd.api.types.is_numeric_dtype(df[target_col])
                    unique_targets = df[target_col].nunique()
                    
                    default_task = "Regression" if is_numeric_target and unique_targets > 10 else "Classification"
                    task_options = [t("ml_classification"), t("ml_regression")]
                    default_index = 0 if default_task == "Classification" else 1
                    
                    st.write("---")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        task_type = st.selectbox(t("ml_task"), task_options, index=default_index)
                    with col2:
                        test_size = st.slider(t("ml_test_size"), 10, 50, 20, 5)
                    with col3:
                        random_state = st.number_input("Random State", value=42)
                        
                    is_classification = (task_type == t("ml_classification"))
                    
                    col_m, col_p = st.columns(2)
                    with col_m:
                        if is_classification:
                            model_name = st.selectbox(t("ml_model"), ["Logistic Regression", "Random Forest", "Decision Tree"])
                        else:
                            model_name = st.selectbox(t("ml_model"), ["Linear Regression", "Random Forest", "Decision Tree"])
                            
                    with col_p:
                        # Model specific params
                        if model_name == "Random Forest":
                            n_estimators = st.slider("n_estimators", 10, 200, 100, 10)
                            max_depth = st.slider("max_depth", 1, 20, 5)
                        elif model_name == "Decision Tree":
                            max_depth = st.slider("max_depth", 1, 20, 5)
                            
                    if st.button(t("ml_train_btn"), use_container_width=True):
                        with st.spinner(t("generating")):
                            try:
                                # Prepare data
                                X = df[selected_features].copy()
                                y = df[target_col].copy()
                                
                                # Encode categorical features
                                encoded = False
                                for col in X.select_dtypes(include=['object', 'category']).columns:
                                    le = LabelEncoder()
                                    X[col] = le.fit_transform(X[col].astype(str))
                                    encoded = True
                                    
                                if not is_numeric_target and is_classification:
                                    le_y = LabelEncoder()
                                    y = le_y.fit_transform(y.astype(str))
                                    
                                if encoded:
                                    st.info(t("ml_encode_warning"))
                                    
                                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size/100.0, random_state=random_state)
                                
                                # Model selection
                                if is_classification:
                                    if model_name == "Logistic Regression":
                                        model = LogisticRegression(random_state=random_state, max_iter=1000)
                                    elif model_name == "Random Forest":
                                        model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=random_state)
                                    else:
                                        model = DecisionTreeClassifier(max_depth=max_depth, random_state=random_state)
                                else:
                                    if model_name == "Linear Regression":
                                        model = LinearRegression()
                                    elif model_name == "Random Forest":
                                        model = RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth, random_state=random_state)
                                    else:
                                        model = DecisionTreeRegressor(max_depth=max_depth, random_state=random_state)
                                        
                                model.fit(X_train, y_train)
                                preds = model.predict(X_test)
                                
                                st.write("---")
                                st.write(f"#### {t('ml_results')}")
                                res1, res2 = st.columns(2)
                                
                                if is_classification:
                                    acc = accuracy_score(y_test, preds)
                                    f1 = f1_score(y_test, preds, average='weighted')
                                    res1.metric(t("ml_accuracy"), f"{acc:.4f}")
                                    res2.metric(t("ml_f1"), f"{f1:.4f}")
                                else:
                                    mae = mean_absolute_error(y_test, preds)
                                    r2 = r2_score(y_test, preds)
                                    res1.metric(t("ml_mae"), f"{mae:.4f}")
                                    res2.metric(t("ml_r2"), f"{r2:.4f}")
                                    
                                # Feature importance
                                if model_name in ["Random Forest", "Decision Tree"]:
                                    st.write(f"#### {t('ml_feature_imp')}")
                                    importances = model.feature_importances_
                                    imp_df = pd.DataFrame({"Feature": X.columns, "Importance": importances}).sort_values(by="Importance", ascending=True)
                                    fig = px.bar(imp_df, x="Importance", y="Feature", orientation='h', color_discrete_sequence=['#D4AF37'])
                                    font_color = "#1a1a1a" if st.session_state.theme == 'light' else "#FFFFFF"
                                    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color=font_color, height=300, margin=dict(l=0, r=0, t=0, b=0))
                                    st.plotly_chart(fig, use_container_width=True)
                            
                            except Exception as e:
                                st.error(f'{t("error")}: {e}')


if __name__ == "__main__":
    init_app()
