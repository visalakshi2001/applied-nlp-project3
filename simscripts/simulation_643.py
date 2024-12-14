
# Claim: Insulin effects appetite via ventral tegmental neurons.
# The simulation will model the effects of insulin on dopaminergic neurons in the ventral tegmental area (VTA) and their role in appetite regulation.

from simulation_utils import GameObject, Container

class Neuron(GameObject):
    def __init__(self, name, insulin_response=0):
        super().__init__(name)
        self.insulin_response = insulin_response  # Represents the firing frequency response to insulin

    def stimulate_insulin(self):
        # Simulate the effect of insulin on the neuron
        if self.insulin_response == 0:
            self.insulin_response = 1  # Insulin stimulates firing frequency
        else:
            self.insulin_response = 0  # Insulin response is abolished

    def makeDescriptionStr(self):
        return f"{self.name} with insulin response level: {self.insulin_response}"

class Mouse(Container):
    def __init__(self, name):
        super().__init__(name)
        self.neurons = []

    def add_neuron(self, neuron):
        self.addObject(neuron)
        self.neurons.append(neuron)

    def simulate_insulin_effect(self):
        for neuron in self.neurons:
            neuron.stimulate_insulin()

    def makeDescriptionStr(self):
        outStr = f"In {self.name}, you see: \n"
        for neuron in self.neurons:
            outStr += "\t" + neuron.makeDescriptionStr() + "\n"
        return outStr

class Simulation:
    def __init__(self):
        self.mouse = self._initialize_simulation()
        self.observationStr = self.mouse.makeDescriptionStr()
        self.generate_possible_actions()

    def _initialize_simulation(self):
        mouse = Mouse("IR(ΔTh) Mouse")
        neuron1 = Neuron("Dopaminergic VTA Neuron 1")
        neuron2 = Neuron("Dopaminergic VTA Neuron 2")
        mouse.add_neuron(neuron1)
        mouse.add_neuron(neuron2)
        return mouse

    def generate_possible_actions(self):
        self.possibleActions = {
            "stimulate insulin": ["stimulate insulin"]
        }

    def step(self, actionStr):
        self.observationStr = ""

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]

        if action[0] == "stimulate insulin":
            self.mouse.simulate_insulin_effect()
            self.observationStr = self.mouse.makeDescriptionStr()

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    
    # Simulate the effect of insulin
    action = "stimulate insulin"
    print(f"Action: {action}")
    obs = simulation.step(action)
    print(obs)

    # Check the insulin response to determine if the claim is supported or refuted
    if all(neuron.insulin_response == 0 for neuron in simulation.mouse.neurons):
        print("Claim Refuted: Insulin does not stimulate appetite via ventral tegmental neurons.")
    else:
        print("Claim Supported: Insulin stimulates appetite via ventral tegmental neurons.")

if __name__ == "__main__":
    main()
