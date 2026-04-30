#this is aa pipeline for the data which is not fixed and to be sent again for fixation.

import sys
import os

# Allow imports from parent folder
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from typing import TypedDict
from langgraph.graph import StateGraph, END

from tools.code_runner import run_code
from agents.planner import planner_agent
from agents.fixer import fixer_agent
from agents.validator import validator_agent

# ============================================================
# STEP 1: Define the State
# ============================================================
# State is like a shared notebook that all agents read and write to.
# Every agent can see what previous agents wrote.
# This is how they communicate with each other.

class AgentState(TypedDict):
    original_code: str      # the broken code user gave us
    error: str              # the error from running it
    plan: dict              # planner's diagnosis
    fixed_code: str         # fixer's corrected code
    validated: bool         # did validator approve it?
    attempts: int           # how many fix attempts so far
    final_output: str       # the final result message

# ============================================================
# STEP 2: Define the Node Functions
# ============================================================
# Each node is one step in the pipeline.
# A node receives the current state, does its job,
# and returns ONLY the fields it wants to update.

def run_code_node(state: AgentState) -> dict:
    """Runs the original broken code and captures the error."""
    print("🔍 Running broken code...")
    result = run_code(state["original_code"])
    return {"error": result["stderr"]}


def planner_node(state: AgentState) -> dict:
    """Sends code + error to planner agent for diagnosis."""
    print("🧠 Planner analyzing the error...")
    plan = planner_agent(state["original_code"], state["error"])
    return {"plan": plan}


def fixer_node(state: AgentState) -> dict:
    """Sends code + plan to fixer agent to write the fix."""
    print(f"🔧 Fixer attempting fix (attempt {state['attempts'] + 1})...")
    result = fixer_agent(
        state["original_code"],
        state["error"],
        state["plan"]["fix_strategy"]
    )
    return {
        "fixed_code": result["fixed_code"],
        "attempts": state["attempts"] + 1
    }


def validator_node(state: AgentState) -> dict:
    """Runs the fixed code to check if it actually works."""
    print("✅ Validator checking the fix...")
    result = validator_agent(state["fixed_code"])
    
    if result["validated"]:
        final = f"""
╔══════════════════════════════════════╗
║         FIX SUCCESSFUL! ✅           ║
╚══════════════════════════════════════╝

ORIGINAL CODE:
{state['original_code']}

ERROR WAS:
{state['error']}

FIXED CODE:
{state['fixed_code']}

ATTEMPTS NEEDED: {state['attempts']}
"""
    else:
        final = f"Fix attempt {state['attempts']} failed. Retrying..."

    return {
        "validated": result["validated"],
        "final_output": final
    }


# ============================================================
# STEP 3: Define the Decision Function
# ============================================================
# This is the "brain" of the loop.
# After validator runs, should we stop or try again?

def should_continue(state: AgentState) -> str:
    """
    Decision function — LangGraph calls this after validator.
    Returns either "fix_again" or "end" based on result.
    
    Why max 3 attempts? To prevent infinite loops.
    If it can't fix in 3 tries, something is fundamentally wrong.
    """
    if state["validated"]:
        return "end"
    elif state["attempts"] >= 3:
        print("❌ Max attempts reached. Could not fix the code.")
        return "end"
    else:
        return "fix_again"


# ============================================================
# STEP 4: Build the Graph
# ============================================================
# This is where we connect all nodes together
# like drawing arrows between boxes in a flowchart.

def build_pipeline():
    # Create a new graph with our state structure
    graph = StateGraph(AgentState)

    # Add each agent as a node
    graph.add_node("run_code", run_code_node)
    graph.add_node("planner", planner_node)
    graph.add_node("fixer", fixer_node)
    graph.add_node("validator", validator_node)

    # Connect the nodes with edges (arrows)
    # This defines the ORDER agents run in
    graph.set_entry_point("run_code")           # start here
    graph.add_edge("run_code", "planner")       # then planner
    graph.add_edge("planner", "fixer")          # then fixer
    graph.add_edge("fixer", "validator")        # then validator

    # Conditional edge — this is the loop!
    # After validator, call should_continue() to decide what happens next
    graph.add_conditional_edges(
        "validator",
        should_continue,
        {
            "fix_again": "fixer",   # loop back to fixer
            "end": END              # or finish
        }
    )

    return graph.compile()


# ============================================================
# STEP 5: Run function
# ============================================================

def run_pipeline(broken_code: str) -> str:
    """Main function to run the full AutoDebug pipeline."""
    
    pipeline = build_pipeline()
    
    # Initial state — everything starts empty except the broken code
    initial_state = {
        "original_code": broken_code,
        "error": "",
        "plan": {},
        "fixed_code": "",
        "validated": False,
        "attempts": 0,
        "final_output": ""
    }
    
    # Run the pipeline!
    final_state = pipeline.invoke(initial_state)
    
    return final_state["final_output"]