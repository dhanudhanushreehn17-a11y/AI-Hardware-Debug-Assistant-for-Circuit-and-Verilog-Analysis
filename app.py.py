import streamlit as st
import requests
import base64
from PIL import Image
import io

# ================= CONFIG =================
OPENCODE_API_URL = "http://127.0.0.1:4096"
CIRCUIT_MODEL = "opencode/gpt-5-nano"
VERILOG_MODEL = "opencode/gpt-5-nano"

# ================= API FUNCTION =================
def call_opencode_api(model, prompt):
    try:
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(
            f"{OPENCODE_API_URL}/api/generate",
            json=payload,
            timeout=120
        )

        response.raise_for_status()
        return response.json().get("response", "No response")

    except requests.exceptions.ConnectionError:
        return "❌ Cannot connect to OpenCode server"
    except Exception as e:
        return f"Error: {str(e)}"


# ================= SIDEBAR =================
st.sidebar.title("Navigation")


# define first
analysis_type = st.sidebar.radio(
    "Select Mode",
    ["🏛️ Circuit Analysis", "🧠 Verilog Debugging"]
)

# then use
if analysis_type == "🏛️ Circuit Analysis":
    render_circuit_analysis()
else:
    render_verilog_analysis()
# Connection check
try:
    requests.get(f"{OPENCODE_API_URL}", timeout=2)
    st.sidebar.success("✅ OpenCode Connected")
except:
    st.sidebar.error("⚠️ Cannot connect to OpenCode")

st.sidebar.markdown("---")
st.sidebar.markdown("### Settings")
st.sidebar.markdown(f"Circuit Model: `{CIRCUIT_MODEL}`")
st.sidebar.markdown(f"Verilog Model: `{VERILOG_MODEL}`")


# ================= MAIN TITLE =================
st.title("🔧 AI Hardware Debug Assistant")
st.caption("Intelligent circuit and Verilog debugging powered by local AI")


# ================= CIRCUIT ANALYSIS =================
def render_circuit_analysis():
    st.header("Circuit Fault Detection")

    uploaded_file = st.file_uploader(
        "Upload Circuit Image",
        type=["png", "jpg", "jpeg"]
    )

    context = st.text_area("Additional Context (optional)")

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image")

        if st.button("Analyze Circuit"):
            prompt = f"""
Analyze this circuit and find faults.

Context: {context}

Explain:
1. Observed circuit
2. Likely fault
3. Cause
4. Fix
"""
            result = call_opencode_api(CIRCUIT_MODEL, prompt)

            st.subheader("Analysis Result")
            st.write(result)


# ================= VERILOG DEBUG =================
def render_verilog_analysis():
    st.header("Verilog Debugging")

    code = st.text_area("Enter Verilog Code", height=200)

    if st.button("Analyze Code"):
        prompt = f"""
Analyze this Verilog code, find errors, and correct it:

{code}

Give:
- Errors
- Explanation
- Correct code
"""
        result = call_opencode_api(VERILOG_MODEL, prompt)

        st.subheader("Analysis Result")
        st.write(result)


# ================= ROUTING =================
if analysis_type == "🏛️ Circuit Analysis":
    render_circuit_analysis()
else:
    render_verilog_analysis()