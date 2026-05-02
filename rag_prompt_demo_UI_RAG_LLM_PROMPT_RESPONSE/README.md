# RAG + Prompt Streamlit Demo

Architecture:
UI → Input → Retrieval → LLM + Prompt → Response

This project demonstrates:
- retrieval of the correct business rule
- sending that retrieved fact into a base LLM
- prompt-based control of the output format

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

## Best demo input
- Age: 30
- Income: 40000
- Credit Score: 650

This will retrieve Rule 4 and show a controlled response.
