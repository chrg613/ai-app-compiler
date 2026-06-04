class Metrics:

    @staticmethod
    def extraction_success_rate(
        successes: int,
        total: int
    ):

        if total == 0:

            return 0

        return (
            successes / total
        )