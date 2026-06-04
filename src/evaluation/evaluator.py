from src.evaluation.metrics import (
    Metrics
)


class Evaluator:

    @staticmethod
    def evaluate(
        successes,
        total
    ):

        return {
            "success_rate":
            Metrics.extraction_success_rate(
                successes,
                total
            )
        }