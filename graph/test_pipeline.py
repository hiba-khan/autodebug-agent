import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from pipeline import run_pipeline

# Test with broken code
broken_code = "print(undefined_variable)"

print("Starting AutoDebug Agent...")
print("=" * 50)

result = run_pipeline(broken_code)
print(result)