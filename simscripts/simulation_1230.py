
# Claim: The minor G allele of FOXO3 downregulates pro-inflammatory cytokines.
# This simulation will model the effect of the minor G allele of FOXO3 on pro-inflammatory cytokines.

from simulation_utils import GameObject, Container

class Cytokine(GameObject):
    def __init__(self, name, level=0):
        super().__init__(name)
        self.level = level  # Level of cytokine production

    def tick(self):
        # The presence of the G allele reduces the level of pro-inflammatory cytokines
        self.level = max(0, self.level - 1)  # Reduce cytokine level, but not below 0

    def makeDescriptionStr(self):
        return f"{self.name} level is {self.level}."

class FOXO3(GameObject):
    def __init__(self, allele_type):
        super().__init__("FOXO3")
        self.allele_type = allele_type  # 'G' for minor allele, 'T' for major allele
        self.cytokines = [Cytokine("TNFα"), Cytokine("IL-6")]  # Pro-inflammatory cytokines

    def tick(self):
        if self.allele_type == 'G':
            # Minor G allele downregulates cytokines
            for cytokine in self.cytokines:
                cytokine.tick()  # Reduce cytokine levels
        else:
            # Major T allele does not downregulate cytokines
            for cytokine in self.cytokines:
                cytokine.level += 1  # Increase cytokine levels

    def makeDescriptionStr(self):
        cytokine_descriptions = "\n".join(cytokine.makeDescriptionStr() for cytokine in self.cytokines)
        return f"{self.name} with allele {self.allele_type}:\n{cytokine_descriptions}"

class World(Container):
    def __init__(self):
        super().__init__("environment")
        self.foxo3_g = FOXO3('G')  # FOXO3 with minor G allele
        self.foxo3_t = FOXO3('T')  # FOXO3 with major T allele
        self.addObject(self.foxo3_g)
        self.addObject(self.foxo3_t)

    def makeDescriptionStr(self):
        return super().makeDescriptionStr()

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        return World()

    def generatePossibleActions(self):
        self.possibleActions = {"look": ["look"]}

    def step(self, actionStr):
        if actionStr not in self.possibleActions:
            return "I don't understand that."

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        
        # Do one tick of the environment
        self.doWorldTick()

        return self.observationStr

    def doWorldTick(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            obj.tick()

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
