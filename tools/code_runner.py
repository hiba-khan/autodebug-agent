import subprocess   #this is where we will run the code in a separate process
import sys     
import tempfile  # we will write the code to a temporary file before running it
import os

def run_code(code: str, timeout: int = 10) -> dict:
    """
    Safely executes Python code in an isolated subprocess.
    Returns a dict with stdout, stderr, and success status.
    
    Why subprocess? So buggy/infinite code can't crash our agent.
    Why tempfile? We write code to a temp file and run it — 
    cleaner than trying to pass code as a string argument.
    """

    # Step 1: Write the code to a temporary file because subprocess runs files, not raw strings
    with tempfile.NamedTemporaryFile(
        mode='w',           # write mode
        suffix='.py',       # give it a .py extension
        delete=False,       # don't auto-delete yet, we need to run it first
        encoding='utf-8'
    ) as tmp_file:
        tmp_file.write(code)
        tmp_path = tmp_file.name  # save the file path for later

    try:
        # Step 2: Run the temp file as a subprocess
        # sys.executable = the same Python that's running our agent
        # timeout = kill the process if it runs too long
        result = subprocess.run(
            [sys.executable, tmp_path],
            capture_output=True,   # capture both stdout and stderr
            text=True,             # return strings not bytes
            timeout=timeout        # seconds before we force-kill it
        )

        # Step 3: Return what happened
        return {
            "stdout": result.stdout,       # normal output
            "stderr": result.stderr,       # error output
            "success": result.returncode == 0,  # 0 means no error
            "returncode": result.returncode
        }

    except subprocess.TimeoutExpired:
        # Code ran too long — kill it and report timeout
        return {
            "stdout": "",
            "stderr": f"Code timed out after {timeout} seconds.",
            "success": False,
            "returncode": -1
        }

    finally:
        # Step 4: Always clean up the temp file
        # Why finally? Even if an error occurs, we still delete the file
        os.unlink(tmp_path)