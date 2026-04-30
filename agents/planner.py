import os
from groq import Groq
from dotenv import load_dotenv

# Load the .env file so we can access GROQ_API_KEY
# Without this line, os.getenv would return None
load_dotenv()

# Initialize the Groq client with our API key
# This is like logging into Groq's service
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def planner_agent(code: str, error: str) -> dict:
    """
    The Planner Agent analyzes the error and decides the fix strategy.
    Now powered by Groq's Llama3 instead of local DeepSeek.
    Same job — diagnose first, prescribe second.
    """

    prompt = f"""You are a Python debugging expert. Be concise and follow the format exactly.

BROKEN CODE:
```python
{code}
```

ERROR:
{error}

Reply in EXACTLY this format with no extra text outside these 4 lines:
ERROR TYPE: <just the error class name e.g. NameError>
ROOT CAUSE: <one short sentence only>
FIX STRATEGY: <one short sentence only>
DIFFICULTY: <Easy, Medium, or Hard>
"""

    # Send prompt to Groq's Llama3 model
    # llama-3.3-70b-versatile means: Llama3, 70 billion parameters, 8192 token context
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1  # low temperature = more focused, less creative
                         # we want precise structured output, not creativity
    )

    # Extract the text — Groq uses OpenAI-compatible format
    # so the path to the content is slightly different from Ollama
    analysis_text = response.choices[0].message.content

    result = {
        "raw_analysis": analysis_text,
        "error_type": extract_field(analysis_text, "ERROR TYPE"),
        "root_cause": extract_field(analysis_text, "ROOT CAUSE"),
        "fix_strategy": extract_field(analysis_text, "FIX STRATEGY"),
        "difficulty": extract_field(analysis_text, "DIFFICULTY")
    }

    return result


def extract_field(text: str, field_name: str) -> str:
    for line in text.split('\n'):
        if line.startswith(field_name):
            parts = line.split(':', 1)
            if len(parts) > 1:
                return parts[1].strip()
    return "Unknown"