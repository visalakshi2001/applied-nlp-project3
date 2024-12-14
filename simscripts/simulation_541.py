
# Claim: Hypothalamic glutamate neurotransmission is unrelated to energy balance.
# The simulation will evaluate the role of glutamate in energy balance based on the provided reference text.

from simulation_utils import GameObject, Container

class Neuron(GameObject):
    def __init__(self, name, glutamate_release=0):
        super().__init__(name)
        self.properties = {
            "glutamate_release": glutamate_release,
            "energy_balance": 100  # Starting energy balance
        }

    def tick(self):
        # Glutamate release affects energy balance
        if self.properties["glutamate_release"] > 0:
            self.properties["energy_balance"] += self.properties["glutamate_release"] * 10  # Arbitrary effect on energy balance
        else:
            self.properties["energy_balance"] -= 5  # Decrease energy balance if no glutamate is released

    def makeDescriptionStr(self):
        description = f"A {self.name} neuron, with glutamate release level at {self.properties['glutamate_release']} and energy balance at {self.properties['energy_balance']}."
        return description

class VMHNeuron(Neuron):
    def __init__(self, name):
        super().__init__(name)
        self.properties["glutamate_release"] = 5  # Default glutamate release for VMH neurons

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("hypothalamus")
        vmh_neuron = VMHNeuron("VMH Neuron")
        world.addObject(vmh_neuron)
        return world

    def makeNameToObjectDict(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        nameToObjectDict = {}
        for obj in allObjects:
            nameToObjectDict[obj.name] = [obj]
        return nameToObjectDict

    def generatePossibleActions(self):
        allObjects = self.makeNameToObjectDict()
        self.possibleActions = {}
        self.addAction("look", ["look"])
        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction(f"increase glutamate release of {objReferent}", ["increase", obj])
                self.addAction(f"decrease glutamate release of {objReferent}", ["decrease", obj])

    def addAction(self, actionStr, actionArgs):
        if actionStr not in self.possibleActions:
            self.possibleActions[actionStr] = actionArgs

    def actionIncrease(self, neuron):
        if type(neuron) != Neuron:
            return f"Cannot increase the glutamate release of {neuron.name}."
        else:
            neuron.properties["glutamate_release"] += 1
            return f"You increase the glutamate release of {neuron.name} by 1."

    def actionDecrease(self, neuron):
        if type(neuron) != Neuron:
            return f"Cannot decrease the glutamate release of {neuron.name}."
        else:
            neuron.properties["glutamate_release"] -= 1
            return f"You decrease the glutamate release of {neuron.name} by 1."

    def step(self, actionStr):
        self.observationStr = ""
        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "increase":
            self.observationStr = self.actionIncrease(action[1])
        elif actionVerb == "decrease":
            self.observationStr = self.actionDecrease(action[1])

        self.doWorldTick()
        return self.observationStr

    def doWorldTick(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            obj.tick()

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["look", "increase glutamate release of VMH Neuron", "look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

    # Final check of energy balance to determine claim support
    vmh_neuron = simulation.rootObject.containsItemWithName("VMH Neuron")[0]
    if vmh_neuron.properties["energy_balance"] > 100:
        print("Claim Refuted: Glutamate neurotransmission is related to energy balance.")
    else:
        print("Claim Supported: Glutamate neurotransmission is unrelated to energy balance.")

if __name__ == "__main__":
    main()
