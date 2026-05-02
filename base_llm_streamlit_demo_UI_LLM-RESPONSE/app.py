import os
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Base LLM Demo", layout="centered")
st.title("UI → Input → Base LLM → Response")
st.caption("Simple practical demo without RAG and without fine-tuning")

def get_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set.")
    return OpenAI(api_key=api_key)

with st.sidebar:
    st.header("Settings")
    model_name = st.text_input("Base model", value="gpt-5.4")

st.subheader("User Input")
user_prompt = st.text_area(
    "Enter your question or instruction",
    value="Summarize why RAG and fine-tuning solve different problems.",
    height=140,
)

if st.button("Send to Base LLM", type="primary"):
    if not user_prompt.strip():
        st.warning("Please enter some input.")
        st.stop()

    try:
        client = get_client()
    except Exception as e:
        st.error(str(e))
        st.info("PowerShell example: $env:OPENAI_API_KEY='your_api_key_here'")
        st.stop()

    with st.spinner("Generating response..."):
        try:
            response = client.responses.create(
                model=model_name,
                input=user_prompt,
            )
            output_text = response.output_text
        except Exception as e:
            st.error(f"API call failed: {e}")
            st.stop()

    st.subheader("Response")
    st.write(output_text)

    st.subheader("Architecture")
    st.code("UI → User Input → Base LLM → Response", language="text")
