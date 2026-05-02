# RAG → Fine-Tuned Model Demo

Architecture:
UI → Input → Retrieval → Fine-Tuned Model → Response

## What this app shows
- deterministic retrieval from a simple loan-rule knowledge base
- sending the retrieved rule to a fine-tuned model
- a practical UI for KT/demo sessions

## Install
```bash
pip install -r requirements.txt
```

## Set API key

### Windows PowerShell
```powershell
$env:OPENAI_API_KEY="your_api_key_here"
```

### macOS / Linux
```bash
export OPENAI_API_KEY="your_api_key_here"
```

## Run
```bash
streamlit run app.py
```

## Important
Replace the default model name in the sidebar with your actual fine-tuned model ID.

## Best demo input
- Age: 30
- Income: 40000
- Credit Score: 650
