#file - 6 

from fixer import fixer_agent

broken_code = "print(undefined_variable)"
error = "NameError: name 'undefined_variable' is not defined"
fix_strategy = "Define the variable before printing its value."

print("Sending to Fixer Agent...")
print("-" * 40)

result = fixer_agent(broken_code, error, fix_strategy)

print(f"Original Code: {result['original_code']}")
print(f"Fixed Code: {result['fixed_code']}")