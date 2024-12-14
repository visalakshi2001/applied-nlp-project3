
# Claim: Therapeutics receiving accelerated approval encounter a lower frequency of post-marketing safety events
# The simulation will model the relationship between therapeutics and their post-marketing safety events based on the claim.

from simulation_utils import GameObject, Container

class Therapeutic(GameObject):
    def __init__(self, name, accelerated_approval=False):
        super().__init__(name)
        self.properties = {
            "accelerated_approval": accelerated_approval,
            "post_market_events": 0
        }

    def evaluate_post_market_events(self):
        # Simulate the frequency of post-market safety events based on accelerated approval status
        if self.properties["accelerated_approval"]:
            self.properties["post_market_events"] = 2.20  # Higher frequency
        else:
            self.properties["post_market_events"] = 1.0  # Baseline frequency

    def makeDescriptionStr(self):
        description = f"{self.name} (Accelerated Approval: {self.properties['accelerated_approval']}, Post-Market Events: {self.properties['post_market_events']})"
        return description

class World(Container):
    def __init__(self):
        Container.__init__(self, "therapeutics_environment")

    def makeDescriptionStr(self):
        outStr = f"In the {self.name}, you see: \n"
        for obj in self.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"
        return outStr

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.run_simulation()

    def _initialize_simulation(self):
        world = World()
        therapeutic1 = Therapeutic("Therapeutic A", accelerated_approval=True)
        therapeutic2 = Therapeutic("Therapeutic B", accelerated_approval=False)
        world.addObject(therapeutic1)
        world.addObject(therapeutic2)
        return world

    def run_simulation(self):
        # Evaluate post-market events for each therapeutic
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            if isinstance(obj, Therapeutic):
                obj.evaluate_post_market_events()

    def print_results(self):
        print(self.observationStr)

def main():
    simulation = Simulation()
    simulation.print_results()

if __name__ == "__main__":
    main()
