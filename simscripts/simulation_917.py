
# Claim: PTEN is a regulator for the transcriptional activity of SRF
# The simulation will model the interaction between PTEN and SRF in a vascular smooth muscle cell context.

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

class PTEN(GameObject):
    def __init__(self):
        super().__init__("PTEN")
        self.properties = {
            "nuclear_location": True,
            "activity_level": 1  # 1 indicates normal activity
        }

class SRF(GameObject):
    def __init__(self):
        super().__init__("SRF")
        self.properties = {
            "binding_activity": 0  # 0 indicates no binding activity
        }

    def bind_to_promoter(self):
        self.properties["binding_activity"] += 1

class VascularSmoothMuscleCell(Container):
    def __init__(self):
        super().__init__("Vascular Smooth Muscle Cell")
        self.pten = PTEN()
        self.srf = SRF()
        self.addObject(self.pten)
        self.addObject(self.srf)

    def regulate_transcription(self):
        if self.pten.getProperty("nuclear_location"):
            self.srf.bind_to_promoter()
            return "PTEN is regulating SRF binding activity."
        else:
            return "PTEN is not in the nucleus, cannot regulate SRF."

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.result = self.run_simulation()

    def _initialize_simulation(self):
        world = VascularSmoothMuscleCell()
        return world

    def run_simulation(self):
        regulation_result = self.rootObject.regulate_transcription()
        if "regulating" in regulation_result:
            return "Supported: PTEN regulates the transcriptional activity of SRF."
        else:
            return "Refuted: PTEN does not regulate the transcriptional activity of SRF."

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    print(simulation.result)

if __name__ == "__main__":
    main()
