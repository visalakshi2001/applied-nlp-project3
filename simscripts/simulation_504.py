
# Claim: Healthy volunteers exhibit rapid and transient increase of cellular ATP after being bolus-injected with fructose.

from simulation_utils import GameObject, Container

class Volunteer(GameObject):
    def __init__(self, name, initial_atp=100):
        super().__init__(name)
        self.properties = {
            "initial_atp": initial_atp,
            "current_atp": initial_atp,
            "fructose_injected": False
        }

    def inject_fructose(self):
        self.properties["fructose_injected"] = True
        self.properties["current_atp"] -= 20  # Simulate ATP decrease after injection
        return f"{self.name} has been injected with fructose. Current ATP: {self.properties['current_atp']}"

    def recover_atp(self):
        if self.properties["fructose_injected"]:
            self.properties["current_atp"] += 30  # Simulate ATP recovery
            return f"{self.name} has recovered ATP. Current ATP: {self.properties['current_atp']}"
        return f"{self.name} has not been injected with fructose."

class Simulation:
    def __init__(self):
        self.volunteer = Volunteer("Healthy Volunteer")
        self.observationStr = self.volunteer.makeDescriptionStr()

    def step(self):
        # Simulate fructose injection
        injection_result = self.volunteer.inject_fructose()
        
        # Simulate recovery after 1 hour
        recovery_result = self.volunteer.recover_atp()
        
        return injection_result, recovery_result

def main():
    simulation = Simulation()
    injection_result, recovery_result = simulation.step()
    
    print(injection_result)
    print(recovery_result)

    # Check if the claim is supported or refuted
    if simulation.volunteer.properties["current_atp"] > simulation.volunteer.properties["initial_atp"]:
        print("Claim Supported: Healthy volunteers exhibit rapid and transient increase of cellular ATP after being bolus-injected with fructose.")
    else:
        print("Claim Refuted: Healthy volunteers do not exhibit rapid and transient increase of cellular ATP after being bolus-injected with fructose.")

if __name__ == "__main__":
    main()
