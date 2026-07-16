import streamlit as st
import ollama

st.set_page_config(
    page_title="Offline AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

# ---------------- Sidebar ----------------

st.sidebar.title("Offline AI Chatbot")

model_name = st.sidebar.selectbox(
    "Select AI Model",
    [
        "llama3.2",
        "gemma3",
        "mistral",
        "qwen2.5"
    ]
)

if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# ---------------- Session ----------------

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("Offline AI Chatbot")
st.caption("Powered by Ollama")

# ---------------- Chat History ----------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------- User Input ----------------

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

    conversation = []

    for chat in st.session_state.messages:

        conversation.append(
            {
                "role": chat["role"],
                "content": chat["content"]
            }
        )

    with st.spinner("Generating response..."):

        response = ollama.chat(
            model=model_name,
            messages=conversation
        )

    answer = response["message"]["content"]

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

# ---------------- Statistics ----------------

st.sidebar.markdown("---")

st.sidebar.subheader("Statistics")

user_count = len(
    [m for m in st.session_state.messages if m["role"] == "user"]
)

ai_count = len(
    [m for m in st.session_state.messages if m["role"] == "assistant"]
)

st.sidebar.write(f"User Messages : {user_count}")
st.sidebar.write(f"AI Responses : {ai_count}")

# ---------------- Download Chat ----------------

chat_history = ""

for message in st.session_state.messages:

    chat_history += (
        f"{message['role'].upper()}:\n"
        f"{message['content']}\n\n"
    )

st.sidebar.download_button(
    "Download Chat",
    chat_history,
    "chat_history.txt",
    "text/plain"
)