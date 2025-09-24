# app.py
import streamlit as st
from backend.predictor import predict_top_conditions
from backend.triage import assess_urgency
from backend.doctor_finder import get_nearby_doctors
from pathlib import Path
from PIL import Image

# Load CSS
def local_css(file_name):
    css_path = Path(file_name)
    if css_path.exists():
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("assets/style.css")

# Page config
st.set_page_config(page_title="AI Symptom Checker", page_icon="🩺", layout="wide")

# Header
st.markdown("""
<div class="header">
  <div>
    <h1>🩺 AI Symptom Checker</h1>
    <p class="subtitle">Quick triage • Differential diagnosis • Nearby doctors (demo)</p>
  </div>
  <div class="avatar">🤖</div>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("👤 Profile")
    age = st.number_input("Age", min_value=0, max_value=120, value=25)
    gender = st.selectbox("Gender", ["Prefer not to say", "Male", "Female", "Other"])
    medical_history = st.text_area("Medical History (comma separated)", "diabetes, asthma")
    st.markdown("---")
    st.caption("This is a demo — no data leaves this machine.")

# Tabs
tabs = st.tabs(["📝 Symptom Input", "🧪 Analysis", "👨‍⚕️ Doctors & Actions"])

# Initialize session state
if "analyze_pressed" not in st.session_state:
    st.session_state.analyze_pressed = False
    st.session_state.symptoms_text = ""
    st.session_state.body_part = "None"
    st.session_state.top_conditions = []
    st.session_state.urgency = ""
    st.session_state.doctors = []

# ===========================
# Tab 1: Symptom Input
# ===========================
with tabs[0]:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("Describe your symptoms")
        symptoms_text = st.text_area(
            "Type symptoms in plain language (comma separated):",
            "fever, sore throat, cough"
        )
        st.markdown("**Or pick common symptoms:**")
        common = ["fever", "cough", "sore throat", "headache", "chest pain", "shortness of breath", "nausea"]
        selected = st.multiselect("Quick pick", common)
        if selected:
            typed = [s.strip() for s in symptoms_text.split(",") if s.strip()]
            merged = list(dict.fromkeys(typed + selected))
            symptoms_text = ", ".join(merged)
            st.write("Merged symptoms:", symptoms_text)

    with col2:
        st.subheader("Body map")
        # Display image
        try:
            img = Image.open("assets/body_map.png")
            st.image(img, caption="Click the area where you feel pain", use_column_width=True)
        except:
            st.info("Add a `body_map.png` in assets to see the body diagram.")

        # Interactive clickable buttons for body parts
        body_parts = ["Head", "Chest", "Abdomen", "Back", "Left Arm", "Right Arm", "Legs"]
        col_count = 3
        cols = st.columns(col_count)

        selected_body = st.session_state.get("body_part", "None")
        for idx, part in enumerate(body_parts):
            with cols[idx % col_count]:
                if st.button(part):
                    st.session_state.body_part = part
                    selected_body = part

        st.write("Selected body part:", selected_body)

    st.markdown("---")
    analyze_btn = st.button("🔍 Analyze Symptoms")

# ===========================
# Handle Analyze Button Press
# ===========================
if analyze_btn:
    with st.spinner("Analyzing symptoms..."):
        st.session_state.analyze_pressed = True
        st.session_state.symptoms_text = symptoms_text
        st.session_state.top_conditions = predict_top_conditions(symptoms_text, top_n=3)
        st.session_state.urgency = assess_urgency(
            symptoms_text, age=age, medical_history=medical_history, body_part=st.session_state.body_part
        )
        top_condition = st.session_state.top_conditions[0][0] if st.session_state.top_conditions else None
        st.session_state.doctors = get_nearby_doctors(top_condition)

# ===========================
# Tab 2: Analysis
# ===========================
with tabs[1]:
    st.subheader("Analysis")
    if st.session_state.analyze_pressed:
        st.write("### 🔎 Differential diagnosis (top suggestions)")
        if not st.session_state.top_conditions:
            st.warning("No prediction available for the provided input.")
        else:
            for cond, prob in st.session_state.top_conditions:
                percent = f"{prob*100:.1f}%"
                st.write(f"**{cond}** — {percent}")
                st.progress(int(prob * 100))

        st.write("### 🚨 Urgency Assessment")
        urgency = st.session_state.urgency
        if urgency == "home":
            st.success("✅ Likely manageable at home. Monitor symptoms & rest.")
        elif urgency == "doctor":
            st.warning("⚠️ Non-urgent: see a doctor soon if symptoms persist/worsen.")
        elif urgency == "er":
            st.error("🚨 Urgent: seek immediate medical attention / ER.")
        else:
            st.info("No specific urgency flagged. Use judgment & contact a clinician if unsure.")

        st.write("### ℹ️ Notes")
        st.markdown(f"- **Age:** {age}  •  **Gender:** {gender}")
        if medical_history.strip():
            st.markdown(f"- **Medical history:** {medical_history}")
    else:
        st.info("Enter symptoms and click 'Analyze Symptoms' to see results.")

# ===========================
# Tab 3: Doctors & Actions
# ===========================
with tabs[2]:
    st.subheader("Recommendations")
    if st.session_state.analyze_pressed:
        if st.session_state.doctors:
            for d in st.session_state.doctors:
                st.markdown(f"**{d['name']}**  •  {d['specialty']}  •  {d.get('distance','N/A')}")
                if d.get("phone"):
                    st.markdown(f"☎️ {d['phone']}")
                st.markdown("---")
        else:
            st.info("No demo doctor data for the predicted condition. Replace with Google Places API for live locations.")
    else:
        st.info("Analyze symptoms first to see recommended doctors.")
