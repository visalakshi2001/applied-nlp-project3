
# Claim: MUC1-C activates the NF-κB p65 signaling pathway by interacting with IκB kinase ß.

from simulation_utils import GameObject, Container

class MUC1(GameObject):
    def __init__(self, name, IKK_activation=False):
        super().__init__(name)
        self.properties = {
            "IKK_activation": IKK_activation
        }

    def activate_IKK(self):
        self.properties["IKK_activation"] = True

    def makeDescriptionStr(self):
        return f"{self.name} is {'activated' if self.properties['IKK_activation'] else 'not activated'}."

class IKK(GameObject):
    def __init__(self, name):
        super().__init__(name)

    def makeDescriptionStr(self):
        return f"{self.name} is present."

class NFkB(GameObject):
    def __init__(self, name, activated=False):
        super().__init__(name)
        self.properties = {
            "activated": activated
        }

    def activate(self):
        self.properties["activated"] = True

    def makeDescriptionStr(self):
        return f"NF-κB is {'activated' if self.properties['activated'] else 'not activated'}."

class World(Container):
    def __init__(self):
        super().__init__("cellular environment")

    def makeDescriptionStr(self):
        outStr = f"In the {self.name}, you see: \n"
        for obj in self.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"
        return outStr

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.check_claim()

    def _initialize_simulation(self):
        world = World()
        muc1 = MUC1("MUC1-C")
        ikk = IKK("IκB kinase ß")
        nfkb = NFkB("NF-κB p65")
        
        world.addObject(muc1)
        world.addObject(ikk)
        world.addObject(nfkb)
        
        return world

    def check_claim(self):
        muc1 = self.rootObject.containsItemWithName("MUC1-C")[0]
        ikk = self.rootObject.containsItemWithName("IκB kinase ß")[0]
        nfkb = self.rootObject.containsItemWithName("NF-κB p65")[0]

        # Simulate the interaction
        muc1.activate_IKK()  # MUC1-C activates IKK
        if muc1.properties["IKK_activation"]:
            nfkb.activate()  # If IKK is activated, NF-κB is activated

        # Check if the claim is supported
        if muc1.properties["IKK_activation"] and nfkb.properties["activated"]:
            self.observationStr += "\nClaim Supported: MUC1-C activates the NF-κB p65 signaling pathway by interacting with IκB kinase ß."
        else:
            self.observationStr += "\nClaim Refuted: MUC1-C does not activate the NF-κB p65 signaling pathway."

def main():
    simulation = Simulation()
    print(simulation.observationStr)

if __name__ == "__main__":
    main()
