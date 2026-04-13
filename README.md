# AI Hardware Debug Assistant

An intelligent, user-friendly application for **electronic circuit fault detection** and **Verilog code debugging**, powered by local AI models.

## Features

- **Circuit Fault Detection**: Upload circuit schematic images and receive AI-powered diagnosis
- **Verilog Debugging**: Analyze Verilog code for errors with corrected code provided
- **Offline Operation**: Runs entirely on local hardware using OpenCode
- **Student-Friendly**: Simple interface with clear explanations

---

## Prerequisites

### 1. Python
Make sure Python 3.10 or higher is installed.
```bash
python --version
```

### 2. OpenCode
This project requires **OpenCode** to be installed and running locally.

#### Installing OpenCode:
```bash
# Download OpenCode from https://opencode.ai
# Or install via package manager

# For Windows: Download the .exe from the official website
# For Linux: Follow installation instructions
```

#### Required Models:
Before running the application, download the required AI models:

```bash
# For circuit image analysis (vision model)
opencode pull llava

# For Verilog code analysis
opencode pull codellama
```

#### Starting OpenCode Server:
```bash
# Start OpenCode in server mode
opencode serve
```

---

## Installation

### Step 1: Clone or Download the Project
```bash
# If using Git
git clone <repository-url>
cd AI_Hardware_Debug_Assistant

# Or simply extract the ZIP file and navigate to the folder
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Running the Application

### Step 1: Ensure OpenCode is Running
Open a terminal and start OpenCode:
```bash
opencode serve
```
Keep this terminal open while running the app.

### Step 2: Run the Streamlit Application
```bash
streamlit run app.py
```

### Step 3: Access the Application
Open your web browser and go to:
```
http://localhost:8501
```

---

## Project Structure

```
AI_Hardware_Debug_Assistant/
│
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── prompts.py         # System prompts for AI (optional)
```

---

## Usage Guide

### Circuit Analysis

1. **Select Analysis Type**: Choose "Circuit Analysis" from the sidebar
2. **Upload Image**: Click "Browse files" and select your circuit schematic image
3. **Add Context** (Optional): Describe any symptoms you've observed
4. **Analyze**: Click "Analyze Circuit" to get diagnosis
5. **View Results**: See fault analysis, causes, and recommended fixes

### Verilog Debugging

1. **Select Analysis Type**: Choose "Verilog Debugging" from the sidebar
2. **Enter Code**: Paste your Verilog code or upload a .v file
3. **Analyze**: Click "Analyze Code" to identify errors
4. **View Results**: See categorized errors with explanations and corrected code

---

## Configuration

### Environment Variables (Optional)

You can customize the settings by setting environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENCODE_API_URL` | `http://localhost:8080` | OpenCode server URL |
| `CIRCUIT_MODEL` | `llava` | Model for circuit image analysis |
| `VERILOG_MODEL` | `codellama` | Model for Verilog analysis |

Example:
```bash
# Windows
set OPENCODE_API_URL=http://localhost:8080
set CIRCUIT_MODEL=llava
set VERILOG_MODEL=codellama

# Linux/Mac
export OPENCODE_API_URL=http://localhost:8080
export CIRCUIT_MODEL=llava
export VERILOG_MODEL=codellama
```

---

## Troubleshooting

### "Cannot connect to OpenCode"
- Make sure OpenCode is running: `opencode serve`
- Check the URL in app.py matches your OpenCode server address
- Try: `curl http://localhost:8080/api/tags` to verify connection

### "Model not found"
- Download the required models: `opencode pull llava` and `opencode pull codellama`
- Check available models: `opencode list`

### Slow Response
- Consider using GPU acceleration in OpenCode
- Smaller models like `mistral` may be faster but less accurate
- Reduce image resolution before uploading

### Image Upload Issues
- Supported formats: PNG, JPG, JPEG
- Maximum recommended size: 5MB
- Try a clearer, higher-resolution image

---

## Supported Circuits

### Analog Circuits
- Op-amp circuits (inverting, non-inverting, etc.)
- RC, RL, RLC networks
- Filter circuits (low-pass, high-pass, band-pass)
- Power supply circuits

### Digital Circuits
- Gate-level implementations
- Basic combinational logic
- Simple sequential circuits

---

## Supported Verilog Analysis

### Error Categories
- **Clocking Issues**: Missing/incorrect clocks, clock domain crossing
- **Reset Logic Errors**: Improper reset, missing resets
- **FSM Defects**: Dead states, unreachable states, incomplete transitions
- **Syntax Errors**: Missing semicolons, port mismatches
- **Logic Mistakes**: Blocking/non-blocking errors, latch inference

---

## Demo Mode (Without OpenCode)

To test the interface without AI capabilities, you can run a demo version:

```python
# In app.py, set DEMO_MODE = True
DEMO_MODE = True
```

---

## License

This project is for educational purposes.

---

## Credits

Built with:
- [Streamlit](https://streamlit.io/) - Web UI framework
- [OpenCode](https://opencode.ai/) - Local LLM inference
- [Pillow](https://python-pillow.org/) - Image processing

---

## Contact

For issues or questions, please create an issue in the repository.
