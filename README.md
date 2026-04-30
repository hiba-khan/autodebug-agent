# 🐛 AutoDebug Agent

An autonomous multi-agent AI system that automatically 
detects, diagnoses, and fixes Python bugs without human intervention.

##  How it works
1.  **Runner** — executes broken code in a safe sandbox
2.  **Planner** — diagnoses the error using LLM
3.  **Fixer** — generates a fix autonomously
4.  **Validator** — verifies the fix actually works
5.  **Loop** — retries automatically if fix fails (max 3 attempts)

##  Tech Stack
- **LangGraph** — multi-agent orchestration
- **Groq + Llama3-70b** — LLM backbone
- **Python subprocess** — sandboxed code execution
- **Streamlit** — web UI
- **PostgreSQL** — bug session logging

##  Run Locally
git clone https://github.com/hiba-khan/autodebug-agent
cd autodebug-agent
pip install -r requirements.txt
streamlit run app.py