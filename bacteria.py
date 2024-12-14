from simulation_utils import GameObject, Container

class Bacteria(GameObject):
    def __init__(self, name, ethanol_stress=0, IBP=0, PSP=0, SRL=0):
        super().__init__(name)
        self.name = name
        self.properties = {
            "ethanol_stress": ethanol_stress,
            "IBP": IBP,
            "PSP": PSP,
            "SRL": SRL
        }

    def tick(self):
        self.properties["IBP"] = self.properties["ethanol_stress"]
        self.properties["PSP"] = 2 * self.properties["ethanol_stress"] # 2 is just an arbitary number here
        self.properties["SRL"] = - self.properties["ethanol_stress"]

    def makeDescriptionStr(self):
        description = f"A {self.name}, whose current ethonal stress is {self.properties['ethanol_stress']}, IBP is {self.properties['IBP']}, PSP is {self.properties['PSP']}, and SRL is {self.properties['SRL']}."
        return description

# The world is the root object of the game object tree.
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
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = World()
        bacteria1 = Bacteria("bacteria_1")
        bacteria2 = Bacteria("bacteria_2")
        world.addObject(bacteria1)
        world.addObject(bacteria2)        
        return world

    # Make a dictionary whose keys are object names (strings), and whose values are lists of object references with those names.
    # This is useful for generating valid actions, and parsing user input.
    def makeNameToObjectDict(self):
        # Get a list of all game objects
        allObjects = self.rootObject.getAllContainedObjectsRecursive()

        # Make a dictionary whose keys are object names (strings), and whose values are lists of object references with those names.
        nameToObjectDict = {}
        for obj in allObjects:
            nameToObjectDict[obj.name] = [obj]

        return nameToObjectDict

    def addAction(self, actionStr, actionArgs):
        # Check whether the action string key already exists -- if not, add a blank list
        if actionStr not in self.possibleActions:
            self.possibleActions[actionStr] = actionArgs

    # Returns a list of valid actions at the current time step
    def generatePossibleActions(self):
        # Get a list of all game objects that could serve as arguments to actions
        allObjects = self.makeNameToObjectDict()

        # Make a dictionary whose keys are possible action strings, and whose values are lists that contain the arguments.
        self.possibleActions = {}

        self.addAction("look", ["look"])

        # (1-arg) Increase ethanol stress of a bacteria
        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction(f"increase ethanol stress of {objReferent}", ["increase", obj])

        # (1-arg) Increase ethanol stress of a bacteria
        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction(f"decrease ethanol stress of {objReferent}", ["decrease", obj])

    def actionIncrease(self, bacteria):
        if type(bacteria) != Bacteria:
            return f"Cannot increase the ethanol stress of {bacteria.name}."
        else:
            bacteria.properties["ethanol_stress"] += 1
            return f"You increase the ethanol stress of {bacteria.name} by 1."
        
    def actionDecrease(self, bacteria):
        if type(bacteria) != Bacteria:
            return f"Cannot increase the ethanol stress of {bacteria.name}."
        else:
            bacteria.properties["ethanol_stress"] -= 1
            return f"You decrease the ethanol stress of {bacteria.name} by 1."

    def step(self, actionStr):
        self.observationStr = ""

        # Check to make sure the action is in the possible actions dictionary
        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        # Find the action in the possible actions dictionary
        action = self.possibleActions[actionStr]

        # Interpret the action
        actionVerb = action[0]


        if (actionVerb == "look"):
            # Look around the environment -- i.e. show the description of the world.
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif (actionVerb == "increase"):
            # increase ethanol stress 
            self.observationStr = self.actionIncrease(action[1])
        elif (actionVerb == "decrease"):
            # decrease ethanol stress
            self.observationStr = self.actionDecrease(action[1])

        
        # Catch-all
        else:
            self.observationStr = "ERROR: Unknown action."

        # Do one tick of the environment
        self.doWorldTick()

        # Update possible actions
        self.generatePossibleActions()

        return self.observationStr


    # Call the object update for each object in the environment
    def doWorldTick(self):
        # Get a list of all objects in the environment
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        # Loop through all objects, and call their tick()
        for obj in allObjects:
            obj.tick()

def main():
    simuation = Simulation()
    print(simuation.observationStr)
    actions = ["increase ethanol stress of bacteria_1", "decrease ethanol stress of bacteria_2", "look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simuation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()

    