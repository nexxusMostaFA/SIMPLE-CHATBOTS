import streamlit as st
from ollama import Client

st.set_page_config(
    page_title="TA7T BITY AI CHAT",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        .stChatMessage {
            padding: 1rem;
            border-radius: 0.5rem;
            margin-bottom: 1rem;
        }
        .stChatInputContainer {
            padding-top: 1rem;
            border-top: 1px solid #e0e0e0;
        }
        .stMarkdown {
            line-height: 1.6;
        }
        .stButton button {
            width: 100%;
        }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.image("https://api.dicebear.com/7.x/bottts/svg?seed=ta7t-bity", width=100)
    st.title("Chat Settings")
    st.markdown("""
    ### About
    This is an AI chatbot powered by Llama 3 (7B).
    
    ### Features
    - Real-time streaming responses
    - Conversation memory
    - Markdown support
    """)
    
    if st.button("Clear Chat History"):
        st.session_state.messages = [{"role": "assistant", "content": "How can I assist you today in our app TA7T BITY ?"}]
        st.rerun()


st.title("💬 TA7T BITY AI CHAT")
st.markdown("##### Powered by Llama 3 (7B)")


if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I assist you today in our app TA7T BITY ?"}]


for msg in st.session_state.messages:
    avatar = "🧑‍💻" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])


def generate_response():
    client = Client()
    response = client.chat(
        model='llama3',
        stream=True,
        messages=st.session_state.messages
    )
    for partial_resp in response:
        token = partial_resp["message"]["content"]
        st.session_state["full_message"] += token
        yield token


if prompt := st.chat_input(placeholder="Type your message here..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

 
    st.session_state["full_message"] = ""
    with st.chat_message("assistant", avatar="🤖"):
        st.write_stream(generate_response)
    
    st.session_state.messages.append({
        "role": "assistant",
        "content": st.session_state["full_message"]
    })

st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "Built with Streamlit & Llama 3</div>",
    unsafe_allow_html=True
)


 