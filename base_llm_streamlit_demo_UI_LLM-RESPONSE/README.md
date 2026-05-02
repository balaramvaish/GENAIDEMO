# Base LLM Streamlit Demo

This is a simple practical demo for:

UI → Input → Base LLM → Response

It does not use:
- RAG
- fine-tuning

## Files
- `app.py`
- `requirements.txt`

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

## Good demo prompts
- Explain the difference between RAG and fine-tuning in simple terms.
- Can I get a loan if I am 25 years old, income 24000, credit score 720?
- Give me a 3-line summary of generative AI for a beginner.
