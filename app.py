import streamlit as st

# --- LÓGICA CLÍNICA INTEGRAL ---
def calcular_analisis_respiratorio(pao2, paco2, spo2, fio2_porcentaje, edad):
    # Constantes a nivel del mar (1 ATM)
    p_atm = 760
    p_h2o = 47
    r = 0.8
    fio2_decimal = fio2_porcentaje / 100
    
    # 1. Cálculos de Presión Alveolar
    pao2_alveolar_actual = (fio2_decimal * (p_atm - p_h2o)) - (paco2 / r)
    pao2_alveolar_21 = (0.21 * (p_atm - p_h2o)) - (paco2 / r)
    
    # 2. Índices de Oxigenación
    pafi = pao2 / fio2_decimal
    spfi = spo2 / fio2_decimal
    indice_aA = pao2 / pao2_alveolar_actual
    
    # 3. Diferenciación (Gradientes)
    gradiente_actual = pao2_alveolar_actual - pao2
    pao2_estimada_21 = pao2_alveolar_21 * indice_aA
    gradiente_21 = pao2_alveolar_21 - pao2_estimada_21
    
    # 4. Valores de Referencia
    gradiente_esperada = (edad / 4) + 4
    
    return {
        "pafi": round(pafi, 1),
        "spfi": round(spfi, 1),
        "indice_aA": round(indice_aA, 2),
        "gradiente_actual": round(gradiente_actual, 1),
        "gradiente_21": round(gradiente_21, 1),
        "gradiente_esperada": round(gradiente_esperada, 1),
        "pao2_estimada_21": round(pao2_estimada_21, 1)
    }

# --- INTERFAZ DE USUARIO (Optimizada para Celular) ---
st.set_page_config(page_title="Monitor Respiratorio", page_icon="🩺")

st.title("🩺 Monitorización de Intercambio Gaseoso")
st.markdown("---")

# Entradas de datos en la pantalla principal
st.subheader("📥 Datos del Paciente")

col1, col2 = st.columns(2)
with col1:
    edad = st.number_input("Edad", min_value=1, max_value=110, value=60)
    pao2 = st.number_input("PaO2 (mmHg)", min_value=20.0, value=85.0)
    paco2 = st.number_input("PaCO2 (mmHg)", min_value=10.0, value=40.0)
with col2:
    fio2_input = st.number_input("FiO2 Actual (%)", min_value=21, max_value=100, value=35)
    spo2 = st.number_input("SpO2 (%)", min_value=50, max_value=100, value=96)

st.write("") # Espacio visual

if st.button("GENERAR DIAGNÓSTICO", type="primary", use_container_width=True):
    res = calcular_analisis_respiratorio(pao2, paco2, spo2, fio2_input, edad)
    
    st.markdown("---")
    
    # --- FILA 1: ÍNDICES DE EFICIENCIA ---
    st.subheader("📊 Índices de Eficiencia")
    c1, c2 = st.columns(2)
    with c1:
        st.metric("PaFi", res['pafi'])
        st.metric("SpFi", res['spfi'])
    with c2:
        st.metric("Índice a/A", res['indice_aA'])
        st.metric("D(A-a)O₂ Actual", f"{res['gradiente_actual']} mmHg")

    st.markdown("---")

    # --- FILA 2: PROYECCIÓN Y GRADIENTE ---
    st.subheader("📉 Proyección a Aire Ambiental (21%)")
    st.info(f"**PaO₂ Proyectada:** {res['pao2_estimada_21']} mmHg")
    st.info(f"**D(A-a)O₂ Proyectada:** {res['gradiente_21']} mmHg")
    st.caption(f"Valor de referencia: D(A-a)O₂ normal para la edad es hasta {res['gradiente_esperada']} mmHg")

    st.markdown("---")

    # --- SECCIÓN DE INTERPRETACIÓN CLÍNICA ---
    st.subheader("🧠 Análisis Clínico")
    
    # 1. Hipoxemia
    if res['pafi'] >= 300:
        st.success("✅ **Oxigenación:** Dentro de límites normales o injuria leve.")
    elif 200 <= res['pafi'] < 300:
        st.warning("⚠️ **Hipoxemia Leve:** Compatible con SDRA Leve (Berlín).")
    elif 100 <= res['pafi'] < 200:
        st.error("🟠 **Hipoxemia Moderada:** Compromiso importante del intercambio.")
    else:
        st.error("🚨 **Hipoxemia Severa:** Criterio de SDRA Severo.")

    # 2. Tipo de Insuficiencia Respiratoria (IRA)
    if paco2 > 45:
        st.error("👉 **IRA Tipo II (Hipercápnica):** Falla de bomba o hipoventilación.")
    elif pao2 < 60:
        st.error("👉 **IRA Tipo I (Hipoxémica):** Falla de parénquima/intercambio.")
    else:
        st.info("👉 Sin criterios de IRA inminente en gasometría actual.")

    # 3. Mecanismo de la Gradiente
    if res['gradiente_actual'] > (res['gradiente_esperada'] + 5):
        st.warning("🔍 **Mecanismo:** Gradiente elevada. Sugiere alteración V/Q, Shunt o defecto de difusión.")
    else:
        st.success("🔍 **Mecanismo:** Gradiente normal. Causas probablemente extrapulmonares.")

