from src.models.contracts import (
    ApplicationIR
)

from src.state.change_request import (
    ChangeRequest
)


class ChangeProcessor:

    @staticmethod
    def apply(
        ir: ApplicationIR,
        change: ChangeRequest
    ) -> ApplicationIR:

        if (
            change.action == "ADD"
            and change.target == "feature"
        ):

            if (
                change.value
                not in ir.features
            ):

                ir.features.append(
                    change.value
                )

        if (
            change.action == "REMOVE"
            and change.target == "feature"
        ):

            if (
                change.value
                in ir.features
            ):

                ir.features.remove(
                    change.value
                )

        return ir