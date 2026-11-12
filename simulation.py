from collections import deque


class SimulationEngine:
    def __init__(self, design_name: str, parameters: dict, max_history: int = 1000):
        self.design_name = design_name
        self.parameters = parameters.copy()
        self.time_step = 0.0

        # Keep only the most recent steps to limit memory use.
        self.history = deque(maxlen=max_history)

    def update_physics(self, delta_time: float) -> None:
        self.time_step += delta_time

        base_load = self.parameters.get("base_load", 10)
        current_stress = base_load * (1 + self.time_step * 0.1)
        self.parameters["current_stress"] = current_stress

        self.history.append({
            "time": self.time_step,
            "stress": current_stress,
        })

    def run_ai_prediction(self) -> str:
        # This is a threshold check, not an AI model yet.
        max_limit = self.parameters.get("failure_threshold", 50.0)
        current_stress = self.parameters.get("current_stress", 0.0)

        if current_stress >= max_limit:
            return (
                f"WARNING: Possible failure at t={self.time_step:.1f}s. "
                f"Stress ({current_stress:.1f}) reached the threshold."
            )

        return (
            f"Status nominal at t={self.time_step:.1f}s. "
            f"Stress: {current_stress:.1f}."
        )


if __name__ == "__main__":
    simulator = SimulationEngine(
        design_name="Prototype-Alpha-Beam",
        parameters={"base_load": 15.0, "failure_threshold": 45.0},
    )

    for _ in range(6):
        simulator.update_physics(delta_time=1.0)
        print(simulator.run_ai_prediction())
