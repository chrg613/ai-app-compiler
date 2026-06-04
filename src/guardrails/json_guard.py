import json


class JSONGuard:

    @staticmethod
    def validate(
        raw_response: str
    ) -> bool:

        try:

            json.loads(
                raw_response
            )

            return True

        except Exception:

            return False