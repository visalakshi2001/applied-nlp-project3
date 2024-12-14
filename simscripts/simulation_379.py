
# Claim: Enhanced early production of inflammatory chemokines damages viral control in the lung.
# The simulation will model the interaction between memory CD4+ T cells and the production of inflammatory chemokines in the lung during a viral infection.

from simulation_utils import GameObject, Container

class InflammatoryChemokine(GameObject):
    def __init__(self, name, production_rate=0):
        super().__init__(name)
        self.production_rate = production_rate

    def tick(self):
        # Simulate the production of inflammatory chemokines
        self.production_rate += 1  # Increase production rate over time

class MemoryCD4TCell(GameObject):
    def __init__(self, name, activation_level=0):
        super().__init__(name)
        self.activation_level = activation_level

    def enhance_inflammatory_response(self):
        # Enhance the production of inflammatory chemokines
        return 2 * self.activation_level  # Arbitrary enhancement factor

class Virus(GameObject):
    def __init__(self, name, control_level=100):
        super().__init__(name)
        self.control_level = control_level

    def tick(self, chemokine_production):
        # Simulate the effect of chemokine production on viral control
        self.control_level -= chemokine_production  # Viral control decreases with increased chemokine production

class World(Container):
    def __init__(self):
        super().__init__("lung environment")

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = World()
        chemokine = InflammatoryChemokine("chemokine")
        memory_t_cell = MemoryCD4TCell("memory_CD4_T_cell", activation_level=5)
        virus = Virus("influenza_virus")

        world.addObject(chemokine)
        world.addObject(memory_t_cell)
        world.addObject(virus)
        return world

    def makeNameToObjectDict(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        nameToObjectDict = {}
        for obj in allObjects:
            nameToObjectDict[obj.name] = [obj]
        return nameToObjectDict

    def step(self):
        chemokine = self.rootObject.containsItemWithName("chemokine")[0]
        memory_t_cell = self.rootObject.containsItemWithName("memory_CD4_T_cell")[0]
        virus = self.rootObject.containsItemWithName("influenza_virus")[0]

        # Simulate the production of inflammatory chemokines
        chemokine.tick()
        enhanced_production = memory_t_cell.enhance_inflammatory_response()
        virus.tick(enhanced_production)

        return f"Chemokine production rate: {chemokine.production_rate}, Virus control level: {virus.control_level}"

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    
    # Run the simulation for a few steps to observe the effects
    for _ in range(5):
        result = simulation.step()
        print(result)

    # Determine if the claim is supported or refuted based on the final virus control level
    final_virus_control = simulation.rootObject.containsItemWithName("influenza_virus")[0].control_level
    if final_virus_control < 100:  # Assuming 100 is the baseline control level
        print("Claim Supported: Enhanced early production of inflammatory chemokines damages viral control in the lung.")
    else:
        print("Claim Refuted: Enhanced early production of inflammatory chemokines does not damage viral control in the lung.")

if __name__ == "__main__":
    main()
