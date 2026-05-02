import os
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Fine-Tuned Model Demo", layout="wide")
st.title("UI → Input → Fine-Tuned Model → Response")
st.caption("Practical demo for a fine-tuned model without RAG")

# Replace with your real fine-tuned model ID in the UI
DEFAULT_FT_MODEL = "ft:your-fine-tuned-model-id"

def get_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set.")
    return OpenAI(api_key=api_key)

def build_input(age: int, income: int, credit_score: int) -> str:
    return (
        f"Age: {age}\n"
        f"Income: {income}\n"
        f"Credit Score: {credit_score}"
    )

def call_finetuned_model(client: OpenAI, model_name: str, user_input: str) -> str:
    response = client.responses.create(
        model=model_name,
        input=user_input,
    )
    return response.output_text

with st.sidebar:
    st.header("Settings")
    ft_model_name = st.text_input("Fine-tuned model name", value=DEFAULT_FT_MODEL)

    st.markdown("---")
    st.subheader("Quick examples")
    if st.button("Example 1"):
        st.session_state["age"] = 25
        st.session_state["income"] = 24000
        st.session_state["credit_score"] = 720
    if st.button("Example 2"):
        st.session_state["age"] = 30
        st.session_state["income"] = 40000
        st.session_state["credit_score"] = 650
    if st.button("Example 3"):
        st.session_state["age"] = 30
        st.session_state["income"] = 40000
        st.session_state["credit_score"] = 750

if "age" not in st.session_state:
    st.session_state["age"] = 30
if "income" not in st.session_state:
    st.session_state["income"] = 40000
if "credit_score" not in st.session_state:
    st.session_state["credit_score"] = 650

col1, col2 = st.columns(2)

with col1:
    st.subheader("Applicant Input")
    age = st.number_input("Age", min_value=18, max_value=100, key="age")
    income = st.number_input("Monthly Income", min_value=0, max_value=500000, step=1000, key="income")
    credit_score = st.number_input("Credit Score", min_value=300, max_value=900, key="credit_score")

    user_input = build_input(int(age), int(income), int(credit_score))
    st.subheader("Model Input")
    st.code(user_input, language="text")

with col2:
    st.subheader("Architecture")
    st.code("UI → Input → Fine-Tuned Model → Response", language="text")
    st.subheader("What this means")
    st.write(
        "The UI sends user input directly to a fine-tuned model. "
        "There is no retrieval step and no external knowledge lookup."
    )

if st.button("Run Demo", type="primary"):
    try:
        client = get_client()
    except Exception as e:
        st.error(str(e))
        st.info("PowerShell example: $env:OPENAI_API_KEY='your_api_key_here'")
        st.stop()

    with st.spinner("Calling fine-tuned model..."):
        try:
            result = call_finetuned_model(client, ft_model_name, user_input)
        except Exception as e:
            st.error(f"API call failed: {e}")
            st.stop()

    st.subheader("Model Response")
    st.code(result, language="text")

    st.subheader("What this proves")
    st.write(
        "- UI collects the user input.\n"
        "- The input goes directly to the fine-tuned model.\n"
        "- The fine-tuned model generates the final response.\n"
        "- This architecture does not use RAG."
    )
