
# Claim: Walking in traffic areas in London improves lung function in elderly adults.
# The simulation will assess the effects of walking in a high pollution area (Oxford Street) versus a low pollution area (Hyde Park) on lung function.

from simulation_utils import GameObject, Container

class Participant(GameObject):
    def __init__(self, name, lung_function=100, pollution_exposure=0):
        super().__init__(name)
        self.lung_function = lung_function
        self.pollution_exposure = pollution_exposure

    def walk(self, area):
        if area == "Oxford Street":
            self.pollution_exposure += 50  # High pollution exposure
            self.lung_function -= 10  # Decrease in lung function due to pollution
        elif area == "Hyde Park":
            self.pollution_exposure += 10  # Low pollution exposure
            self.lung_function += 5  # Increase in lung function due to clean air

    def makeDescriptionStr(self):
        return f"{self.name} has a lung function of {self.lung_function} and pollution exposure of {self.pollution_exposure}."

class World(Container):
    def __init__(self):
        Container.__init__(self, "environment")

    def makeDescriptionStr(self):
        outStr = f"In the {self.name}, you see: \n"
        for obj in self.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"
        return outStr

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.simulate_walks()

    def _initialize_simulation(self):
        world = World()
        participant1 = Participant("Elderly Participant 1")
        participant2 = Participant("Elderly Participant 2")
        world.addObject(participant1)
        world.addObject(participant2)
        return world

    def simulate_walks(self):
        # Simulate walking in Oxford Street
        for participant in self.rootObject.contains:
            participant.walk("Oxford Street")
        
        # Simulate walking in Hyde Park
        for participant in self.rootObject.contains:
            participant.walk("Hyde Park")

    def check_claim(self):
        # Check the lung function of participants after both walks
        results = []
        for participant in self.rootObject.contains:
            results.append((participant.name, participant.lung_function))
        
        # If any participant has improved lung function after walking in Hyde Park, claim is supported
        if any(lung_function > 100 for _, lung_function in results):
            return "Claim Supported: Walking in traffic areas does not improve lung function."
        else:
            return "Claim Refuted: Walking in traffic areas does not improve lung function."

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    print(simulation.check_claim())

if __name__ == "__main__":
    main()
