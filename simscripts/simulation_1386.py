
# Claim: cSMAC formation represses weak ligand signalling.
# The simulation will model the relationship between cSMAC formation and T cell activation in response to weak and strong ligands.

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
        return self.properties.get(propertyName, None)

    def addObject(self, obj):
        obj.removeSelfFromContainer()
        self.contains.append(obj)
        obj.parent = self

    def removeObject(self, obj):
        self.contains.remove(obj)
        obj.parent = None

    def removeSelfFromContainer(self):
        if self.parent is not None:
            self.parent.removeObject(self)

    def getAllContainedObjectsRecursive(self):
        outList = []
        for obj in self.contains:
            outList.append(obj)
            outList.extend(obj.getAllContainedObjectsRecursive())
        return outList

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

class TCell(GameObject):
    def __init__(self, name, ligand_strength):
        super().__init__(name)
        self.properties = {
            "ligand_strength": ligand_strength,
            "cSMAC_formation": False,
            "activation_level": 0
        }

    def form_cSMAC(self):
        self.properties["cSMAC_formation"] = True
        self.update_activation()

    def update_activation(self):
        if self.properties["cSMAC_formation"]:
            if self.properties["ligand_strength"] == "weak":
                self.properties["activation_level"] = 1  # Repressed activation
            else:
                self.properties["activation_level"] = 5  # Strong activation
        else:
            self.properties["activation_level"] = 3  # Default activation without cSMAC

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.run_simulation()

    def _initialize_simulation(self):
        world = Container("T Cell Environment")
        weak_ligand_tcell = TCell("T Cell with Weak Ligand", "weak")
        strong_ligand_tcell = TCell("T Cell with Strong Ligand", "strong")
        world.addObject(weak_ligand_tcell)
        world.addObject(strong_ligand_tcell)
        return world

    def run_simulation(self):
        # Simulate cSMAC formation for weak ligand T cell
        weak_ligand_tcell = self.rootObject.contains[0]
        weak_ligand_tcell.form_cSMAC()

        # Check activation levels
        weak_activation = weak_ligand_tcell.properties["activation_level"]
        strong_ligand_tcell = self.rootObject.contains[1]
        strong_activation = strong_ligand_tcell.properties["activation_level"]

        # Determine claim support
        if weak_activation < strong_activation:
            self.result = "Supported"
        else:
            self.result = "Refuted"

    def makeDescriptionStr(self):
        outStr = f"In the {self.rootObject.name}, you see: \n"
        for obj in self.rootObject.contains:
            outStr += f"\t{obj.makeDescriptionStr()} with activation level: {obj.properties['activation_level']}\n"
        return outStr

def main():
    simulation = Simulation()
    print(simulation.rootObject.makeDescriptionStr())
    print(f"Claim verification result: {simulation.result}")

if __name__ == "__main__":
    main()
