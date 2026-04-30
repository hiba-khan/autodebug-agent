

import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(__file__))
from graph.pipeline import run_pipeline

# ============================================================
# PAGE SETUP
# ============================================================
st.set_page_config(
    page_title="AutoDebug Agent",
    page_icon="🐛",
    layout="wide"
)

# ============================================================
# HEADER
# ============================================================
st.title("🐛 AutoDebug Agent")
st.markdown("**An autonomous AI agent that finds and fixes Python bugs automatically.**")
st.divider()

# ============================================================
# SIDEBAR — how it works
# ============================================================
with st.sidebar:
    st.header("How it works")
    st.markdown("""
    1. 🔍 **Runner** — executes your broken code
    2. 🧠 **Planner** — diagnoses the error
    3. 🔧 **Fixer** — writes the fix
    4. ✅ **Validator** — verifies the fix works
    
    If the fix fails, the agent automatically retries up to 3 times.
    """)
    st.divider()
    st.markdown("Built with LangGraph + Groq + Python")

# ============================================================
# MAIN AREA
# ============================================================
st.subheader("Paste your broken Python code below:")

# Some example broken codes for the user to try
examples = {
    "Select an example...": "",
    "NameError": "print(undefined_variable)",
    "TypeError": "print('Age: ' + 25)",
    "IndexError": "my_list = [1,2,3]\nprint(my_list[10])",
    "ZeroDivisionError": "result = 10 / 0\nprint(result)"
}

selected = st.selectbox("Or pick an example:", list(examples.keys()))

# Text area for code input
code_input = st.text_area(
    "Your broken code:",
    value=examples[selected],
    height=200,
    placeholder="Paste your broken Python code here..."
)

# ============================================================
# RUN BUTTON
# ============================================================
if st.button("🚀 Fix My Code!", type="primary", use_container_width=True):
    
    if not code_input.strip():
        st.warning("Please paste some broken code first!")
    else:
        # Show progress to user while agents are running
        with st.status("🤖 Agent is working...", expanded=True) as status:
            st.write("🔍 Running your code to catch the error...")
            st.write("🧠 Planner diagnosing the problem...")
            st.write("🔧 Fixer writing a solution...")
            st.write("✅ Validator verifying the fix...")
            
            # Run the full pipeline
            result = run_pipeline(code_input)
            
            status.update(label="✅ Done!", state="complete")
        
        # Show the result
        st.divider()
        st.subheader("Result:")
        st.code(result, language="text")
        
        # Extract and highlight the fixed code separately
        if "FIXED CODE:" in result:
            fixed_part = result.split("FIXED CODE:")[1].split("ATTEMPTS")[0].strip()
            st.subheader("✨ Your Fixed Code:")
            st.code(fixed_part, language="python")
            
            # Copy button area
            st.success("Your code has been fixed! Copy the fixed code above.")