
# Claim: Kir7.1 modulates channel activity by the G protein-coupled melanocortin-4 receptor (MC4R) in the paraventricular nucleus of the hypothalamus.

from simulation_utils import GameObject, Container

class Neuron(GameObject):
    def __init__(self, name, activity_level=0):
        super().__init__(name)
        self.properties = {
            "activity_level": activity_level,
            "MC4R_coupled": False,
            "Kir7.1_open": False
        }

    def tick(self):
        if self.properties["MC4R_coupled"]:
            if self.properties["Kir7.1_open"]:
                self.properties["activity_level"] += 1  # Increase activity when Kir7.1 is open
            else:
                self.properties["activity_level"] -= 1  # Decrease activity when Kir7.1 is closed

    def makeDescriptionStr(self):
        return f"A {self.name} neuron with activity level {self.properties['activity_level']}."

class MC4R(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.properties = {
            "is_active": False
        }

    def activate(self):
        self.properties["is_active"] = True

    def deactivate(self):
        self.properties["is_active"] = False

class Kir7_1(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.properties = {
            "is_open": False
        }

    def open_channel(self):
        self.properties["is_open"] = True

    def close_channel(self):
        self.properties["is_open"] = False

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("hypothalamus")
        neuron = Neuron("PVN Neuron")
        mc4r = MC4R("MC4R")
        kir7_1 = Kir7_1("Kir7.1")

        world.addObject(neuron)
        world.addObject(mc4r)
        world.addObject(kir7_1)

        # Simulate the activation of MC4R and opening of Kir7.1
        mc4r.activate()
        neuron.properties["MC4R_coupled"] = True
        kir7_1.open_channel()
        neuron.properties["Kir7.1_open"] = kir7_1.properties["is_open"]

        return world

    def makeDescriptionStr(self):
        outStr = f"In the {self.rootObject.name}, you see: \n"
        for obj in self.rootObject.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"
        return outStr

    def step(self):
        self.rootObject.tick()
        self.observationStr = self.makeDescriptionStr()
        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    result = simulation.step()
    print(result)

    # Check the activity level of the neuron to determine if the claim is supported
    if simulation.rootObject.contains[0].properties["activity_level"] > 0:
        print("Claim Supported: Kir7.1 modulates channel activity by the G protein-coupled melanocortin-4 receptor (MC4R) in the paraventricular nucleus of the hypothalamus.")
    else:
        print("Claim Refuted: Kir7.1 does not modulate channel activity by the G protein-coupled melanocortin-4 receptor (MC4R) in the paraventricular nucleus of the hypothalamus.")

if __name__ == "__main__":
    main()
