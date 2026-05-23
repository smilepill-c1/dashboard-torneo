import streamlit as st
import pandas as pd
import plotly.express as px
import subprocess
import os

# Configuración de la página
st.set_page_config(page_title="⚽ Líderes de Torneo Mundialista", layout="wide", page_icon="⚽")

# Inyectar fuentes y estilos CSS de cápsula premium y temática futbolística avanzada
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&family=Syncopate:wght@400;700&display=swap');
    
    /* Configurar tipografía global y fondo estilo estadio nocturno premium */
    html, body, [class*="css"], .stApp {
        font-family: 'Poppins', sans-serif;
        background: radial-gradient(circle at center, #1b4d3e 0%, #0f2b22 60%, #071410 100%);
        color: #ffffff;
    }
    
    /* Título Principal Estilo Syncopate Bold con destellos de neón fútbol */
    .main-header {
        font-family: 'Syncopate', sans-serif;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        font-size: 2.2rem;
        background: linear-gradient(135deg, #00FF87 0%, #60EFFF 50%, #00D4FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        text-shadow: 0px 0px 30px rgba(0, 255, 135, 0.35);
    }
    
    /* Línea divisoria gradiente estilo cancha de fútbol iluminada */
    .gradient-divider {
        height: 4px;
        background: linear-gradient(90deg, transparent 0%, #00FF87 50%, transparent 100%);
        border-radius: 2px;
        margin: 25px 0;
        box-shadow: 0px 0px 15px rgba(0, 255, 135, 0.6);
    }
    
    /* Tarjetas de líderes premium estilo Palco VIP */
    .leader-card {
        background: linear-gradient(135deg, rgba(15, 43, 34, 0.85), rgba(7, 20, 16, 0.95));
        border: 2px solid rgba(0, 255, 135, 0.2);
        border-radius: 16px;
        padding: 22px;
        box-shadow: 0 10px 35px 0 rgba(0, 255, 135, 0.08);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 16px;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    .leader-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #00FF87, #00D4FF);
    }
    .leader-card:hover {
        transform: translateY(-5px);
        border-color: rgba(0, 255, 135, 0.6);
        box-shadow: 0 15px 40px 0 rgba(0, 255, 135, 0.25);
    }
    .leader-title {
        font-family: 'Syncopate', sans-serif;
        font-weight: 700;
        color: #60EFFF;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin-bottom: 10px;
    }
    .leader-team {
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        color: #ffffff;
        font-size: 1.3rem;
        margin: 4px 0;
    }
    .leader-points {
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        color: #00FF87;
        font-size: 1.2rem;
        margin-top: 8px;
        text-shadow: 0 0 12px rgba(0, 255, 135, 0.4);
    }
    
    /* Configuración de Pestañas (Tabs) Estilo Marcador Electrónico */
    button[data-baseweb="tab"] {
        font-family: 'Syncopate', sans-serif !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
        font-size: 0.8rem !important;
        color: #a2c4b9 !important;
        border-bottom: 2px solid transparent !important;
        transition: all 0.3s ease-in-out !important;
        background: rgba(15, 43, 34, 0.5) !important;
        border-radius: 8px 8px 0 0 !important;
        margin-right: 6px !important;
        padding: 14px 24px !important;
        border: 1px solid rgba(0, 255, 135, 0.1) !important;
    }
    button[data-baseweb="tab"]:hover {
        color: #00FF87 !important;
        background: rgba(255, 255, 255, 0.05) !important;
        border-color: rgba(0, 255, 135, 0.3) !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #ffffff !important;
        border-bottom: 3px solid #00FF87 !important;
        background: rgba(0, 255, 135, 0.15) !important;
        box-shadow: 0px 4px 25px rgba(0, 255, 135, 0.2) !important;
        border-color: rgba(0, 255, 135, 0.4) !important;
    }
    
    /* Estilo de Formulario y Entradas del Vestidor */
    .stForm {
        background: rgba(7, 20, 16, 0.75) !important;
        border: 1px solid rgba(0, 255, 135, 0.25) !important;
        border-radius: 16px !important;
        padding: 26px !important;
        box-shadow: 0 10px 35px 0 rgba(0, 0, 0, 0.4) !important;
    }
    div[data-baseweb="select"], input, .stNumberInput input {
        background-color: rgba(5, 12, 10, 0.9) !important;
        color: #ffffff !important;
        border: 1px solid rgba(0, 255, 135, 0.2) !important;
        border-radius: 8px !important;
    }
    .stButton button {
        background: linear-gradient(135deg, #00FF87 0%, #00A352 100%) !important;
        color: #071410 !important;
        border: none !important;
        font-family: 'Syncopate', sans-serif !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
        border-radius: 8px !important;
        padding: 14px 28px !important;
        transition: all 0.3s ease-in-out !important;
        box-shadow: 0 5px 18px rgba(0, 255, 135, 0.3) !important;
    }
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(0, 255, 135, 0.5) !important;
        background: linear-gradient(135deg, #00FF87 0%, #60EFFF 100%) !important;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# VISUALIZACIÓN DE LOGOTIPOS EN ENCABEZADO SIMÉTRICO
# ----------------------------------------------------
col_logo1, col_text, col_logo2 = st.columns([1, 4, 1])

with col_logo1:
    if os.path.exists("SmilePill_All-in_blanco.png"):
        st.image("SmilePill_All-in_blanco.png", width=140)

with col_text:
    st.markdown('<div class="main-header">🏆 Líderes de Torneo Mundialista ⚽</div>', unsafe_allow_html=True)

with col_logo2:
    if os.path.exists("image.png"):
        st.image("image.png", width=140)

st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

# ----------------------------------------------------
# 1. CARGA Y PREPARACIÓN DE DATOS BASE (MARZO / ABRIL)
# ----------------------------------------------------
@st.cache_data
def cargar_datos_base():
    df = pd.read_excel("Tabla de Puntos.xlsx", header=None)
    df_clean = df.iloc[2:, :15].copy()
    
    df_clean.columns = [
        'SEDE', 'Numero', 'Equipo',
        'P. Porra Marzo', 'P. Actv.1 Marzo', 'P. Act. 3 Marzo', 'P. Act. 2 Slido Marzo', 'Penalizacion Marzo', 'Extras Marzo', 'Total puntos Marzo',
        'P. Porra Abril', 'P. Actv.1 Abril', 'P. Act. 2 Slido Abril', 'P. Act. 3 Abril', 'Total puntos Abril'
    ]
    
    df_clean['SEDE'] = df_clean['SEDE'].astype(str).str.replace('MAZATLN', 'MAZATLÁN')
    df_clean['SEDE'] = df_clean['SEDE'].str.replace('MAZATL\ufffdN', 'MAZATLÁN')
    df_clean['SEDE'] = df_clean['SEDE'].str.strip()
    df_clean['Equipo'] = df_clean['Equipo'].astype(str).str.strip()
    
    columnas_numericas = [
        'P. Porra Marzo', 'P. Actv.1 Marzo', 'P. Act. 3 Marzo', 'P. Act. 2 Slido Marzo',
        'Penalizacion Marzo', 'Extras Marzo', 'Total puntos Marzo', 'Total puntos Abril'
    ]
    for col in columnas_numericas:
        df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce').fillna(0.0)
    
    return df_clean

df_base = cargar_datos_base()
sedes_historicas = sorted(df_base['SEDE'].dropna().unique().tolist())

# ----------------------------------------------------
# 2. DEFINICIÓN DE SEDES DE SOLO MAYO
# ----------------------------------------------------
SEDES_SOLO_MAYO = [
    "CHIHUAHUA", "CIUDAD JUÁREZ", "CIUDAD VICTORIA", "CULIACAN", 
    "ENSENADA", "IRAPUATO", "LA PAZ", "LOS MOCHIS", "MATAMOROS", 
    "MONTERREY 1", "MONTERREY 2", "REYNOSA", "SALTILLO", "TAMPICO", "TORREÓN"
]

# ----------------------------------------------------
# 3. BASE DE DATOS INTEGRADA EN REPOSITORIO (SISTEMA AUTÓNOMO)
# ----------------------------------------------------
archivo_persistente = "Puntos_Mayo_Local.xlsx"

if os.path.exists(archivo_persistente):
    df_mayo = pd.read_excel(archivo_persistente)
else:
    df_mayo = df_base[['SEDE', 'Equipo']].copy()
    df_mayo['P. Porra Mayo'] = 0.0
    df_mayo['P. Actv.1 Mayo'] = 0.0
    df_mayo['P. Act 2 Slido Mayo'] = 0.0
    df_mayo['P. Act 3 Mayo'] = 0.0
    df_mayo.to_excel(archivo_persistente, index=False)

columnas_mayo = ['P. Porra Mayo', 'P. Actv.1 Mayo', 'P. Act 2 Slido Mayo', 'P. Act 3 Mayo']
for col in columnas_mayo:
    if col not in df_mayo.columns:
        df_mayo[col] = 0.0
    df_mayo[col] = pd.to_numeric(df_mayo[col], errors='coerce').fillna(0.0)

df_mayo['Total Mayo'] = df_mayo[columnas_mayo].sum(axis=1)
df_mayo['SEDE'] = df_mayo['SEDE'].astype(str).str.replace('MAZATLN', 'MAZATLÁN').str.replace('MAZATL\ufffdN', 'MAZATLÁN').str.strip()
df_mayo['Equipo'] = df_mayo['Equipo'].astype(str).str.strip()

# Función con disparo de comandos Git automáticos para guardar en la nube sin Google Sheets
def guardar_mayo(df):
    df.to_excel(archivo_persistente, index=False)
    try:
        subprocess.run(["git", "config", "user.name", "Mesa Arbitraje App"], check=False)
        subprocess.run(["git", "config", "user.email", "staff@torneo.com"], check=False)
        subprocess.run(["git", "add", archivo_persistente], check=True)
        subprocess.run(["git", "commit", "-m", "⚽ Marcador actualizado por Staff desde Panel Web"], check=True)
        subprocess.run(["git", "push"], check=True)
    except Exception:
        pass # Funciona localmente si no hay conexión git activa

# ----------------------------------------------------
# 4. UNIFICACIÓN DE DATOS (CONSOLIDADO)
# ----------------------------------------------------
df_final = pd.merge(
    df_base, 
    df_mayo[['SEDE', 'Equipo', 'P. Porra Mayo', 'P. Actv.1 Mayo', 'P. Act 2 Slido Mayo', 'P. Act 3 Mayo', 'Total Mayo']], 
    on=['SEDE', 'Equipo'], 
    how='outer'
)

columnas_numericas_final = [
    'P. Porra Marzo', 'P. Actv.1 Marzo', 'P. Act. 3 Marzo', 'P. Act. 2 Slido Marzo',
    'Penalizacion Marzo', 'Extras Marzo', 'Total puntos Marzo', 'Total puntos Abril',
    'P. Porra Mayo', 'P. Actv.1 Mayo', 'P. Act 2 Slido Mayo', 'P. Act 3 Mayo', 'Total Mayo'
]
for col in columnas_numericas_final:
    df_final[col] = pd.to_numeric(df_final[col], errors='coerce').fillna(0.0)

df_final['Total Marzo Sin Penalizaciones'] = (
    df_final['P. Porra Marzo'] + 
    df_final['P. Actv.1 Marzo'] + 
    df_final['P. Act. 3 Marzo'] + 
    df_final['P. Act. 2 Slido Marzo']
)

df_final['Total Acumulado General'] = df_final['Total Marzo Sin Penalizaciones'] + df_final['Total puntos Abril'] + df_final['Total Mayo']
df_final['Total Acumulado General'] = df_final['Total Acumulado General'].round(2)

df_final['Total Acumulado Local'] = df_final['Total puntos Marzo'] + df_final['Total puntos Abril'] + df_final['Total Mayo']
df_final['Total Acumulado Local'] = df_final['Total Acumulado Local'].round(2)

# ----------------------------------------------------
# 5. ESTRUCTURA DE PESTAÑAS
# ----------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "🏆 Líderes de Torneo Mundialista", 
    "🏢 Sedes Líderes", 
    "📅 Torneo Local", 
    "📝 Panel de Carga (Staff)"
])

# --- PESTAÑA 1: LÍDERES DE TORNEO MUNDIALISTA ---
with tab1:
    st.subheader("⚽ Marcador Mundialista - Puntos Netos Acumulados")
    st.info("Esta tabla presenta la clasificación del **Top 5** de escuadras del campeonato histórico. Se omiten penalizaciones de forma equitativa.")
    
    df_general = df_final[df_final['SEDE'].isin(sedes_historicas)].copy()
    df_general_sorted = df_general.sort_values(by='Total Acumulado General', ascending=False)
    
    st.markdown("### 🥇 Líderes Actuales de Grupo")
    columnas_lideres = st.columns(4)
    for idx, sede in enumerate(sedes_historicas):
        df_sede = df_general[df_general['SEDE'] == sede]
        col_idx = idx % 4
        if not df_sede.empty:
            df_sede_sorted = df_sede.sort_values(by='Total Acumulado General', ascending=False)
            lider = df_sede_sorted.iloc[0]
            nombre_lider = lider['Equipo']
            puntos_lider = lider['Total Acumulado General']
            
            with columnas_lideres[col_idx]:
                st.markdown(f"""
                <div class="leader-card">
                    <div class="leader-title">🏟️ {sede}</div>
                    <div class="leader-team">🏃‍♂️ {nombre_lider}</div>
                    <div class="leader-points">🥅 {puntos_lider} Pts</div>
                </div>
                """, unsafe_allow_html=True)
                
    st.write("---")
    
    st.markdown("### 📈 Cuadro de Honor: Top 5 General del Campeonato")
    top_5 = df_general_sorted.drop_duplicates(subset=['SEDE', 'Equipo']).head(5)
    
    fig_global = px.bar(
        top_5,
        x='Total Acumulado General',
        y='Equipo',
        orientation='h',
        labels={'Total Acumulado General': 'Puntos Totales Computados', 'Equipo': 'Club / Selección'},
        color='Total Acumulado General',
        color_continuous_scale='Greens',
        text='Total Acumulado General'
    )
    fig_global.update_layout(
        yaxis={'categoryorder':'total ascending'},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_family="Poppins",
        font_color="#ffffff",
        xaxis=dict(showgrid=False),
        yaxis_gridcolor='rgba(255,255,255,0.05)',
        height=380,
        bargap=0.35
    )
    st.plotly_chart(fig_global, width='stretch')
    
    st.markdown("### 📋 Tabla de Posiciones Oficial - Top 5")
    df_tabla_gen = top_5[['SEDE', 'Equipo', 'Total Marzo Sin Penalizaciones', 'Total puntos Abril', 'Total Mayo', 'Total Acumulado General']].copy()
    df_tabla_gen.columns = ['Sede / Estadio', 'Club / Selección', 'Puntos Marzo (Netos)', 'Puntos Abril', 'Puntos Mayo', 'Marcador Final Acumulado']
    st.dataframe(df_tabla_gen, width='stretch', hide_index=True)

# --- PESTAÑA 2: SEDES LÍDERES ---
with tab2:
    st.subheader("🏟️ Estadísticas por Sede")
    st.info("Análisis de estadísticas grupales con aplicación de bonificaciones y amonestaciones oficiales.")
    
    sede_sel = st.selectbox("Selecciona el Estadio / Sede a visualizar:", sedes_historicas, key="sede_sel_hist")
    df_sede = df_final[df_final['SEDE'] == sede_sel].sort_values(by='Total Acumulado Local', ascending=False)
    
    if not df_sede.empty:
        ganador_row = df_sede.iloc[0]
        nombre_ganador = ganador_row['Equipo']
        puntos_ganador = ganador_row['Total Acumulado Local']
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #00FF87, #00A352); padding: 18px; border-radius: 12px; margin-bottom: 20px; color: #071410; box-shadow: 0px 4px 15px rgba(0, 255, 135, 0.3);">
            <h4 style="margin:0; font-family:'Syncopate', sans-serif; font-size: 1.1rem; text-transform: uppercase; letter-spacing:0.05em;">🏆 Puntero de Grupo de {sede_sel}: <b>{nombre_ganador}</b> con <b>{puntos_ganador} pts</b></h4>
        </div>
        """, unsafe_allow_html=True)
        
        fig = px.bar(
            df_sede,
            x='Total Acumulado Local',
            y='Equipo',
            orientation='h',
            title=f"Marcadores Registrados en {sede_sel}",
            labels={'Total Acumulado Local': 'Puntos Totales Local', 'Equipo': 'Escuadra'},
            color='Total Acumulado Local',
            color_continuous_scale='Mint',
            text='Total Acumulado Local'
        )
        fig.update_layout(
            yaxis={'categoryorder':'total ascending'},
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_family="Poppins",
            font_color="#ffffff",
            xaxis=dict(showgrid=False)
        )
        st.plotly_chart(fig, width='stretch')
        
        st.markdown("### 📋 Tabla de Estadísticas de Grupo")
        df_tabla_sede = df_sede[['Equipo', 'Total puntos Marzo', 'Penalizacion Marzo', 'Extras Marzo', 'Total puntos Abril', 'P. Porra Mayo', 'P. Actv.1 Mayo', 'P. Act 2 Slido Mayo', 'P. Act 3 Mayo', 'Total Mayo', 'Total Acumulado Local']].copy()
        df_tabla_sede.columns = ['Escuadra', 'Marzo (Bruto)', '⚠️ Penalizaciones', '✨ Extras', 'Puntos Abril', 'Porra Mayo', 'Act 1 Mayo', 'Act 2 Mayo', 'Act 3 Mayo', 'Total Mayo', 'Acumulado Local']
        st.dataframe(df_tabla_sede, width='stretch', hide_index=True)
    else:
        st.warning("No hay selecciones registradas en este Estadio.")

# --- PESTAÑA 3: TORNEO LOCAL (SOLO MAYO) ---
with tab3:
    st.subheader("🥅 Torneo Local")
    st.info("Visualización local de las sedes de la temporada de Mayo.")
    
    sede_sel_nueva = st.selectbox("Selecciona la sede de Torneo Local:", sorted(SEDES_SOLO_MAYO), key="sede_sel_nueva")
    df_sede_nueva = df_final[df_final['SEDE'] == sede_sel_nueva].sort_values(by='Total Mayo', ascending=False)
    
    if df_sede_nueva.empty:
        st.warning(f"⚠️ Sin registros oficiales de escuadras en el Estadio **{sede_sel_nueva}**. Utiliza la Mesa de Control para agregarlas.")
    else:
        ganador_row = df_sede_nueva.iloc[0]
        nombre_ganador = ganador_row['Equipo']
        puntos_ganador = ganador_row['Total Mayo']
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #60EFFF, #00D4FF); padding: 18px; border-radius: 12px; margin-bottom: 20px; color: #071410; box-shadow: 0px 4px 15px rgba(96, 239, 255, 0.3);">
            <h4 style="margin:0; font-family:'Syncopate', sans-serif; font-size: 1.1rem; text-transform: uppercase; letter-spacing:0.05em;">🏆 Líder Local del Mes en {sede_sel_nueva}: <b>{nombre_ganador}</b> con <b>{puntos_ganador} pts</b></h4>
        </div>
        """, unsafe_allow_html=True)
        
        fig = px.bar(
            df_sede_nueva,
            x='Total Mayo',
            y='Equipo',
            orientation='h',
            title=f"Standings Vigentes de Mayo en {sede_sel_nueva}",
            labels={'Total Mayo': 'Puntos de Mayo', 'Equipo': 'Escuadra'},
            color='Total Mayo',
            color_continuous_scale='Tealgrn',
            text='Total Mayo'
        )
        fig.update_layout(
            yaxis={'categoryorder':'total ascending'},
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_family="Poppins",
            font_color="#ffffff",
            xaxis=dict(showgrid=False)
        )
        st.plotly_chart(fig, width='stretch')
        
        st.markdown("### 📋 Marcador de Mayo")
        df_tabla_sede_nueva = df_sede_nueva[['Equipo', 'P. Porra Mayo', 'P. Actv.1 Mayo', 'P. Act 2 Slido Mayo', 'P. Act 3 Mayo', 'Total Mayo']].copy()
        df_tabla_sede_nueva.columns = ['Escuadra', 'Porra Mayo', 'Act 1 Mayo', 'Act 2 Mayo', 'Act 3 Mayo', 'Total Mayo']
        st.dataframe(df_tabla_sede_nueva, width='stretch', hide_index=True)

# --- PESTAÑA 4: PANEL DE CARGA (STAFF) ---
with tab4:
    st.subheader("🏁 Mesa de Control y Arbitraje (Staff)")
    col_reg, col_pts = st.columns(2)
    
    with col_reg:
        st.markdown("### ✍️ Fichar Nueva Selección")
        st.info("Formulario para registrar una escuadra en cualquier sede para la temporada.")
        
        todas_las_sedes = sorted(list(set(sedes_historicas + SEDES_SOLO_MAYO)))
        sede_reg = st.selectbox("1. Selecciona la Sede / Estadio:", todas_las_sedes, key="sede_reg_select")
        nombre_reg = st.text_input("2. Nombre de la Selección / Club:", key="team_reg_input")
        
        if st.button("💾 Fichar Selección", width='stretch'):
            nombre_reg_clean = nombre_reg.strip()
            if not nombre_reg_clean:
                st.error("Por favor, ingresa un nombre para la selección.")
            else:
                existe = df_mayo[(df_mayo['SEDE'] == sede_reg) & (df_mayo['Equipo'].str.lower() == nombre_reg_clean.lower())]
                if not existe.empty:
                    st.error(f"La selección '{nombre_reg_clean}' ya está dada de alta en {sede_reg}.")
                else:
                    nuevo_eq = {
                        'SEDE': sede_reg,
                        'Equipo': nombre_reg_clean,
                        'P. Porra Mayo': 0.0,
                        'P. Actv.1 Mayo': 0.0,
                        'P. Act 2 Slido Mayo': 0.0,
                        'P. Act 3 Mayo': 0.0,
                        'Total Mayo': 0.0
                    }
                    df_mayo = pd.concat([df_mayo, pd.DataFrame([nuevo_eq])], ignore_index=True)
                    guardar_mayo(df_mayo)
                    st.balloons()
                    st.success(f"¡Selección '{nombre_reg_clean}' registrada con éxito en {sede_reg}!")
                    st.rerun()
                    
    with col_pts:
        st.markdown("### 📋 Calificar Actividades y Goles")
        sedes_con_equipos = sorted(df_mayo['SEDE'].dropna().unique().tolist())
        
        if not sedes_con_equipos:
            st.warning("Sin escuadras registradas aún para calificar.")
        else:
            sede_cal = st.selectbox("1. Selecciona el Estadio:", sedes_con_equipos, key="sede_cal_select")
            equipos_sede = sorted(df_mayo[df_mayo['SEDE'] == sede_cal]['Equipo'].dropna().unique().tolist())
            equipo_cal = st.selectbox("2. Selecciona la Selección:", equipos_sede, key="equipo_cal_select")
            
            fila_actual = df_mayo[(df_mayo['SEDE'] == sede_cal) & (df_mayo['Equipo'] == equipo_cal)]
            porra_prev = float(fila_actual['P. Porra Mayo'].values[0]) if not fila_actual.empty else 0.0
            actv1_prev = float(fila_actual['P. Actv.1 Mayo'].values[0]) if not fila_actual.empty else 0.0
            act2_prev = float(fila_actual['P. Act 2 Slido Mayo'].values[0]) if not fila_actual.empty else 0.0
            act3_prev = float(fila_actual['P. Act 3 Mayo'].values[0]) if not fila_actual.empty else 0.0
            
            st.markdown(f"Registrando marcador para: **{equipo_cal}** en **{sede_cal}**")
            p_porra = st.number_input("Puntos Porra Mayo (Goles):", min_value=0.0, max_value=100.0, value=porra_prev, step=0.5, key="p_porra_input")
            p_actv1 = st.number_input("Puntos Actividad 1 Mayo (Goles):", min_value=0.0, max_value=100.0, value=actv1_prev, step=0.5, key="p_actv1_input")
            p_act2 = st.number_input("Puntos Actividad 2 Slido Mayo (Opcional):", min_value=0.0, max_value=100.0, value=act2_prev, step=0.5, key="p_act2_input")
            p_act3 = st.number_input("Puntos Actividad 3 Mayo (Goles):", min_value=0.0, max_value=100.0, value=act3_prev, step=0.5, key="p_act3_input")
            
            if st.button("💾 Guardar Marcador", width='stretch'):
                idx = df_mayo[(df_mayo['SEDE'] == sede_cal) & (df_mayo['Equipo'] == equipo_cal)].index
                if not idx.empty:
                    df_mayo.loc[idx, 'P. Porra Mayo'] = p_porra
                    df_mayo.loc[idx, 'P. Actv.1 Mayo'] = p_actv1
                    df_mayo.loc[idx, 'P. Act 2 Slido Mayo'] = p_act2
                    df_mayo.loc[idx, 'P. Act 3 Mayo'] = p_act3
                    df_mayo.loc[idx, 'Total Mayo'] = p_porra + p_actv1 + p_act2 + p_act3
                    guardar_mayo(df_mayo)
                    st.balloons()
                    st.success(f"¡Marcador actualizado con éxito para {equipo_cal}!")
                    st.rerun()

# Barra lateral informativa
st.sidebar.success("⚽ Base de Datos Autónoma Activa (.xlsx integrado)")