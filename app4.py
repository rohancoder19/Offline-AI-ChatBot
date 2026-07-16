import streamlit as st
import os
import socket
from dotenv import load_dotenv

# Try to import ollama and google-genai safely
try:
    import ollama
    OLLAMA_INSTALLED = True
except ImportError:
    OLLAMA_INSTALLED = False

try:
    from google import genai
    from google.genai import types
    GEMINI_INSTALLED = True
except ImportError:
    GEMINI_INSTALLED = False

# Load local .env if it exists
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)

# Configure Page
st.set_page_config(
    page_title="Offline & Cloud AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

# ---------------- Custom Premium CSS Injection ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

/* Apply font to all Streamlit elements */
html, body, [class*="css"], .stMarkdown {
    font-family: 'Outfit', sans-serif !important;
}

/* Gradient Title */
.main-title {
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #6366F1 0%, #A855F7 50%, #EC4899 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0px;
    padding-bottom: 0px;
}

.sub-title {
    font-size: 1.1rem;
    color: #94A3B8;
    margin-top: -5px;
    margin-bottom: 25px;
}

/* Custom Status Indicator Badge */
.status-badge {
    display: inline-flex;
    align-items: center;
    padding: 0.35rem 0.85rem;
    border-radius: 9999px;
    font-size: 0.85rem;
    font-weight: 600;
    margin-bottom: 1.5rem;
    border-width: 1px;
    border-style: solid;
}
.status-online {
    background-color: rgba(16, 185, 129, 0.1);
    color: #10B981;
    border-color: rgba(16, 185, 129, 0.2);
}
.status-offline {
    background-color: rgba(239, 68, 68, 0.1);
    color: #EF4444;
    border-color: rgba(239, 68, 68, 0.2);
}

/* Sidebar Custom Styling */
section[data-testid="stSidebar"] {
    background-color: #0F172A;
    border-right: 1px solid #1E293B;
}

section[data-testid="stSidebar"] .stMarkdown h1, 
section[data-testid="stSidebar"] .stMarkdown h2, 
section[data-testid="stSidebar"] .stMarkdown h3 {
    color: #F8FAFC;
    font-weight: 600;
}

/* Styled Sidebar Buttons */
div.stButton > button {
    background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
    color: #E2E8F0;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    transition: all 0.3s ease;
    width: 100%;
}

div.stButton > button:hover {
    background: linear-gradient(135deg, #334155 0%, #1E293B 100%);
    border-color: #6366F1;
    box-shadow: 0 0 10px rgba(99, 102, 241, 0.4);
}

/* Custom Styled Chat Messages */
[data-testid="stChatMessage"] {
    border-radius: 16px !important;
    padding: 1.25rem !important;
    margin-bottom: 1rem !important;
    border: 1px solid #1E293B !important;
    background-color: #0F172A !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
}

/* Ensure text inside chat messages is clearly readable (off-white) */
[data-testid="stChatMessage"] p, 
[data-testid="stChatMessage"] li, 
[data-testid="stChatMessage"] h1, 
[data-testid="stChatMessage"] h2, 
[data-testid="stChatMessage"] h3, 
[data-testid="stChatMessage"] h4, 
[data-testid="stChatMessage"] h5, 
[data-testid="stChatMessage"] h6 {
    color: #F1F5F9 !important;
}

/* Inline code formatting inside chat messages */
[data-testid="stChatMessage"] code {
    color: #F472B6 !important;
    background-color: #1E293B !important;
    padding: 0.15rem 0.35rem !important;
    border-radius: 4px !important;
    font-size: 0.9em !important;
}

[data-testid="stChatMessageAvatar"] {
    background-color: #1E293B !important;
    border: 1px solid #334155 !important;
}

/* Statistics container styling */
.stats-container {
    background-color: #1E293B;
    border-radius: 12px;
    padding: 1rem;
    border: 1px solid #334155;
    margin-top: 1rem;
    margin-bottom: 1.5rem;
}

.stats-item {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.5rem;
    color: #94A3B8;
    font-size: 0.95rem;
}

.stats-item:last-child {
    margin-bottom: 0;
}

.stats-value {
    font-weight: 700;
    color: #F1F5F9;
}
</style>
""", unsafe_allow_html=True)


# Helper function to check if Ollama is running locally
def check_ollama_status(host="localhost", port=11434):
    if not OLLAMA_INSTALLED:
        return False
    try:
        with socket.create_connection((host, port), timeout=1.0):
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False

# Initialize status flags
ollama_running = check_ollama_status()

# Retrieve developer's Gemini API Key from environment or Streamlit secrets
dev_api_key = None
try:
    if "GOOGLE_GEMINI_API_KEY" in st.secrets:
        dev_api_key = st.secrets["GOOGLE_GEMINI_API_KEY"]
    elif "GEMINI_API_KEY" in st.secrets:
        dev_api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

if not dev_api_key:
    dev_api_key = os.getenv("GOOGLE_GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")


# ---------------- Sidebar Layout ----------------
st.sidebar.title("Settings")

# Provider selection
available_providers = []
if OLLAMA_INSTALLED:
    available_providers.append("Ollama (Offline/Local)")
if GEMINI_INSTALLED:
    available_providers.append("Gemini (Cloud)")

if not available_providers:
    st.sidebar.error("❌ Required packages not installed. Please check requirements.txt.")
    provider = st.sidebar.selectbox("AI Provider", ["None"], disabled=True)
else:
    # If Ollama is running, default to it. Otherwise, default to Gemini if available.
    default_idx = 0
    if not ollama_running and "Gemini (Cloud)" in available_providers:
        default_idx = available_providers.index("Gemini (Cloud)")
    
    provider = st.sidebar.selectbox(
        "AI Provider",
        available_providers,
        index=default_idx
    )

# Handle API Key configuration for Gemini
active_api_key = dev_api_key
if provider == "Gemini (Cloud)":
    # Let users input their own key as well
    user_api_key = st.sidebar.text_input(
        "Gemini API Key (Optional)",
        type="password",
        help="Provide your own Gemini API key. If left blank, the app will try to use the host's configured key."
    )
    if user_api_key:
        active_api_key = user_api_key

# Select AI Model dynamically based on provider
model_name = None
if provider == "Ollama (Offline/Local)":
    # Display local Ollama status
    if ollama_running:
        st.sidebar.markdown(
            '<div class="status-badge status-online">🟢 Ollama Local server: Connected</div>', 
            unsafe_allow_html=True
        )
        try:
            models_info = ollama.list()
            ollama_models = [m['name'] for m in models_info.get('models', [])]
        except Exception:
            ollama_models = []
    else:
        st.sidebar.markdown(
            '<div class="status-badge status-offline">🔴 Ollama Local server: Disconnected</div>', 
            unsafe_allow_html=True
        )
        ollama_models = []

    if not ollama_models:
        ollama_models = ["llama3.2", "gemma3", "mistral", "qwen2.5"]
        st.sidebar.warning("⚠️ Could not fetch active local Ollama models. Using fallback list.")
        st.sidebar.info("Tip: Start your Ollama app and run `ollama pull <model_name>` locally.")

    model_name = st.sidebar.selectbox("Select Ollama Model", ollama_models)

elif provider == "Gemini (Cloud)":
    if active_api_key:
        st.sidebar.markdown(
            '<div class="status-badge status-online">🟢 Gemini Cloud API: Configured</div>', 
            unsafe_allow_html=True
        )
    else:
        st.sidebar.markdown(
            '<div class="status-badge status-offline">🔴 Gemini Cloud API: Key Missing</div>', 
            unsafe_allow_html=True
        )
        st.sidebar.warning("🔑 Gemini API Key is missing!")
        st.sidebar.info(
            "To use Gemini, enter an API Key in the field above, or configure `GOOGLE_GEMINI_API_KEY` in Streamlit Secrets / `.env` file."
        )

    gemini_models = [
        "gemini-2.5-flash",
        "gemini-2.5-pro",
        "gemini-1.5-flash",
        "gemini-3.5-flash"
    ]
    model_name = st.sidebar.selectbox("Select Gemini Model", gemini_models)

# Clear Chat Button
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()


# ---------------- Session State initialization ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []


# ---------------- Main Layout ----------------
st.markdown('<div class="main-title">🤖 AI Chatbot</div>', unsafe_allow_html=True)
st.markdown(
    f'<div class="sub-title">Powered by {provider} — Model: {model_name}</div>', 
    unsafe_allow_html=True
)

# ---------------- Chat History Display ----------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ---------------- User Input & Generation ----------------
prompt = st.chat_input("Ask anything...")

if prompt:
    # Check Gemini API availability if selected
    if provider == "Gemini (Cloud)" and not active_api_key:
        st.error("🔑 API Key is required for Gemini Cloud. Please enter it in the sidebar settings.")
        st.stop()
        
    # Check Ollama status if selected
    if provider == "Ollama (Offline/Local)" and not ollama_running:
        st.error("🔴 Ollama local server is not running. Please launch Ollama locally, or switch to Gemini Cloud in the sidebar.")
        st.stop()

    # Append user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Process response based on provider
    answer = ""
    
    with st.spinner("Generating response..."):
        if provider == "Ollama (Offline/Local)":
            # Prepare conversation history in Ollama format
            conversation = [
                {"role": chat["role"], "content": chat["content"]}
                for chat in st.session_state.messages
            ]
            try:
                response = ollama.chat(
                    model=model_name,
                    messages=conversation
                )
                answer = response["message"]["content"]
            except Exception as e:
                st.error(f"Ollama Error: {e}")
                st.stop()
                
        elif provider == "Gemini (Cloud)":
            try:
                client = genai.Client(api_key=active_api_key)
                # Map role names: Gemini requires "user" or "model"
                contents = []
                for msg in st.session_state.messages:
                    role = "user" if msg["role"] == "user" else "model"
                    contents.append(
                        types.Content(
                            role=role,
                            parts=[types.Part.from_text(text=msg["content"])]
                        )
                    )
                response = client.models.generate_content(
                    model=model_name,
                    contents=contents
                )
                answer = response.text
            except Exception as e:
                st.error(f"Gemini API Error: {e}")
                st.stop()

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(answer)

    # Save to history
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )


# ---------------- Sidebar Statistics & Download ----------------
st.sidebar.markdown("---")
st.sidebar.subheader("Statistics")

user_count = len([m for m in st.session_state.messages if m["role"] == "user"])
ai_count = len([m for m in st.session_state.messages if m["role"] == "assistant"])

# Premium Statistics Card HTML
st.sidebar.markdown(f"""
<div class="stats-container">
    <div class="stats-item">
        <span>User Messages</span>
        <span class="stats-value">{user_count}</span>
    </div>
    <div class="stats-item">
        <span>AI Responses</span>
        <span class="stats-value">{ai_count}</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ---------------- Download Chat History ----------------
chat_history = ""
for message in st.session_state.messages:
    chat_history += f"{message['role'].upper()}:\n{message['content']}\n\n"

st.sidebar.download_button(
    "📥 Download Chat Log",
    chat_history,
    "chat_history.txt",
    "text/plain"
)