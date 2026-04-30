
#2nd file: tools/test_runner.py

from code_runner import run_code    #importing from 1st file. 

# Test 1: Working code
print("TEST 1 - Working code:")
result = run_code("print('hello world')")
print(result)

# Test 2: Broken code
print("\nTEST 2 - Broken code:")
result = run_code("print(undefined_variable)")
print(result)

# Test 3: Infinite loop protection
print("\nTEST 3 - Infinite loop:")
result = run_code("while True: pass", timeout=3)
print(result)