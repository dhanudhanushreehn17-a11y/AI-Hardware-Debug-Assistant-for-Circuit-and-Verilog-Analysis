"""
AI Hardware Debug Assistant
A Streamlit application for circuit fault detection and Verilog debugging
"""

import streamlit as st
import requests
import base64
import io
from PIL import Image
import os

# Configuration
OPENCODE_API_URL = "http://127.0.0.1:4096"
CIRCUIT_MODEL = "opencode/gpt-5-nano"
VERILOG_MODEL = "opencode/gpt-5-nano"

# System prompts
CIRCUIT_ANALYSIS_PROMPT = """You are an expert electronics engineer with 15+ years of experience in 
analog and digital circuit design, debugging, and fault diagnosis.

Your role is to analyze circuit schematic images provided by users, identify likely faults, 
explain root causes in accessible language, and recommend specific corrective actions.

Guidelines:
1. First, describe what you observe in the circuit schematic (components, connections, topology)
2. Provide diagnosis in this format:
   - **Observed Circuit**: [description of identified components and connections]
   - **Likely Fault**: [concise description]
   - **Probable Cause**: [technical explanation]
   - **Affected Components**: [list with values/positions]
   - **Recommended Fix**: [numbered step-by-step actions]
3. Prioritize the most common faults before rare edge cases
4. Suggest basic measurement techniques to confirm the diagnosis
5. If the schematic image quality is insufficient, specify what additional information or clearer images would help

IMPORTANT: Be concise but thorough. Format your response using markdown for readability."""

VERILOG_ANALYSIS_PROMPT = """You are a senior VLSI design engineer and Verilog expert specializing in 
RTL design, synthesis, and verification.

Your role is to analyze Verilog code provided by users, identify errors across all categories 
(clocking, reset, FSM, syntax, logic), explain each issue clearly, and provide corrected code.

Guidelines:
1. Categorize each error: Clocking / Reset / FSM / Syntax / Logic
2. For each error provide:
   - **Category**: [one of the above]
   - **Issue**: [brief description]
   - **Location**: [approximate line or component]
   - **Explanation**: [why this is an error]
   - **Fix**: [specific change needed]
3. Provide complete corrected module code in Verilog syntax
4. Add inline comments in the corrected code explaining key changes
5. Flag any synthesis warnings or simulation mismatches
6. If code appears functionally correct, state this explicitly

IMPORTANT: Use markdown formatting for headers and code blocks. Wrap code in triple backticks with 'verilog' language tag."""


def call_opencode_api(model: str, prompt: str, image_base64: str = None) -> str:
    """Call OpenCode API for inference"""
    try:
        # Build messages (correct format)
        message_content = prompt

        # (Optional: include image if needed later)
        if image_base64:
            message_content += "\n[Image attached]"

        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": message_content
                }
            ],
            "temperature": 0.3
        }

        response = requests.post(
            f"{OPENCODE_API_URL}/v1/chat/completions",
            json=payload,
            timeout=300
        )

        response.raise_for_status()

        return response.json()["choices"][0]["message"]["content"]

    except requests.exceptions.ConnectionError:
        st.warning("OpenCode server not reachable. Check if it's running.")
        return ""

    except requests.exceptions.Timeout:
        return "Error: Request timed out."

    except Exception as e:
        return f"Error: {str(e)}"
def image_to_base64(image_file) -> str:
    """Convert uploaded image to base64"""
    try:
        img = Image.open(image_file)
        img = img.convert("RGB")
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=85)
        return base64.b64encode(buffer.getvalue()).decode("utf-8")
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        return None


def analyze_circuit(image_file, user_context: str = "") -> str:
    """Analyze circuit from uploaded image"""
    image_base64 = image_to_base64(image_file)
    if not image_base64:
        return "Failed to process image"
    
    prompt = CIRCUIT_ANALYSIS_PROMPT
    if user_context:
        prompt += f"\n\nAdditional context from user: {user_context}"
    
    return call_opencode_api(CIRCUIT_MODEL, prompt, image_base64)


def analyze_verilog(code: str) -> str:
    """Analyze Verilog code"""
    prompt = f"{VERILOG_ANALYSIS_PROMPT}\n\nPlease analyze the following Verilog code:\n\n```{code}```"
    return call_opencode_api(VERILOG_MODEL, prompt)


def main():
    st.set_page_config(
        page_title="AI Hardware Debug Assistant",
        page_icon="🔧",
        layout="wide"
    )
    
    # Header
    st.title("🔧 AI Hardware Debug Assistant")
    st.markdown("*Intelligent circuit and Verilog debugging powered by local AI*")
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    analysis_type = st.sidebar.radio(
        "Select Analysis Type",
        ["🏛️ Circuit Analysis", "📝 Verilog Debugging"],
        label_visibility="collapsed"
    )
    
    # Display OpenCode connection status
    try:
        f"{OPENCODE_API_URL}/v1/chat/completions"
        if response.status_code == 200:
            st.sidebar.success("✅ OpenCode Connected")
            models = response.json().get("models", [])
            if models:
                st.sidebar.info(f"Available models: {len(models)}")
        else:
            st.sidebar.error("⚠️ OpenCode unavailable")
    except:
        st.sidebar.error("⚠️ Cannot connect to OpenCode")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Settings")
    st.sidebar.markdown(f"Circuit Model: `{CIRCUIT_MODEL}`")
    st.sidebar.markdown(f"Verilog Model: `{VERILOG_MODEL}`")
    
    if analysis_type == "🏛️ Circuit Analysis":
        render_circuit_analysis()
    else:
        render_verilog_analysis()


