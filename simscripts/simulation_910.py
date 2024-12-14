
# Claim: PKG-la does not have a large impact on expression of spinal long term potentiation in PGK-la knockout mice.
# The simulation will test the impact of PKG-I on spinal long-term potentiation (LTP) in knockout mice.

from simulation_utils import GameObject, Container

class Neuron(GameObject):
    def __init__(self, name, pkgi_expression=0):
        super().__init__(name)
        self.pkgi_expression = pkgi_expression  # Represents the expression level of PKG-I

    def express_ltp(self):
        # If PKG-I is expressed, LTP occurs; if not, LTP is abolished
        if self.pkgi_expression > 0:
            return "LTP is expressed."
        else:
            return "LTP is abolished."

class KnockoutMouse(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.neuron = Neuron("spinal_neuron", pkgi_expression=0)  # PKG-I is knocked out

    def test_ltp_expression(self):
        return self.neuron.express_ltp()

class Simulation:
    def __init__(self):
        self.knockout_mouse = KnockoutMouse("SNS-PKG-I(-/-) mouse")
        self.result = self.knockout_mouse.test_ltp_expression()

    def run(self):
        return self.result

def main():
    simulation = Simulation()
    result = simulation.run()
    print(result)

    # Determine if the claim is supported or refuted based on the result
    if "LTP is abolished" in result:
        print("Claim is Refuted: PKG-I has a large impact on expression of spinal long term potentiation.")
    else:
        print("Claim is Supported: PKG-I does not have a large impact on expression of spinal long term potentiation.")

if __name__ == "__main__":
    main()
