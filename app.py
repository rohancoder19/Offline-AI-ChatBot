#from config import API_KEY
from google import genai

#client = genai.Client(api_key=API_KEY)

#response = client.models.generate_content(
  #      model="gemini-.5-flash",
   #     contents="Hellow Gemini.python app.py"
#)
#
#print(response.text)
import streamlit as st
from google import genai
from config import API_KEY

st.set_page_config(
    page_title="AI Chatbot",
    page_icon=" ",
    layout="centered"
)

if not API_KEY:
    st.error("🔑 Gemini API Key is missing!")
    st.info("""
    To run this app on Streamlit Cloud, you need to set your Gemini API Key in the Streamlit Secrets:
    
    1. Go to your **Streamlit App Dashboard**.
    2. Click on the app's settings (**Settings** -> **Secrets**).
    3. Add the following:
       ```toml
       GOOGLE_GEMINI_API_KEY = "your_actual_api_key_here"
       ```
    4. Save the secrets and reboot the app.
    
    *If running locally, please add `GOOGLE_GEMINI_API_KEY=your_key` to a `.env` file in the root directory.*
    """)
    st.stop()

client = genai.Client(api_key=API_KEY)

st.title(" AI Chatbot")
st.caption("Powered by Google Gemini")

# ---------------- Sidebar ----------------

st.sidebar.title("Settings")

model_name = st.sidebar.selectbox(
    "Select Model",
    [
        "gemini-3.5-flash",
        "gemini-2.5-flash",
        "gemini-2.5-pro"
    ]
)

temperature = st.sidebar.slider(
    "Temperature",
    min_value=0.0,
    max_value=2.0,
    value=0.7,
    step=0.1
)

max_tokens = st.sidebar.slider(
    "Maximum Output Tokens",
    min_value=100,
    max_value=2048,
    value=512,
    step=100
)

if st.sidebar.button(" Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# ------------- Session State -------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# -------- Display Previous Messages -------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ------------- User Input ----------------

prompt = st.chat_input("Ask anything...")

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        config={
            "temperature": temperature,
            "max_output_tokens": max_tokens
        }
    )

    answer = response.text

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

# -------- Download Chat --------

chat_text = ""

for message in st.session_state.messages:

    chat_text += (
        f"{message['role'].upper()}:\n"
        f"{message['content']}\n\n"
    )

st.sidebar.download_button(
    label=" Download Chat",
    data=chat_text,
    file_name="chat_history.txt",
    mime="text/plain"
)