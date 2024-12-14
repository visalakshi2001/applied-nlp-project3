
# Claim: Trans-acting factors, such as lncRNAs, influence mRNA translation.
# The simulation will model the interaction between lncRNA and mRNA translation influenced by a trans-acting factor (HuR).

from simulation_utils import GameObject, Container

class LncRNA(GameObject):
    def __init__(self, name, stability=0):
        super().__init__(name)
        self.stability = stability
        self.translation_efficiency = 0

    def tick(self, huR_level):
        if huR_level > 0:
            self.stability -= 1  # HuR decreases lncRNA stability
        else:
            self.stability += 1  # Reduced HuR increases lncRNA stability

        # Translation efficiency is inversely related to stability
        self.translation_efficiency = max(0, 10 - self.stability)

class mRNA(GameObject):
    def __init__(self, name, translation_rate=0):
        super().__init__(name)
        self.translation_rate = translation_rate

    def update_translation(self, lncRNA):
        # If lncRNA is stable, it inhibits translation
        if lncRNA.stability < 5:
            self.translation_rate = 0  # Translation is inhibited
        else:
            self.translation_rate = 10  # Translation occurs

class HuR(GameObject):
    def __init__(self, name, level=0):
        super().__init__(name)
        self.level = level

class World(Container):
    def __init__(self):
        super().__init__("cell environment")
        self.lncRNA = LncRNA("lincRNA-p21", stability=5)
        self.mRNA1 = mRNA("JUNB")
        self.mRNA2 = mRNA("CTNNB1")
        self.huR = HuR("HuR", level=0)

        self.addObject(self.lncRNA)
        self.addObject(self.mRNA1)
        self.addObject(self.mRNA2)
        self.addObject(self.huR)

    def tick(self):
        # Update lncRNA based on HuR level
        self.lncRNA.tick(self.huR.level)
        # Update mRNA translation based on lncRNA stability
        self.mRNA1.update_translation(self.lncRNA)
        self.mRNA2.update_translation(self.lncRNA)

class Simulation:
    def __init__(self):
        self.rootObject = World()
        self.rootObject.tick()  # Initial tick to set up the environment

    def change_huR_level(self, new_level):
        self.rootObject.huR.level = new_level
        self.rootObject.tick()  # Update the environment after changing HuR level

    def get_translation_rates(self):
        return {
            "JUNB_translation_rate": self.rootObject.mRNA1.translation_rate,
            "CTNNB1_translation_rate": self.rootObject.mRNA2.translation_rate,
            "lncRNA_stability": self.rootObject.lncRNA.stability
        }

def main():
    simulation = Simulation()
    
    # Initial state with HuR level 0
    print("Initial state with HuR level 0:")
    print(simulation.get_translation_rates())

    # Change HuR level to 1 (increasing HuR)
    simulation.change_huR_level(1)
    print("After increasing HuR level to 1:")
    print(simulation.get_translation_rates())

    # Change HuR level to 0 (decreasing HuR)
    simulation.change_huR_level(0)
    print("After decreasing HuR level to 0:")
    print(simulation.get_translation_rates())

if __name__ == "__main__":
    main()
