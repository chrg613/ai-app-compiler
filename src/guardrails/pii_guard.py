import re


class PIIGuard:

    EMAIL_PATTERN = (
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    )

    @staticmethod
    def contains_pii(
        text: str
    ) -> bool:

        return bool(
            re.search(
                PIIGuard.EMAIL_PATTERN,
                text
            )
        )