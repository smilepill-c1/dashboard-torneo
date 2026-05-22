import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection

# Configuración de la página
st.set_page_config(page_title="Dashboard de Puntos - Torneo", layout="wide", page_icon="🏆")

st.title("🏆 Dashboard de Puntos en Tiempo Real")
st.markdown("Actualizaciones en vivo por sede y carga de actividades de Mayo.")

# ----------------------------------------------------
# 1. CARGA Y PREPARACIÓN DE DATOS BASE
# ----------------------------------------------------
@st.cache_data
def cargar_datos_base():
    # Cargamos el archivo CSV original que proveíste
   df = pd.read_excel("Tabla de Puntos.xlsx", header=None)
    # Limpieza: Fila 1 contiene las cabeceras reales
    df_clean = df.iloc[2:].copy()
    df_clean.columns = df.iloc[1]
    
    # Seleccionar y limpiar solo las columnas clave de Marzo y Abril
    columnas_interes = [
        'SEDE', 'Numero', 'Equipo', 
        'Total puntos Marzo', 'Total puntos Abril'
    ]
    df_base = df_clean[columnas_interes].copy()
    
    # Convertir a numérico lo necesario
    df_base['Total puntos Marzo'] = pd.to_numeric(df_base['Total puntos Marzo'], errors='coerce').fillna(0)
    df_base['Total puntos Abril'] = pd.to_numeric(df_base['Total puntos Abril'], errors='coerce').fillna(0)
    
    return df_base

df_base = cargar_datos_base()

# ----------------------------------------------------
# 2. CONEXIÓN A BASE DE DATOS (GOOGLE SHEETS / LOCAL)
# ----------------------------------------------------
# Intentamos conectar a Google Sheets para tiempo real multi-dispositivo.
# Si no está configurado en los "secrets", usamos un archivo local temporal para pruebas.
usa_gsheets = False
try:
    if "gsheets" in st.secrets:
        conn = st.connection("gsheets", type=GSheetsConnection)
        # Intentamos leer la tabla de Mayo desde Google Sheets
        df_mayo = conn.read(worksheet="Mayo", ttl=5) # ttl=5 hace que refresque cada 5 segundos
        usa_gsheets = True
    else:
        raise Exception("No configurado")
except:
    # Backup Local en caso de estar probando en tu PC sin internet/configuración todavía
    if 'df_mayo_local' not in st.session_state:
        # Crear estructura vacía para Mayo basada en los equipos existentes
        df_mayo_init = df_base[['SEDE', 'Equipo']].copy()
        df_mayo_init['P. Porra Mayo'] = 0.0
        df_mayo_init['P. Act 3 Mayo'] = 0.0
        st.session_state.df_mayo_local = df_mayo_init
    df_mayo = st.session_state.df_mayo_local

# Asegurar tipos numéricos en los datos de Mayo
df_mayo['P. Porra Mayo'] = pd.to_numeric(df_mayo['P. Porra Mayo'], errors='coerce').fillna(0)
df_mayo['P. Act 3 Mayo'] = pd.to_numeric(df_mayo['P. Act 3 Mayo'], errors='coerce').fillna(0)
df_mayo['Total Mayo'] = df_mayo['P. Porra Mayo'] + df_mayo['P. Act 3 Mayo']

# ----------------------------------------------------
# 3. UNIFICACIÓN DE DATOS (CONSOLIDADO)
# ----------------------------------------------------
# Combinamos Marzo/Abril con los datos en tiempo real de Mayo
df_final = pd.merge(df_base, df_mayo[['SEDE', 'Equipo', 'P. Porra Mayo', 'P. Act 3 Mayo', 'Total Mayo']], on=['SEDE', 'Equipo'], how='left')
df_final['Total Acumulado'] = df_final['Total puntos Marzo'] + df_final['Total puntos Abril'] + df_final['Total Mayo']
df_final['Total Acumulado'] = df_final['Total Acumulado'].round(2)

# ----------------------------------------------------
# 4. INTERFAZ EN PESTAÑAS (DASHBOARD vs CARGA)
# ----------------------------------------------------
tab1, tab2 = st.tabs(["📊 Dashboard de Resultados", "📝 Panel de Carga (Staff)"])

