# Fine-Tuned Model Streamlit Demo

Architecture:
UI → Input → Fine-Tuned Model → Response

This project demonstrates:
- direct user input sent to a fine-tuned model
- no retrieval
- no RAG

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
Replace the fine-tuned model name in the sidebar with your real fine-tuned model ID.

Example shape:
```text
ft:your-fine-tuned-model-id
```

## Suggested demo inputs
- Age: 25, Income: 24000, Credit Score: 720
- Age: 30, Income: 40000, Credit Score: 650
- Age: 30, Income: 40000, Credit Score: 750
