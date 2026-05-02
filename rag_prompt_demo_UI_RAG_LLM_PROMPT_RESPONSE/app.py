import os
from typing import Dict, List, Optional

import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="RAG + Prompt Demo", layout="wide")
st.title("UI → Input → Retrieval → LLM + Prompt → Response")
st.caption("Practical demo for RAG + prompt-based behavior control")

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

def format_customer(customer: Dict) -> str:
    return (
        f"Age: {customer['age']}\n"
        f"Income: {customer['income']}\n"
        f"Credit Score: {customer['credit_score']}"
    )

def prompt_controlled_response(client: OpenAI, model_name: str, retrieved_doc: Dict, customer: Dict) -> str:
    prompt = f"""
You are a loan eligibility assistant.

Use ONLY the retrieved policy rule below.
Do not use outside assumptions.

Retrieved policy rule:
{retrieved_doc['title']} ({retrieved_doc['rule']}): {retrieved_doc['content']}

Applicant details:
{format_customer(customer)}

Return the answer in exactly this format:

Decision: <Eligible / Rejected / Manual Review / Unknown>
Reason: <one sentence>
Rule Applied: <rule name>
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
    model_name = st.text_input("Base model", value="gpt-5.4")

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
    st.subheader("Applicant input")
    age = st.number_input("Age", min_value=18, max_value=100, key="age")
    income = st.number_input("Monthly Income", min_value=0, max_value=500000, step=1000, key="income")
    credit_score = st.number_input("Credit Score", min_value=300, max_value=900, key="credit_score")

customer = {"age": int(age), "income": int(income), "credit_score": int(credit_score)}
retrieved_doc = retrieve_relevant_rule(customer, KNOWLEDGE_BASE)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Current Input")
    st.json(customer)

    st.subheader("Retrieved Rule")
    if retrieved_doc:
        st.success(f"{retrieved_doc['title']} | {retrieved_doc['rule']}")
        st.code(retrieved_doc["content"], language="text")
    else:
        st.warning("No matching rule found.")

with col2:
    st.subheader("Architecture")
    st.code("UI → Input → Retrieval → LLM + Prompt → Response", language="text")
    st.subheader("Prompt Behavior")
    st.write("The prompt forces the model to use only the retrieved rule and answer in a fixed structure.")

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

    with st.spinner("Generating response..."):
        try:
            result = prompt_controlled_response(client, model_name, retrieved_doc, customer)
        except Exception as e:
            st.error(f"API call failed: {e}")
            st.stop()

    st.subheader("Final Response")
    st.code(result, language="text")

    st.subheader("What this proves")
    st.write(
        "- UI collects the user input.\n"
        "- Retrieval fetches the correct business fact.\n"
        "- The base LLM uses prompt instructions to control the answer format.\n"
        "- This is RAG + prompt-based behavior control, not fine-tuning."
    )
