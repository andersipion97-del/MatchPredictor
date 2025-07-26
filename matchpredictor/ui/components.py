import streamlit as st

def scoreboard (equipo1, equipo2):
    st.markdown(f"""
    <div style='text-align: center; font-size: 28px; font-weight: bold;'>
        <span style='color: blue;'>{equipo1}</span> VS <span style='color: red;'>{equipo2}</span>
    </div>
    """, unsafe_allow_html=True)
    
def metricas_resumen(resumen, equipo1, equipo2):
    victorias1 = resumen.get(f"Victorias {equipo1}", 0)
    victorias2 = resumen.get(f"Victorias {equipo2}", 0)
    
    color1 = "green" if victorias1 > victorias2 else "gray"
    color2 = "green" if victorias2 > victorias1 else "gray"
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"{equipo1}")
        st.markdown(f"<h3 style='color: {color1};'>Victorias: {victorias1}</h3>", unsafe_allow_html=True)
        st.metric("Goles anotados", resumen.get(f"Goles {equipo1}", 0))
    
    with col2:
        st.subheader(f"{equipo2}")
        st.markdown(f"<h3 style='color: {color2};'>Victorias: {victorias2}</h3>", unsafe_allow_html=True)
        st.metric("Goles anotados", resumen.get(f"Goles {equipo2}", 0))