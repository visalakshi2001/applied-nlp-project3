
# Claim: PKG-la plays an essential role in expression of spinal long term potentiation in PGK-la knockout mice.
# The simulation will test the role of PKG-I in spinal long-term potentiation (LTP) using knockout mice.

from simulation_utils import GameObject, Container

class Neuron(GameObject):
    def __init__(self, name, pkgi_present=True):
        super().__init__(name)
        self.pkgi_present = pkgi_present  # Indicates if PKG-I is present
        self.ltp_expressed = False  # Indicates if LTP is expressed

    def express_ltp(self):
        if self.pkgi_present:
            self.ltp_expressed = True
        else:
            self.ltp_expressed = False

    def makeDescriptionStr(self):
        return f"A {self.name} neuron with PKG-I present: {self.pkgi_present}, LTP expressed: {self.ltp_expressed}"

class KnockoutMouse(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.neuron = Neuron("spinal neuron", pkgi_present=False)  # PKG-I is knocked out

    def test_ltp_expression(self):
        self.neuron.express_ltp()

class WildTypeMouse(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.neuron = Neuron("spinal neuron", pkgi_present=True)  # PKG-I is present

    def test_ltp_expression(self):
        self.neuron.express_ltp()

class Simulation:
    def __init__(self):
        self.knockout_mouse = KnockoutMouse("PGK-la knockout mouse")
        self.wild_type_mouse = WildTypeMouse("Wild type mouse")
        self.results = {}

    def run_simulation(self):
        # Test LTP expression in both types of mice
        self.knockout_mouse.test_ltp_expression()
        self.wild_type_mouse.test_ltp_expression()

        # Collect results
        self.results["knockout_mouse_ltp"] = self.knockout_mouse.neuron.ltp_expressed
        self.results["wild_type_mouse_ltp"] = self.wild_type_mouse.neuron.ltp_expressed

    def make_description(self):
        return f"{self.knockout_mouse.neuron.makeDescriptionStr()}\n{self.wild_type_mouse.neuron.makeDescriptionStr()}"

def main():
    simulation = Simulation()
    simulation.run_simulation()
    print(simulation.make_description())
    
    # Determine if the claim is supported or refuted
    if not simulation.results["knockout_mouse_ltp"] and simulation.results["wild_type_mouse_ltp"]:
        print("Claim Supported: PKG-I plays an essential role in expression of spinal long term potentiation.")
    else:
        print("Claim Refuted: PKG-I does not play an essential role in expression of spinal long term potentiation.")

if __name__ == "__main__":
    main()
