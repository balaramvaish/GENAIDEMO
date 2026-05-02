import streamlit as st

st.set_page_config(page_title="RAG + Base LLM Demo", layout="centered")
st.title("UI → Input → Retrieval → Base LLM → Response")

# Knowledge base
rules = {
    "Rule 1": "If age < 21 → Reject",
    "Rule 2": "If income < 25000 → Reject",
    "Rule 3": "If good profile → Eligible",
    "Rule 4": "If credit score 600–699 → Manual Review"
}

def retrieve_rule(age, income, score):
    if age < 21:
        return "Rule 1"
    elif income < 25000:
        return "Rule 2"
    elif 600 <= score <= 699:
        return "Rule 4"
    else:
        return "Rule 3"

def base_llm_response(rule):
    responses = {
        "Rule 1": "Applicant is rejected due to age criteria.",
        "Rule 2": "Income is below required level, so not eligible.",
        "Rule 3": "Applicant meets all criteria and is eligible.",
        "Rule 4": "Application requires manual review."
    }
    return responses.get(rule, "No decision")

# UI Input
age = st.number_input("Age", 18, 100, 30)
income = st.number_input("Income", 0, 100000, 40000)
score = st.number_input("Credit Score", 300, 900, 650)

if st.button("Run Demo"):
    rule = retrieve_rule(age, income, score)

    st.subheader("Retrieved Rule")
    st.write(f"{rule}: {rules[rule]}")

    response = base_llm_response(rule)

    st.subheader("LLM Response")
    st.write(response)

st.code("UI → Input → Retrieval → Base LLM → Response")
