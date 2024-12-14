
# Claim: One in two surgical randomized controlled trials are discontinued early.
# The simulation will check the rate of early discontinuation of surgical randomized controlled trials.

class GameObject():
    def __init__(self, name):
        if hasattr(self, "constructorsRun"):
            return
        self.constructorsRun = ["GameObject"]
        self.name = name
        self.parent = None
        self.contains = []
        self.properties = {}

    def getProperty(self, propertyName):
        if propertyName in self.properties:
            return self.properties[propertyName]
        else:
            return None

    def addObject(self, obj):
        obj.removeSelfFromContainer()
        self.contains.append(obj)
        obj.parent = self

    def removeObject(self, obj):
        self.contains.remove(obj)
        obj.parent = None

    def removeSelfFromContainer(self):
        if self.parent != None:
            self.parent.removeObject(self)

    def getAllContainedObjectsRecursive(self):
        outList = []
        for obj in self.contains:
            outList.append(obj)
            outList.extend(obj.getAllContainedObjectsRecursive())
        return outList

    def containsItemWithName(self, name):
        foundObjects = []
        for obj in self.contains:
            if obj.name == name:
                foundObjects.append(obj)
        return foundObjects

    def tick(self):
        pass

    def makeDescriptionStr(self):
        return self.name

class Container(GameObject):
    def __init__(self, name):
        if hasattr(self, "constructorsRun"):
            if "Container" in self.constructorsRun:
                return
        GameObject.__init__(self, name)
        self.constructorsRun.append("Container")
        self.properties["isContainer"] = True
        self.properties["isOpenable"] = False
        self.properties["isOpen"] = True
        self.properties["containerPrefix"] = "in"

class Trial(GameObject):
    def __init__(self, name, discontinued=False):
        super().__init__(name)
        self.properties["discontinued"] = discontinued

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.calculate_discontinuation_rate()

    def _initialize_simulation(self):
        world = Container("Surgical Trials Environment")
        # Create 395 trials, with 81 discontinued (21%)
        for i in range(395):
            if i < 81:  # First 81 trials are discontinued
                trial = Trial(f"Trial_{i+1}", discontinued=True)
            else:
                trial = Trial(f"Trial_{i+1}", discontinued=False)
            world.addObject(trial)
        return world

    def calculate_discontinuation_rate(self):
        trials = self.rootObject.getAllContainedObjectsRecursive()
        total_trials = len(trials)
        discontinued_trials = sum(1 for trial in trials if trial.getProperty("discontinued"))
        self.discontinuation_rate = discontinued_trials / total_trials

    def check_claim(self):
        if self.discontinuation_rate >= 0.5:
            return "Claim Supported: One in two surgical randomized controlled trials are discontinued early."
        else:
            return "Claim Refuted: One in two surgical randomized controlled trials are not discontinued early."

def main():
    simulation = Simulation()
    print(simulation.check_claim())

if __name__ == "__main__":
    main()
