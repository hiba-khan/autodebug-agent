#Take the broken code + the planner's diagnosis → ask Groq to write a fixed version of the code → return the fixed code.

#file - 5

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def fixer_agent(code: str, error: str, fix_strategy: str) -> dict:
    """
    The Fixer Agent takes the broken code + planner's strategy
    and asks Groq to write the actual fixed code.
    
    Input:  broken code + error + fix strategy
    Output: fixed code
    """

    prompt = f"""You are a Python debugging expert. Fix the broken code below.

BROKEN CODE:
```python
{code}
```

ERROR:
{error}

FIX STRATEGY:
{fix_strategy}

Rules:
- Return ONLY the fixed Python code
- No explanations
- No markdown backticks
- No extra text
- Just the raw fixed code itself
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )

    fixed_code = response.choices[0].message.content.strip()

    # Sometimes the LLM wraps code in ```python ``` despite instructions
    # This cleans that up just in case
    if fixed_code.startswith("```"):
        lines = fixed_code.split('\n')
        # Remove first line (```python) and last line (```)
        fixed_code = '\n'.join(lines[1:-1])

    return {
        "fixed_code": fixed_code,
        "original_code": code,
        "error": error,
        "fix_strategy": fix_strategy
    }
