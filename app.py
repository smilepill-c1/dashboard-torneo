import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
import os

# Configuración de la página
st.set_page_config(page_title="⚽ Líderes de Torneo Mundialista", layout="wide", page_icon="⚽")

# Inyectar fuentes y estilos CSS de cápsula premium (Prompt_HTML.txt) y temática futbolística
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&family=Syncopate:wght@400;700&display=swap');
    
    /* Configurar tipografía global */
    html, body, [class*="css"], .stApp {
        font-family: 'Poppins', sans-serif;
        background: radial-gradient(circle at center, #2e1154 0%, #1a0b2e 70%, #0d0418 100%);
        color: #ffffff;
    }
    
    /* Título Principal Estilo Syncopate Bold */
    .main-header {
        font-family: 'Syncopate', sans-serif;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        font-size: 2.4rem;
        background: linear-gradient(135deg, #FF0080 0%, #8B00FF 50%, #00D4FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-top: 10px;
        margin-bottom: 5px;
        text-shadow: 0px 0px 25px rgba(255, 0, 128, 0.25);
    }
    
    .sub-header {
        font-family: 'Poppins', sans-serif;
        font-weight: 300;
        font-size: 1.1rem;
        color: #00D4FF;
        text-align: center;
        margin-bottom: 25px;
        letter-spacing: 0.05em;
    }
    
    /* Línea divisoria gradiente estilo Prompt_HTML */
    .gradient-divider {
        height: 3px;
        background: linear-gradient(90deg, #FF0080 0%, #8B00FF 50%, #00D4FF 100%);
        border-radius: 2px;
        margin: 25px 0;
        box-shadow: 0px 0px 10px rgba(139, 0, 255, 0.5);
    }
    
    /* Tarjetas de líderes premium */
    .leader-card {
        background: linear-gradient(135deg, rgba(26, 11, 46, 0.75), rgba(13, 4, 24, 0.9));
        border: 1px solid rgba(0, 212, 255, 0.15);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(139, 0, 255, 0.12);
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
        background: linear-gradient(90deg, #FF0080, #8B00FF, #00D4FF);
    }
    .leader-card:hover {
        transform: translateY(-4px);
        border-color: rgba(255, 0, 128, 0.5);
        box-shadow: 0 12px 40px 0 rgba(255, 0, 128, 0.25);
    }
    .leader-title {
        font-family: 'Syncopate', sans-serif;
        font-weight: 700;
        color: #00D4FF;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 8px;
    }
    .leader-team {
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        color: #ffffff;
        font-size: 1.2rem;
        margin: 4px 0;
    }
    .leader-points {
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        color: #FF0080;
        font-size: 1.1rem;
        margin-top: 6px;
        text-shadow: 0 0 10px rgba(255, 0, 128, 0.3);
    }
    
    /* Configuración de Pestañas (Tabs) Estilo Cápsula */
    button[data-baseweb="tab"] {
        font-family: 'Syncopate', sans-serif !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        font-size: 0.8rem !important;
        color: #a78bfa !important;
        border-bottom: 2px solid transparent !important;
        transition: all 0.3s ease-in-out !important;
        background: rgba(26, 11, 46, 0.4) !important;
        border-radius: 8px 8px 0 0 !important;
        margin-right: 6px !important;
        padding: 12px 22px !important;
        border: 1px solid rgba(139, 0, 255, 0.1) !important;
    }
    button[data-baseweb="tab"]:hover {
        color: #00D4FF !important;
        background: rgba(255, 255, 255, 0.05) !important;
        border-color: rgba(0, 212, 255, 0.3) !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #ffffff !important;
        border-bottom: 3px solid #FF0080 !important;
        background: rgba(139, 0, 255, 0.25) !important;
        box-shadow: 0px 4px 20px rgba(255, 0, 128, 0.3) !important;
        border-color: rgba(255, 0, 128, 0.3) !important;
    }
    
    /* Estilo de Formulario y Entradas */
    .stForm {
        background: rgba(26, 11, 46, 0.65) !important;
        border: 1px solid rgba(139, 0, 255, 0.2) !important;
        border-radius: 16px !important;
        padding: 24px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important;
    }
    div[data-baseweb="select"], input, .stNumberInput input {
        background-color: rgba(13, 4, 24, 0.8) !important;
        color: #ffffff !important;
        border: 1px solid rgba(0, 212, 255, 0.2) !important;
        border-radius: 8px !important;
    }
    .stButton button {
        background: linear-gradient(135deg, #FF0080 0%, #8B00FF 100%) !important;
        color: white !important;
        border: none !important;
        font-family: 'Syncopate', sans-serif !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        transition: all 0.3s ease-in-out !important;
        box-shadow: 0 4px 15px rgba(255, 0, 128, 0.3) !important;
    }
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(255, 0, 128, 0.5) !important;
        background: linear-gradient(135deg, #FF0080 0%, #00D4FF 100%) !important;
    }
</style>
""", unsafe_allow_html=True)

# Títulos Principales de Portada
st.markdown('<div class="main-header">🏆 Líderes de Torneo Mundialista ⚽</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Estética Premium de Cápsula | Marcadores y Estadísticas Oficiales</div>', unsafe_allow_html=True)
st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

# ----------------------------------------------------
# 1. CARGA Y PREPARACIÓN DE DATOS BASE (MARZO / ABRIL)
# ----------------------------------------------------
@st.cache_data
def cargar_datos_base():
    # Cargamos el archivo de Excel original (Solo como historial)
    df = pd.read_excel("Tabla de Puntos.xlsx", header=None)
    
    # Tomamos solo las filas de datos y estrictamente las primeras 15 columnas (Marzo y Abril)
    df_clean = df.iloc[2:, :15].copy()
    
    # Asignar nombres exactos a esas 15 columnas históricas
    df_clean.columns = [
        'SEDE', 'Numero', 'Equipo',
        'P. Porra Marzo', 'P. Actv.1 Marzo', 'P. Act. 3 Marzo', 'P. Act. 2 Slido Marzo', 'Penalizacion Marzo', 'Extras Marzo', 'Total puntos Marzo',
        'P. Porra Abril', 'P. Actv.1 Abril', 'P. Act. 2 Slido Abril', 'P. Act. 3 Abril', 'Total puntos Abril'
    ]
    
    # Limpiar nombres de Sedes para corregir codificación
    df_clean['SEDE'] = df_clean['SEDE'].astype(str).str.replace('MAZATLN', 'MAZATLÁN')
    df_clean['SEDE'] = df_clean['SEDE'].str.replace('MAZATL\ufffdN', 'MAZATLÁN')
    df_clean['SEDE'] = df_clean['SEDE'].str.strip()
    df_clean['Equipo'] = df_clean['Equipo'].astype(str).str.strip()
    
    # Convertir a numérico todas las columnas numéricas
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
# 3. CONEXIÓN A BASE DE DATOS (GOOGLE SHEETS / LOCAL)
# ----------------------------------------------------
usa_gsheets = False
conn = None

# Intentamos conectar a Google Sheets.
# Si no está configurado en st.secrets, usamos el backup local de la cápsula.
try:
    if "gsheets" in st.secrets:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df_mayo = conn.read(worksheet="Mayo", ttl=2)
        usa_gsheets = True
    else:
        raise Exception("No configurado")
except Exception as e:
    archivo_local = "Puntos_Mayo_Local.xlsx"
    if os.path.exists(archivo_local):
        df_mayo = pd.read_excel(archivo_local)
    else:
        # Inicializar archivo vacío con los equipos del excel base
        df_mayo = df_base[['SEDE', 'Equipo']].copy()
        df_mayo['P. Porra Mayo'] = 0.0
        df_mayo['P. Actv.1 Mayo'] = 0.0
        df_mayo['P. Act 2 Slido Mayo'] = 0.0
        df_mayo['P. Act 3 Mayo'] = 0.0
        df_mayo.to_excel(archivo_local, index=False)

# Asegurar tipos y columnas requeridas en los datos de Mayo
columnas_mayo = ['P. Porra Mayo', 'P. Actv.1 Mayo', 'P. Act 2 Slido Mayo', 'P. Act 3 Mayo']
for col in columnas_mayo:
    if col not in df_mayo.columns:
        df_mayo[col] = 0.0
    df_mayo[col] = pd.to_numeric(df_mayo[col], errors='coerce').fillna(0.0)

# Calcular total de Mayo
df_mayo['Total Mayo'] = df_mayo[columnas_mayo].sum(axis=1)

# Asegurar limpieza de Sede y Equipo en df_mayo
df_mayo['SEDE'] = df_mayo['SEDE'].astype(str).str.replace('MAZATLN', 'MAZATLÁN').str.replace('MAZATL\ufffdN', 'MAZATLÁN').str.strip()
df_mayo['Equipo'] = df_mayo['Equipo'].astype(str).str.strip()

# Función para guardar datos de Mayo de forma persistente
def guardar_mayo(df):
    if usa_gsheets and conn is not None:
        conn.update(worksheet="Mayo", data=df)
    else:
        df.to_excel("Puntos_Mayo_Local.xlsx", index=False)

# ----------------------------------------------------
# 4. UNIFICACIÓN DE DATOS (CONSOLIDADO)
# ----------------------------------------------------
df_final = pd.merge(
    df_base, 
    df_mayo[['SEDE', 'Equipo', 'P. Porra Mayo', 'P. Actv.1 Mayo', 'P. Act 2 Slido Mayo', 'P. Act 3 Mayo', 'Total Mayo']], 
    on=['SEDE', 'Equipo'], 
    how='outer'
)

# Rellenar valores nulos resultantes del outer join
columnas_numericas_final = [
    'P. Porra Marzo', 'P. Actv.1 Marzo', 'P. Act. 3 Marzo', 'P. Act. 2 Slido Marzo',
    'Penalizacion Marzo', 'Extras Marzo', 'Total puntos Marzo', 'Total puntos Abril',
    'P. Porra Mayo', 'P. Actv.1 Mayo', 'P. Act 2 Slido Mayo', 'P. Act 3 Mayo', 'Total Mayo'
]
for col in columnas_numericas_final:
    df_final[col] = pd.to_numeric(df_final[col], errors='coerce').fillna(0.0)

# Calcular Puntos de Marzo sin Penalizaciones ni Extras
df_final['Total Marzo Sin Penalizaciones'] = (
    df_final['P. Porra Marzo'] + 
    df_final['P. Actv.1 Marzo'] + 
    df_final['P. Act. 3 Marzo'] + 
    df_final['P. Act. 2 Slido Marzo']
)

# Total Acumulado General (Excluye penalización y extras de Marzo de la tabla global)
df_final['Total Acumulado General'] = df_final['Total Marzo Sin Penalizaciones'] + df_final['Total puntos Abril'] + df_final['Total Mayo']
df_final['Total Acumulado General'] = df_final['Total Acumulado General'].round(2)

# Total Acumulado Local (Incluye penalización y extras de Marzo para la vista por Sede)
df_final['Total Acumulado Local'] = df_final['Total puntos Marzo'] + df_final['Total puntos Abril'] + df_final['Total Mayo']
df_final['Total Acumulado Local'] = df_final['Total Acumulado Local'].round(2)

# ----------------------------------------------------
# 5. ESTRUCTURA DE PESTAÑAS (REDEFINIDAS SEGÚN EL FEEDBACK)
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
    st.info("Esta tabla general presenta el **Top 10** de equipos del Torneo Mundialista histórico. Se omiten las columnas de Penalizaciones y Extras para una clasificación global equitativa.")
    
    # Filtrar solo sedes históricas
    df_general = df_final[df_final['SEDE'].isin(sedes_historicas)].copy()
    df_general_sorted = df_general.sort_values(by='Total Acumulado General', ascending=False)
    
    # Líderes por sede histórica en una cuadrícula
    st.markdown("### 🥇 Campeones Proyectados por Confederación (Sede)")
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
    
    # Top 10 Equipos (Solicitado: Presentación del Top 10 ordenado del mejor al último)
    st.markdown("### 📈 Top 10 del Campeonato Mundialista")
    top_10 = df_general_sorted.head(10)
    fig_global = px.bar(
        top_10,
        x='Total Acumulado General',
        y='Equipo',
        color='SEDE',
        orientation='h',
        labels={'Total Acumulado General': 'Puntos Totales (Campaña Mundialista)', 'Equipo': 'Selección / Club'},
        color_discrete_sequence=px.colors.sequential.Sunset_r, # Degradados magenta/naranja premium
        text='Total Acumulado General'
    )
    fig_global.update_layout(
        yaxis={'categoryorder':'total ascending'},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_family="Poppins",
        font_color="#ffffff",
        xaxis=dict(showgrid=False),
        yaxis_gridcolor='rgba(255,255,255,0.05)'
    )
    st.plotly_chart(fig_global, use_container_width=True)
    
    # Tabla General Top 10 Completa
    st.markdown("### 📋 Tabla de Posiciones Oficial - Top 10")
    df_tabla_gen = top_10[['SEDE', 'Equipo', 'Total Marzo Sin Penalizaciones', 'Total puntos Abril', 'Total Mayo', 'Total Acumulado General']].copy()
    df_tabla_gen.columns = ['Confederación / Sede', 'Selección / Club', 'Puntos Marzo (Netos)', 'Puntos Abril', 'Puntos Mayo', 'Total Acumulado']
    st.dataframe(
        df_tabla_gen,
        use_container_width=True,
        hide_index=True
    )

# --- PESTAÑA 2: SEDES LÍDERES ---
with tab2:
    st.subheader("🏟️ Estadio de Puntuaciones por Sede Histórica")
    st.info("En esta visualización de la fase de grupos local, sí se aplican las Penalizaciones y Extras correspondientes.")
    
    sede_sel = st.selectbox("Selecciona el Estadio / Sede a visualizar:", sedes_historicas, key="sede_sel_hist")
    
    df_sede = df_final[df_final['SEDE'] == sede_sel].sort_values(by='Total Acumulado Local', ascending=False)
    
    if not df_sede.empty:
        ganador_row = df_sede.iloc[0]
        nombre_ganador = ganador_row['Equipo']
        puntos_ganador = ganador_row['Total Acumulado Local']
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #FF0080, #8B00FF); padding: 18px; border-radius: 12px; margin-bottom: 20px; color: white; box-shadow: 0px 4px 15px rgba(255, 0, 128, 0.35);">
            <h4 style="margin:0; font-family:'Syncopate', sans-serif; font-size: 1.1rem; text-transform: uppercase; letter-spacing:0.05em;">🏆 Campeón Local de {sede_sel}: <b>{nombre_ganador}</b> con <b>{puntos_ganador} pts</b></h4>
        </div>
        """, unsafe_allow_html=True)
        
        fig = px.bar(
            df_sede,
            x='Total Acumulado Local',
            y='Equipo',
            orientation='h',
            title=f"Marcador Local en {sede_sel}",
            labels={'Total Acumulado Local': 'Puntos de Grupo', 'Equipo': 'Selección'},
            color='Total Acumulado Local',
            color_continuous_scale='Bluered', # Gradientes azul/rojo
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
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### 📋 Tabla de Estadísticas de Grupo")
        df_tabla_sede = df_sede[['Equipo', 'Total puntos Marzo', 'Penalizacion Marzo', 'Extras Marzo', 'Total puntos Abril', 'P. Porra Mayo', 'P. Actv.1 Mayo', 'P. Act 2 Slido Mayo', 'P. Act 3 Mayo', 'Total Mayo', 'Total Acumulado Local']].copy()
        df_tabla_sede.columns = ['Selección / Club', 'Puntos Marzo (Brutos)', '⚠️ Penalización Marzo', '✨ Extras Marzo', 'Puntos Abril', 'Porra Mayo', 'Act 1 Mayo', 'Act 2 Slido Mayo', 'Act 3 Mayo', 'Total Mayo', 'Total Acumulado (Local)']
        st.dataframe(
            df_tabla_sede,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.warning("No hay selecciones registradas en este Estadio.")

# --- PESTAÑA 3: TORNEO LOCAL (SOLO MAYO) ---
with tab3:
    st.subheader("🥅 Marcador de Torneo Local - Sedes Invitadas (Solo Mayo)")
    st.info("Visualización local de las nuevas sedes que ingresaron a participar directamente en la temporada de Mayo.")
    
    # Detectar cuáles sedes de Mayo tienen datos
    sedes_nuevas_con_datos = sorted(df_final[df_final['SEDE'].isin(SEDES_SOLO_MAYO)]['SEDE'].dropna().unique().tolist())
    
    if not sedes_nuevas_con_datos:
        st.info("💡 Aún no se han registrado selecciones para las sedes invitadas de Mayo. Para registrar una y calificarla, ve a la pestaña **Panel de Carga (Staff)**.")
    else:
        sede_sel_nueva = st.selectbox("Selecciona la sede de Torneo Local:", sedes_nuevas_con_datos, key="sede_sel_nueva")
        
        df_sede_nueva = df_final[df_final['SEDE'] == sede_sel_nueva].sort_values(by='Total Mayo', ascending=False)
        
        if not df_sede_nueva.empty:
            ganador_row = df_sede_nueva.iloc[0]
            nombre_ganador = ganador_row['Equipo']
            puntos_ganador = ganador_row['Total Mayo']
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #00D4FF, #8B00FF); padding: 18px; border-radius: 12px; margin-bottom: 20px; color: white; box-shadow: 0px 4px 15px rgba(0, 212, 255, 0.3);">
                <h4 style="margin:0; font-family:'Syncopate', sans-serif; font-size: 1.1rem; text-transform: uppercase; letter-spacing:0.05em;">🏆 Líder del Grupo Local en {sede_sel_nueva}: <b>{nombre_ganador}</b> con <b>{puntos_ganador} pts</b></h4>
            </div>
            """, unsafe_allow_html=True)
            
            fig = px.bar(
                df_sede_nueva,
                x='Total Mayo',
                y='Equipo',
                orientation='h',
                title=f"Standings Temporales de Mayo en {sede_sel_nueva}",
                labels={'Total Mayo': 'Goles / Puntos de Mayo', 'Equipo': 'Selección'},
                color='Total Mayo',
                color_continuous_scale='Electric', # Estética azul-eléctrico a magenta
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
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("### 📋 Marcador de Mayo")
            df_tabla_sede_nueva = df_sede_nueva[['Equipo', 'P. Porra Mayo', 'P. Actv.1 Mayo', 'P. Act 2 Slido Mayo', 'P. Act 3 Mayo', 'Total Mayo']].copy()
            df_tabla_sede_nueva.columns = ['Selección / Club', 'Porra Mayo', 'Act 1 Mayo', 'Act 2 Slido Mayo', 'Act 3 Mayo', 'Total Mayo']
            st.dataframe(
                df_tabla_sede_nueva,
                use_container_width=True,
                hide_index=True
            )

# --- PESTAÑA 4: PANEL DE CARGA (STAFF) ---
with tab4:
    st.subheader("🏁 Mesa de Control y Arbitraje (Staff)")
    
    col_reg, col_pts = st.columns(2)
    
    with col_reg:
        st.markdown("### ✍️ Fichar Nueva Selección")
        st.info("Formulario oficial para registrar una selección en cualquier Estadio para la temporada de Mayo.")
        
        todas_las_sedes = sorted(list(set(sedes_historicas + SEDES_SOLO_MAYO)))
        sede_reg = st.selectbox("1. Selecciona la Sede / Estadio:", todas_las_sedes, key="sede_reg_select")
        nombre_reg = st.text_input("2. Nombre de la Selección / Club:", key="team_reg_input")
        
        if st.button("💾 Fichar Selección", use_container_width=True):
            nombre_reg_clean = nombre_reg.strip()
            if not nombre_reg_clean:
                st.error("Por favor, ingresa un nombre para la selección.")
            else:
                # Comprobar si ya existe en df_mayo
                existe = df_mayo[(df_mayo['SEDE'] == sede_reg) & (df_mayo['Equipo'].str.lower() == nombre_reg_clean.lower())]
                if not existe.empty:
                    st.error(f"La selección '{nombre_reg_clean}' ya está fichada en el Estadio {sede_reg}.")
                else:
                    # Registrar en df_mayo
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
            st.warning("No hay selecciones registradas aún para calificar.")
        else:
            sede_cal = st.selectbox("1. Selecciona el Estadio:", sedes_con_equipos, key="sede_cal_select")
            
            equipos_sede = sorted(df_mayo[df_mayo['SEDE'] == sede_cal]['Equipo'].dropna().unique().tolist())
            equipo_cal = st.selectbox("2. Selecciona la Selección:", equipos_sede, key="equipo_cal_select")
            
            # Obtener valores previos
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
            
            if st.button("💾 Guardar Marcador", use_container_width=True):
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

# Mensaje de conexión en la barra lateral
if not usa_gsheets:
    st.sidebar.warning("⚠️ Modo de Prueba Local de la Cápsula (Puntos_Mayo_Local.xlsx).")
else:
    st.sidebar.success("⚡ Conexión Establecida - Base de Datos (Google Sheets)")