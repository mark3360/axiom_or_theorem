import uuid
import os
import shutil
import subprocess

SANDBOX_INPUT = "/tmp/lean-sandbox"

def check_lean_proof(code: str) -> dict:
    # Give this execution its own directory
    execution_id = uuid.uuid4().hex

    execution_dir = os.path.join(
        SANDBOX_INPUT,
        execution_id
    )

    os.makedirs(execution_dir)

    filepath = os.path.join(
        execution_dir,
        "Main.lean"
    )

    try:
        # Write the user's Lean code
        with open(filepath, "w") as f:
            f.write(code)

        # Run Lean inside our existing container
        result = subprocess.run(
            [
                "docker",
                "exec",
                "lean-sandbox",
                "/root/.elan/toolchains/leanprover--lean4---v4.33.1/bin/lean",
                f"/input/{execution_id}/Main.lean",
            ],
            capture_output=True,
            text=True,
            timeout=5,
        )

        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "stdout": "",
            "stderr": "Lean execution timed out.",
        }

    finally:
        # Delete the user's code after execution
        shutil.rmtree(execution_dir, ignore_errors=True)