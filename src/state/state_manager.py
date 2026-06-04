from src.models.contracts import (
    ApplicationIR
)


class StateManager:

    def __init__(self):

        self.current_version = 1

        self.current_ir = None

        self.history = []

    def save_ir(
        self,
        ir: ApplicationIR
    ):

        self.current_ir = ir

        self.history.append(
            {
                "version": self.current_version,
                "app_name": ir.app_name
            }
        )

    def get_current_ir(self):

        return self.current_ir

    def create_new_version(self):

        self.current_version += 1