import streamlit as st

# --- LÓGICA MATEMÁTICA ---
def calcular_gradiente(pao2_paciente, paco2_paciente, edad_paciente):
    p_atm = 760
    p_h2o = 47
    fio2 = 0.21
    r = 0.8
    
    pao2_alveolar = (p_atm - p_h2o) * fio2 - (paco2_paciente / r)
    gradiente = pao2_alveolar - pao2_paciente
    gradiente_normal = (edad_paciente / 4) + 4
    
    return pao2_alveolar, gradiente, gradiente_normal

# --- INTERFAZ VISUAL DE LA APP ---
st.set_page_config(page_title="Calculadora A-a", page_icon="🫁")

st.title("🫁 Calculadora Gradiente Alvéolo-Arterial")
st.write("Ingresa los datos de la gasometría en aire ambiente (FiO2 21%)")

# Cajas para ingresar datos
col1, col2 = st.columns(2)
with col1:
    pao2 = st.number_input("PaO2 (mmHg)", min_value=0.0, value=60.0, step=1.0)
with col2:
    paco2 = st.number_input("PaCO2 (mmHg)", min_value=0.0, value=40.0, step=1.0)

edad = st.number_input("Edad del paciente (Años)", min_value=0, value=50, step=1)

# Botón de cálculo
if st.button("Calcular Intercambio Gaseoso", type="primary"):
    alveolar, gradiente, grad_esperada = calcular_gradiente(pao2, paco2, edad)
    
    st.divider()
    
    # Mostrar resultados
    st.subheader("Resultados:")
    st.info(f"**PAO2 (Presión Alveolar):** {round(alveolar, 1)} mmHg")
    
    if gradiente > grad_esperada:
        st.error(f"**Gradiente A-a:** {round(gradiente, 1)} mmHg (Elevada)")
        st.write(f"*(El valor normal esperado para {edad} años es hasta {round(grad_esperada, 1)} mmHg)*")
        st.warning("⚠️ **Interpretación:** Posible alteración intrínseca del pulmón (ej. alteración V/Q, shunt).")
    else:
        st.success(f"**Gradiente A-a:** {round(gradiente, 1)} mmHg (Normal)")
        st.write(f"*(El valor normal esperado para {edad} años es hasta {round(grad_esperada, 1)} mmHg)*")
        st.success("✅ **Interpretación:** Intercambio gaseoso conservado. Si existe hipoxemia, investigar hipoventilación.")