with tab1:
    st.subheader("Resultados por Sede")
    
    # Filtro de Sede de acceso rápido
    sedes_disponibles = sorted(df_final['SEDE'].dropna().unique())
    sede_seleccionada = st.selectbox("Selecciona una Sede para ver sus posiciones:", sedes_disponibles)
    
    # Filtrar datos de la sede
    df_sede = df_final[df_final['SEDE'] == sede_seleccionada].sort_values(by='Total Acumulado', ascending=False)
    
    if not df_sede.empty:
        # Identificar Ganador / Líder Actual de la Sede
        ganador_row = df_sede.iloc[0]
        nombre_ganador = ganador_row['Equipo']
        puntos_ganador = ganador_row['Total Acumulado']
        
        # Métrica destacada en un cuadro llamativo
        st.success(f"🏆 **LÍDER ACTUAL EN {sede_seleccionada}:** {nombre_ganador} con **{puntos_ganador} pts**")
        
        # Gráfico interactivo con Plotly
        fig = px.bar(
            df_sede, 
            x='Total Acumulado', 
            y='Equipo', 
            orientation='h',
            title=f"Posiciones Acumuladas en {sede_seleccionada}",
            labels={'Total Acumulado': 'Puntos Totales', 'Equipo': 'Equipo'},
            color='Total Acumulado',
            color_continuous_scale='Viridis',
            text='Total Acumulado'
        )
        fig.update_layout(yaxis={'categoryorder':'total ascending'}) # Ordenar de mayor a menor arriba
        st.plotly_chart(fig, use_container_width=True)
        
        # Tabla detallada para auditoría de los usuarios
        st.markdown("### 📋 Desglose Detallado de Puntos")
        st.dataframe(
            df_sede[['Equipo', 'Total puntos Marzo', 'Total puntos Abril', 'P. Porra Mayo', 'P. Act 3 Mayo', 'Total Mayo', 'Total Acumulado']],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.warning("No hay datos disponibles para esta sede.")

with tab2:
    st.subheader("Formulario de Actualización en Tiempo Real (Mayo)")
    st.info("Nota: Los cambios realizados aquí impactarán el tablero de inmediato para todos los usuarios.")
    
    # Crear formulario dinámico
    with st.form("formulario_carga"):
        sede_form = st.selectbox("1. Selecciona la Sede:", sedes_disponibles, key="sede_f")
        
        # Filtrar los equipos pertenecientes únicamente a esa sede seleccionada
        equipos_sede = df_base[df_base['SEDE'] == sede_form]['Equipo'].unique()
        equipo_form = st.selectbox("2. Selecciona el Equipo:", equipos_sede)
        
        # Obtener valores actuales para mostrarlos por defecto si ya existen
        fila_actual = df_mayo[(df_mayo['SEDE'] == sede_form) & (df_mayo['Equipo'] == equipo_form)]
        porra_prev = float(fila_actual['P. Porra Mayo'].values[0]) if not fila_actual.empty else 0.0
        act3_prev = float(fila_actual['P. Act 3 Mayo'].values[0]) if not fila_actual.empty else 0.0
        
        st.markdown(f"**Modificando puntos para el equipo: `{equipo_form}`**")
        p_porra = st.number_input("Puntos Actividad Porra 1 (Mayo):", min_value=0.0, max_value=100.0, value=porra_prev, step=1.0)
        p_act3 = st.number_input("Puntos Actividad 3 (Mayo):", min_value=0.0, max_value=100.0, value=act3_prev, step=1.0)
        
        boton_guardar = st.form_submit_button("💾 Guardar y Actualizar Puntos")
        
    if boton_guardar:
        # Lógica de guardado
        if usa_gsheets:
            # 1. Caso Producción: Guardar en Google Sheets
            # Buscamos el índice exacto en el DataFrame de Mayo para actualizarlo
            idx = df_mayo[(df_mayo['SEDE'] == sede_form) & (df_mayo['Equipo'] == equipo_form)].index
            if not idx.empty:
                df_mayo.loc[idx, 'P. Porra Mayo'] = p_porra
                df_mayo.loc[idx, 'P. Act 3 Mayo'] = p_act3
                # Subir de vuelta a Google Sheets usando el conector
                conn.update(worksheet="Mayo", data=df_mayo)
                st.balloons()
                st.success(f"¡Datos guardados con éxito en la nube para {equipo_form}!")
                st.rerun()
        else:
            # 2. Caso de Prueba Local (sin Google Sheets configurado)
            idx = st.session_state.df_mayo_local[(st.session_state.df_mayo_local['SEDE'] == sede_form) & (st.session_state.df_mayo_local['Equipo'] == equipo_form)].index
            if not idx.empty:
                st.session_state.df_mayo_local.loc[idx, 'P. Porra Mayo'] = p_porra
                st.session_state.df_mayo_local.loc[idx, 'P. Act 3 Mayo'] = p_act3
                st.balloons()
                st.success(f"¡Modificación guardada localmente para {equipo_form}! (Modo de prueba local)")
                st.rerun()

# Mensaje flotante abajo si está en modo de prueba local
if not usa_gsheets:
    st.sidebar.warning("⚠️ Modo de Prueba Local activado. Para habilitar multi-dispositivo real, conecta tu Google Sheet.")
else:
    st.sidebar.success("⚡ Conectado a la Base de Datos en tiempo real (Google Sheets)")