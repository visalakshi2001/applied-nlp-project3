
# Claim: Cellular clocks are associated with mitosis timing in NIH 3T3 cells.
# The simulation will model the interaction between circadian cycles and cell division timing in NIH 3T3 cells.

from simulation_utils import GameObject, Container

class Cell(GameObject):
    def __init__(self, name, circadian_cycle_time=24, division_time=0):
        super().__init__(name)
        self.properties = {
            "circadian_cycle_time": circadian_cycle_time,  # in hours
            "division_time": division_time,  # time of next division in hours
            "last_division_time": 0  # last division time in hours
        }

    def tick(self):
        # Update the division time based on the circadian cycle
        if self.properties["last_division_time"] + 5 <= self.properties["circadian_cycle_time"]:
            self.properties["division_time"] = self.properties["last_division_time"] + 5
        else:
            self.properties["division_time"] = self.properties["circadian_cycle_time"]

    def makeDescriptionStr(self):
        description = (f"{self.name}: Circadian cycle time is {self.properties['circadian_cycle_time']} hours, "
                       f"next division time is in {self.properties['division_time']} hours, "
                       f"last division was at {self.properties['last_division_time']} hours.")
        return description

class World(Container):
    def __init__(self):
        super().__init__("NIH 3T3 Cell Environment")

    def makeDescriptionStr(self):
        outStr = f"In the {self.name}, you see: \n"
        for obj in self.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"
        return outStr

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()

    def _initialize_simulation(self):
        world = World()
        cell1 = Cell("NIH 3T3 Cell 1", circadian_cycle_time=24)
        cell2 = Cell("NIH 3T3 Cell 2", circadian_cycle_time=24)
        world.addObject(cell1)
        world.addObject(cell2)
        return world

    def step(self):
        # Do one tick of the environment
        self.doWorldTick()
        return self.rootObject.makeDescriptionStr()

    def doWorldTick(self):
        # Get a list of all objects in the environment
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        # Loop through all objects, and call their tick()
        for obj in allObjects:
            obj.tick()

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    
    # Simulate for a few ticks to observe the behavior
    for _ in range(5):
        print("Ticking...")
        obs = simulation.step()
        print(obs)
        print()

if __name__ == "__main__":
    main()
