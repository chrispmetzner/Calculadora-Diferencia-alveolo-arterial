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
    # Estimación de PaO2 a 21% usando el índice a/A (estabilidad relativa)
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

# --- INTERFAZ DE USUARIO ---
st.set_page_config(page_title="Monitorización Respiratoria Kine", page_icon="🩺", layout="wide")

st.title("🩺 Monitorización de Intercambio Gaseoso y Oxigenación")
st.markdown("---")

# Entradas de datos
with st.sidebar:
    st.header("📥 Datos del Paciente")
    edad = st.number_input("Edad", min_value=1, max_value=110, value=60)
    st.subheader("Gases Arteriales / Monitor")
    pao2 = st.number_input("PaO2 (mmHg)", min_value=20.0, value=85.0)
    paco2 = st.number_input("PaCO2 (mmHg)", min_value=10.0, value=40.0)
    spo2 = st.number_input("SpO2 (%)", min_value=50, max_value=100, value=96)
    fio2_input = st.number_input("FiO2 Actual (%)", min_value=21, max_value=100, value=35)

if st.button("GENERAR DIAGNÓSTICO CLÍNICO", type="primary"):
    res = calcular_analisis_respiratorio(pao2, paco2, spo2, fio2_input, edad)
    
    # --- FILA 1: ÍNDICES DE EFICIENCIA ---
    st.subheader("📊 Índices de Eficiencia de Oxigenación")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("PaFi", res['pafi'])
    c2.metric("SpFi", res['spfi'])
    c3.metric("Índice a/A", res['indice_aA'])
    c4.metric("D(A-a)O₂ Actual", f"{res['gradiente_actual']} mmHg")

    st.markdown("---")

    # --- FILA 2: PROYECCIÓN Y GRADIENTE ---
    st.subheader("📉 Proyección a Aire Ambiental (FiO₂ 21%)")
    col_a, col_b = st.columns(2)
    with col_a:
        st.write(f"**PaO₂ Proyectada:** {res['pao2_estimada_21']} mmHg")
        st.write(f"**D(A-a)O₂ Proyectada:** {res['gradiente_21']} mmHg")
    with col_b:
        st.write(f"**D(A-a)O₂ Esperada para la edad:** {res['gradiente_esperada']} mmHg")

    st.markdown("---")

    # --- SECCIÓN DE INTERPRETACIÓN CLÍNICA ---
    st.subheader("🧠 Interpretación Clínica")
    
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
    st.write("**Clasificación de IRA:**")
    if paco2 > 45:
        st.error("👉 **IRA Tipo II (Hipercapnica):** Existe falla de bomba o hipoventilación alveolar.")
    elif pao2 < 60:
        st.error("👉 **IRA Tipo I (Hipoxémica):** Existe falla de parénquima/intercambio.")
    else:
        st.info("👉 Sin criterios de IRA inminente en gasometría actual.")

    # 3. Mecanismo de la Gradiente
    if res['gradiente_actual'] > (res['gradiente_esperada'] + 5): # Tolerancia de 5mmHg
        st.warning("🔍 **Mecanismo:** Gradiente elevada. Sugiere alteración V/Q, Shunt o alteración de la difusión.")
    else:
        st.success("🔍 **Mecanismo:** Gradiente normal. Si hay hipoxemia, considere causas extrapulmonares (SNC, debilidad muscular).")

st.caption("Nota: Esta herramienta es un apoyo clínico. Las decisiones deben basarse en la evaluación integral del paciente en la UPC.")
