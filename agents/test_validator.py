#file - 8

from validator import validator_agent

# Test 1: Give it working code — should pass
print("TEST 1 - Working fix:")
print("-" * 40)
working_code = """
undefined_variable = "some value"
print(undefined_variable)
"""
result = validator_agent(working_code)
print(f"Validated: {result['validated']}")
print(f"Message: {result['message']}")
if result['validated']:
    print(f"Output: {result['output']}")

# Test 2: Give it still-broken code — should fail
print("\nTEST 2 - Still broken code:")
print("-" * 40)
broken_code = "print(still_undefined)"
result = validator_agent(broken_code)
print(f"Validated: {result['validated']}")
print(f"Message: {result['message']}")
if not result['validated']:
    print(f"Error: {result['error']}")