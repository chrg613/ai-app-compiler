from src.guardrails.json_guard import (
    JSONGuard
)

from src.guardrails.pii_guard import (
    PIIGuard
)

print(
    JSONGuard.validate(
        '{"name":"CRM"}'
    )
)

print(
    PIIGuard.contains_pii(
        "contact me at test@gmail.com"
    )
)