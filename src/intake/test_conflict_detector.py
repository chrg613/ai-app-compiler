from src.intake.conflict_detector import (
    ConflictDetector
)

prompt = """
Build a CRM.

No authentication.

Admins must login.
"""

result = (
    ConflictDetector.detect(
        prompt
    )
)

print(result)