from src.models.contracts import (
    ApplicationIR
)

from src.state.state_manager import (
    StateManager
)

manager = StateManager()

ir = ApplicationIR(
    app_name="Drone System"
)

manager.save_ir(ir)

print(manager.current_version)

print(manager.history)

print(
    manager.get_current_ir()
)