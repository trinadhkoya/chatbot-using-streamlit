import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load environment variables from .env file (specifically GROQ_API_KEY)
load_dotenv()

# Configure the Streamlit page settings
st.set_page_config(
    page_title="TrinAI Nexus",
    page_icon="🤖",
    layout="centered",
)
st.title("🤖 TrinAI Nexus")

# Initialize chat history in session state if it doesn't exist
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Render existing chat history from session state
# This ensures previous messages remain visible on page reruns

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Initialize the LLM with the specific model
# temperature=0.0 ensures deterministic outputs
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.0)

# Capture user input
user_prompt = st.chat_input("What's on your mind? The Nexus is ready.")

if user_prompt:
    # Display user message immediately
    st.chat_message('user').markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # Generate response using the LLM
    # We prepend a system message to define the assistant's behavior
    # 'st.session_state.chat_history' is a list of dictionaries: [{...}, {...}]
    # without '*', the input would become: [system_msg, [{...}, {...}]] (Nested List - Wrong)
    # with '*', the input becomes: [system_msg, {...}, {...}] (Flat List - Correct)
    response = llm.invoke(
        input=[
            {"role": "system", "content": "You are a helpful assistant."}, *st.session_state.chat_history
        ]
    )
    # Display and store assistant response
    assistant_response = response.content
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
