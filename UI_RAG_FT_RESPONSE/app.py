import os
from typing import Dict, List, Optional

import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="RAG → Fine-Tuned Model Demo", layout="wide")
st.title("UI → Input → Retrieval → Fine-Tuned Model → Response")
st.caption("Practical demo for RAG + fine-tuned model")

# Replace this with your actual fine-tuned model id, e.g.
# ft:gpt-4.1-mini:your-org:loan-eligibility-demo:abc123
DEFAULT_FT_MODEL = "ft:your-fine-tuned-model-id"

KNOWLEDGE_BASE = [
    {"id": "doc1", "title": "Loan Rule 1", "content": "If age is less than 21, reject the loan application.", "rule": "Rule 1"},
    {"id": "doc2", "title": "Loan Rule 2", "content": "If monthly income is less than 25000, reject the loan application.", "rule": "Rule 2"},
    {"id": "doc3", "title": "Loan Rule 3", "content": "If age is 21 or above, monthly income is at least 25000, and credit score is at least 700, approve the loan application.", "rule": "Rule 3"},
    {"id": "doc4", "title": "Loan Rule 4", "content": "If credit score is between 600 and 699, mark the application for manual review.", "rule": "Rule 4"},
]

def get_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set.")
    return OpenAI(api_key=api_key)

def retrieve_relevant_rule(customer: Dict, kb: List[Dict]) -> Optional[Dict]:
    age = customer["age"]
    income = customer["income"]
    credit_score = customer["credit_score"]

    for doc in kb:
        rule = doc["rule"]
        if rule == "Rule 1" and age < 21:
            return doc
        elif rule == "Rule 2" and income < 25000:
            return doc
        elif rule == "Rule 4" and 600 <= credit_score <= 699:
            return doc
        elif rule == "Rule 3" and age >= 21 and income >= 25000 and credit_score >= 700:
            return doc
    return None

def build_customer(age: int, income: int, credit_score: int) -> Dict:
    return {"age": int(age), "income": int(income), "credit_score": int(credit_score)}

def format_customer(customer: Dict) -> str:
    return (
        f"Age: {customer['age']}\n"
        f"Income: {customer['income']}\n"
        f"Credit Score: {customer['credit_score']}"
    )

def call_finetuned_model(client: OpenAI, model_name: str, retrieved_doc: Dict, customer: Dict) -> str:
    prompt = f"""
You are a loan eligibility assistant.

Use only the retrieved policy rule below.

Retrieved policy rule:
{retrieved_doc['title']} ({retrieved_doc['rule']}): {retrieved_doc['content']}

Applicant details:
{format_customer(customer)}
""".strip()

    response = client.responses.create(
        model=model_name,
        input=prompt,
    )
    return response.output_text

def apply_preset(name: str) -> None:
    if name == "Rule 1":
        st.session_state["age"] = 19
        st.session_state["income"] = 30000
        st.session_state["credit_score"] = 720
    elif name == "Rule 2":
        st.session_state["age"] = 25
        st.session_state["income"] = 24000
        st.session_state["credit_score"] = 720
    elif name == "Rule 3":
        st.session_state["age"] = 30
        st.session_state["income"] = 40000
        st.session_state["credit_score"] = 750
    elif name == "Rule 4":
        st.session_state["age"] = 30
        st.session_state["income"] = 40000
        st.session_state["credit_score"] = 650

if "age" not in st.session_state:
    st.session_state["age"] = 30
if "income" not in st.session_state:
    st.session_state["income"] = 40000
if "credit_score" not in st.session_state:
    st.session_state["credit_score"] = 650

with st.sidebar:
    st.header("Settings")
    ft_model_name = st.text_input("Fine-tuned model", value=DEFAULT_FT_MODEL)

    st.markdown("---")
    st.subheader("Quick examples")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Rule 1 Example"):
            apply_preset("Rule 1")
        if st.button("Rule 2 Example"):
            apply_preset("Rule 2")
    with c2:
        if st.button("Rule 3 Example"):
            apply_preset("Rule 3")
        if st.button("Rule 4 Example"):
            apply_preset("Rule 4")

    st.markdown("---")
    st.subheader("Applicant Input")
    age = st.number_input("Age", min_value=18, max_value=100, key="age")
    income = st.number_input("Monthly Income", min_value=0, max_value=500000, step=1000, key="income")
    credit_score = st.number_input("Credit Score", min_value=300, max_value=900, key="credit_score")

customer = build_customer(age, income, credit_score)
retrieved_doc = retrieve_relevant_rule(customer, KNOWLEDGE_BASE)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Current Input")
    st.json(customer)

    st.subheader("Retrieved Rule (RAG)")
    if retrieved_doc:
        st.success(f"{retrieved_doc['title']} | {retrieved_doc['rule']}")
        st.code(retrieved_doc["content"], language="text")
    else:
        st.warning("No matching rule found.")

with col2:
    st.subheader("Architecture")
    st.code("UI → Input → Retrieval → Fine-Tuned Model → Response", language="text")
    st.subheader("What this means")
    st.write(
        "RAG fetches the correct business fact first. "
        "The fine-tuned model then generates the final answer using that retrieved fact."
    )

if st.button("Run Demo", type="primary"):
    if not retrieved_doc:
        st.error("No rule retrieved for this input.")
        st.stop()

    try:
        client = get_client()
    except Exception as e:
        st.error(str(e))
        st.info("PowerShell example: $env:OPENAI_API_KEY='your_api_key_here'")
        st.stop()

    with st.spinner("Calling fine-tuned model..."):
        try:
            result = call_finetuned_model(client, ft_model_name, retrieved_doc, customer)
        except Exception as e:
            st.error(f"API call failed: {e}")
            st.stop()

    st.subheader("Fine-Tuned Model Response")
    st.code(result, language="text")

    st.subheader("What this proves")
    st.write(
        "- UI collects the business input.\n"
        "- Retrieval fetches the applicable business rule.\n"
        "- The fine-tuned model uses that retrieved fact to generate the final response.\n"
        "- This is a valid combination of RAG + fine-tuned model."
    )
