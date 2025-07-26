import streamlit as st

def css_claro ():
    return """
        <style>
        body {background-color: #f5f7fa; color: #000; }
        h1, h2, h3 {color: #003366;}
        [data-testid="stMetric"] {
            background: #ffffff;
            border-radius: 10px;
            padding: 10px;
            box-shadow: 0px 2px 4px rgba(0,0,0,0.1);    
        }
        .stTabs [data-baseweb="tab"] {
            font-size: 18px;
            padding: 10px;
            color: #000;
        }
        </style>
"""
def css_oscuro ():
    return """
        <style>
        body {background-color: #1e1e1e; color: #e0e0e0; }
        h1, h2, h3 {color: #f2f2f2;}
        [data-testid="stMetric"] {
            background: #2c2c2c;
            border-radius: 10px;
            padding: 10px;
            box-shadow: 0px 2px 4px rgba(255,255,255,0.1);    
        }
        .stTabs [data-baseweb="tab"] {
            font-size: 18px;
            padding: 10px;
            color: #fff;
        }
        </style>
"""

def load_custom_css(theme="Claro"):
    if theme == "Claro":
        st.markdown(css_claro(), unsafe_allow_html=True)
    else:
        st.markdown(css_oscuro(), unsafe_allow_html=True)