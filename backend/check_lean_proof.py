import os

import requests


AXLE_URL = "https://axle.axiommath.ai/api/v1/check"
AXLE_API_KEY = os.environ["AXLE_API_KEY"]

# AXLE environment to use.
AXLE_ENVIRONMENT = "lean-4.28.0"


def check_lean_proof(code: str) -> dict:
    try:
        response = requests.post(
            AXLE_URL,
            headers={
                "Authorization": f"Bearer {AXLE_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "content": code,
                "environment": AXLE_ENVIRONMENT,
            },
            timeout=30,
        )

        response.raise_for_status()

        result = response.json()

        # AXLE's `okay` means the Lean code compiled.
        return {
            "success": result["okay"],
            "stdout": "\n".join(
                result["lean_messages"].get("infos", [])
            ),
            "stderr": "\n".join(
                result["lean_messages"].get("errors", [])
            ),
        }

    except requests.Timeout:
        return {
            "success": False,
            "stdout": "",
            "stderr": "AXLE request timed out.",
        }

    except requests.RequestException as e:
        return {
            "success": False,
            "stdout": "",
            "stderr": f"AXLE request failed: {e}",
        }

    except (KeyError, ValueError) as e:
        return {
            "success": False,
            "stdout": "",
            "stderr": f"Invalid response from AXLE: {e}",
        }

