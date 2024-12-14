
# Claim: Hypocretin neurones suppress panicprone state in rats.
# The simulation will model the relationship between hypocretin (orexin) neurons and panic-prone states in rats.

from simulation_utils import GameObject, Container

class HypocretinNeuron(GameObject):
    def __init__(self, name, activity_level=0):
        super().__init__(name)
        self.activity_level = activity_level  # Represents the activity level of the hypocretin neuron

    def tick(self):
        # Hypocretin neuron activity can influence panic-prone state
        if self.activity_level > 0:
            self.activity_level -= 1  # Decrease activity over time
        else:
            self.activity_level = 0  # Prevent negative activity

class PanicState(GameObject):
    def __init__(self, name, intensity=0):
        super().__init__(name)
        self.intensity = intensity  # Represents the intensity of the panic state

    def tick(self):
        # Panic state intensity can increase if hypocretin activity is low
        if self.intensity < 10:  # Maximum intensity
            self.intensity += 1  # Increase intensity over time

class Rat(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.hypocretin_neuron = HypocretinNeuron("Hypocretin Neuron")
        self.panic_state = PanicState("Panic State")

    def tick(self):
        # Update the state of the rat
        self.hypocretin_neuron.tick()
        self.panic_state.tick()

        # If hypocretin neuron activity is low, increase panic state intensity
        if self.hypocretin_neuron.activity_level == 0:
            self.panic_state.intensity += 1

class World(Container):
    def __init__(self):
        super().__init__("environment")
        self.rat = Rat("Rat")

    def makeDescriptionStr(self):
        return f"In the {self.name}, you see: \n" + self.rat.makeDescriptionStr()

def main():
    world = World()
    print(world.makeDescriptionStr())
    
    # Simulate for a number of ticks to observe the behavior
    for tick in range(10):
        print(f"Tick {tick + 1}:")
        world.rat.tick()
        print(f"Hypocretin Neuron Activity Level: {world.rat.hypocretin_neuron.activity_level}")
        print(f"Panic State Intensity: {world.rat.panic_state.intensity}")
        print()

        # Check if the claim is supported or refuted
        if world.rat.hypocretin_neuron.activity_level == 0 and world.rat.panic_state.intensity > 0:
            print("Claim Refuted: Hypocretin neurones do not suppress panic-prone state.")
            return
        elif world.rat.hypocretin_neuron.activity_level > 0 and world.rat.panic_state.intensity == 0:
            print("Claim Supported: Hypocretin neurones suppress panic-prone state.")
            return

    print("Claim Supported: Hypocretin neurones suppress panic-prone state.")

if __name__ == "__main__":
    main()
