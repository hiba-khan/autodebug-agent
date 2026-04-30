#file - 7

import sys
import os

# This line lets us import from the tools folder
# Why? validator needs code_runner but they're in different folders
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from tools.code_runner import run_code

def validator_agent(fixed_code: str) -> dict:
    """
    The Validator Agent checks if the fixed code actually works.
    
    It does this by literally running the fixed code and checking:
    - Did it run without errors? → Success
    - Did it throw an error again? → Failure, needs another fix attempt
    
    This is what makes our system agentic —
    it doesn't just trust the fix, it VERIFIES it.
    """

    # Run the fixed code using our code_runner tool
    result = run_code(fixed_code)

    if result["success"]:
        # Code ran without any errors
        return {
            "validated": True,
            "message": "Fix successful! Code runs without errors.",
            "output": result["stdout"],
            "fixed_code": fixed_code
        }
    else:
        # Code still has errors — fixer needs to try again
        return {
            "validated": False,
            "message": "Fix failed. Code still has errors.",
            "error": result["stderr"],
            "fixed_code": fixed_code
        }