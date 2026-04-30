
#file-4

from planner import planner_agent  #from file-3(planner.py)

# Simulate what code_runner would give us
broken_code = "print(undefined_variable)"
error_message = "NameError: name 'undefined_variable' is not defined"

print("Sending to Planner Agent...")
print("-" * 40)

result = planner_agent(broken_code, error_message)

print(f"Error Type: {result['error_type']}")
print(f"Root Cause: {result['root_cause']}")
print(f"Fix Strategy: {result['fix_strategy']}")
print(f"Difficulty: {result['difficulty']}")
print("-" * 40)
print("Full raw response from DeepSeek:")
print(result['raw_analysis'])