def render_circuit_analysis():
    """Render circuit analysis interface"""
    st.header("Circuit Fault Detection")
    st.markdown("Upload a circuit schematic image to identify potential faults and get diagnostic recommendations.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📤 Upload Circuit Image")
        uploaded_file = st.file_uploader(
            "Choose a circuit schematic image",
            type=["png", "jpg", "jpeg"],
            help="Upload an image of your circuit schematic (PNG, JPG, or JPEG)"
        )
        
        if uploaded_file:
            st.image(uploaded_file, caption="Uploaded Circuit", use_container_width=True)
        
        user_context = st.text_area(
            "Additional Context (Optional)",
            placeholder="e.g., 'Output waveform shows clipping at peaks' or 'Circuit worked before but stopped after replacing component'",
            height=100,
            help="Provide any symptoms or observations you've noticed"
        )
    
    with col2:
        st.subheader("📊 Analysis Results")
        
        if uploaded_file:
            if st.button("🔍 Analyze Circuit", type="primary", use_container_width=True):
                with st.spinner("Analyzing circuit... This may take a moment."):
                    result = analyze_circuit(uploaded_file, user_context)
                    st.session_state["circuit_result"] = result
        else:
            st.info("👆 Please upload a circuit image to begin analysis")
        
        if "circuit_result" in st.session_state:
            st.markdown("---")
            st.markdown(st.session_state["circuit_result"])
            
            # Option to copy result
            if st.button("📋 Copy Results"):
                st.toast("Results copied to clipboard!")
    
    # Information section
    st.markdown("---")
    with st.expander("ℹ️ Supported Circuit Types"):
        st.markdown("""
        - **Analog Circuits**: Op-amp circuits, RC/RL/RLC networks, filter circuits
        - **Power Supplies**: Linear regulators, switching supplies, voltage dividers
        - **Basic Components**: Resistors, capacitors, inductors, diodes, transistors
        - **Simple Digital**: Gate-level circuits, basic logic implementations
        """)


def render_verilog_analysis():
    """Render Verilog analysis interface"""
    st.header("Verilog Code Debugging")
    st.markdown("Paste your Verilog code below to identify errors, get explanations, and receive corrected code.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📝 Enter Verilog Code")
        
        verilog_code = st.text_area(
            "Verilog Code",
            placeholder="""// Paste your Verilog code here
module example (
    input clk,
    input rst,
    output [7:0] count
);
    always @(posedge clk) begin
        if (rst)
            count <= 0;
        else
            count <= count + 1;
    end
endmodule""",
            height=400,
            help="Enter your Verilog code for analysis"
        )
        
        col_upload, col_clear = st.columns(2)
        with col_upload:
            uploaded_verilog = st.file_uploader(
                "Or upload .v file",
                type=["v", "vh", "verilog"],
                label_visibility="collapsed"
            )
            if uploaded_verilog:
                verilog_code = uploaded_verilog.read().decode("utf-8")
                st.text_area("Verilog Code", verilog_code, height=400, disabled=True, key="verilog_display")
        
        with col_clear:
            if st.button("🗑️ Clear"):
                verilog_code = ""
                if "verilog_result" in st.session_state:
                    del st.session_state["verilog_result"]
                st.rerun()
    
    with col2:
        st.subheader("🔍 Analysis Results")
        
        if verilog_code.strip():
            if st.button("🔍 Analyze Code", type="primary", use_container_width=True):
                with st.spinner("Analyzing Verilog code... This may take a moment."):
                    result = analyze_verilog(verilog_code)
                    st.session_state["verilog_result"] = result
        else:
            st.info("👆 Please enter Verilog code to begin analysis")
        
        if "verilog_result" in st.session_state:
            st.markdown("---")
            st.markdown(st.session_state["verilog_result"])
    
    # Information section
    st.markdown("---")
    with st.expander("ℹ️ Error Categories Detected"):
        st.markdown("""
        - **Clocking Issues**: Missing clocks, incorrect assignments, CDC problems
        - **Reset Logic Errors**: Improper reset sequencing, missing resets
        - **FSM Defects**: Dead states, unreachable states, missing defaults
        - **Syntax Errors**: Missing semicolons, incorrect operators, port mismatches
        - **Logic Mistakes**: Blocking/non-blocking errors, latch inference, combinational loops
        """)


if __name__ == "__main__":
    main()
