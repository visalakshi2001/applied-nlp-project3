
# Claim: Cyclin A2 destruction is necessary to switch from unstable to stable kt-mt attachments in mitosis.
# The simulation will model the relationship between cyclin A destruction and the stability of kinetochore-microtubule attachments.

from simulation_utils import GameObject, Container

class CyclinA(GameObject):
    def __init__(self, name, is_destroyed=False):
        super().__init__(name)
        self.is_destroyed = is_destroyed

    def destroy(self):
        self.is_destroyed = True

class KMTAttachment(GameObject):
    def __init__(self, name, stability="unstable"):
        super().__init__(name)
        self.stability = stability

    def stabilize(self):
        self.stability = "stable"

class Cell(Container):
    def __init__(self):
        super().__init__("Cell")
        self.cyclin_a = CyclinA("Cyclin A")
        self.kmt_attachment = KMTAttachment("Kinetochore-Microtubule Attachment")
        self.addObject(self.cyclin_a)
        self.addObject(self.kmt_attachment)

    def transition_to_metaphase(self):
        if not self.cyclin_a.is_destroyed:
            return "Cyclin A is present, preventing stabilization of k-MT attachments."
        else:
            self.kmt_attachment.stabilize()
            return "Cyclin A is destroyed, k-MT attachments are now stable."

class Simulation:
    def __init__(self):
        self.cell = Cell()
        self.result = ""

    def run(self):
        # First, check the state of the cell before destruction of Cyclin A
        self.result += self.cell.transition_to_metaphase() + "\n"
        
        # Now destroy Cyclin A
        self.cell.cyclin_a.destroy()
        
        # Check the state of the cell after destruction of Cyclin A
        self.result += self.cell.transition_to_metaphase() + "\n"
        
        return self.result

def main():
    simulation = Simulation()
    result = simulation.run()
    print(result)

if __name__ == "__main__":
    main()
