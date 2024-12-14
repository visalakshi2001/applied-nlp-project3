
# Claim: Gpr124 suppresses BBB breakdown in mouse models of ischemic stroke.
# The simulation will model the effects of Gpr124 knockout on BBB integrity in mouse models of ischemic stroke.

from simulation_utils import GameObject, Container

class MouseModel(GameObject):
    def __init__(self, name, gpr124_active=True):
        super().__init__(name)
        self.gpr124_active = gpr124_active
        self.bbb_integrity = True  # True means BBB is intact, False means BBB is disrupted

    def simulate_stroke(self):
        if not self.gpr124_active:
            self.bbb_integrity = False  # Gpr124 knockout leads to BBB disruption
        else:
            self.bbb_integrity = True  # Gpr124 active maintains BBB integrity

    def makeDescriptionStr(self):
        status = "intact" if self.bbb_integrity else "disrupted"
        return f"A mouse model named {self.name} with Gpr124 {'active' if self.gpr124_active else 'knockout'}, BBB is {status}."

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.run_simulation()

    def _initialize_simulation(self):
        world = Container("environment")
        mouse_with_gpr124 = MouseModel("Mouse_with_Gpr124", gpr124_active=True)
        mouse_without_gpr124 = MouseModel("Mouse_without_Gpr124", gpr124_active=False)
        world.addObject(mouse_with_gpr124)
        world.addObject(mouse_without_gpr124)
        return world

    def run_simulation(self):
        # Simulate stroke in both mouse models
        for mouse in self.rootObject.contains:
            mouse.simulate_stroke()

    def makeDescriptionStr(self):
        outStr = f"In the {self.rootObject.name}, you see: \n"
        for obj in self.rootObject.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"
        return outStr

def main():
    simulation = Simulation()
    print(simulation.makeDescriptionStr())

if __name__ == "__main__":
    main()
