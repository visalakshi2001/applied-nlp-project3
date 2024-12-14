
# Claim: Vitamin D is an important factor in the relationship between calcium and parathyroid hormone.

from simulation_utils import GameObject, Container

class VitaminD(GameObject):
    def __init__(self, level):
        super().__init__("Vitamin D")
        self.level = level  # in ng/mL
        self.properties = {
            "level": level
        }

class Calcium(GameObject):
    def __init__(self, intake):
        super().__init__("Calcium")
        self.intake = intake  # in mg/d
        self.properties = {
            "intake": intake
        }

class ParathyroidHormone(GameObject):
    def __init__(self):
        super().__init__("Parathyroid Hormone")
        self.level = 0  # Initial level
        self.properties = {
            "level": self.level
        }

    def update_level(self, vitamin_d, calcium):
        if vitamin_d.level < 10:
            if calcium.intake < 800:
                self.level = 1  # High PTH level
            else:
                self.level = 0.5  # Moderate PTH level
        elif vitamin_d.level > 18:
            self.level = 0  # Low PTH level
        else:
            self.level = 0.75  # Moderate PTH level

class World(Container):
    def __init__(self):
        super().__init__("Bone Health Environment")
        self.vitamin_d = VitaminD(0)  # Initial level of Vitamin D
        self.calcium = Calcium(0)  # Initial calcium intake
        self.pth = ParathyroidHormone()  # Parathyroid hormone object
        self.addObject(self.vitamin_d)
        self.addObject(self.calcium)
        self.addObject(self.pth)

    def simulate(self):
        # Simulate different scenarios
        scenarios = [
            (5, 700),   # Low Vitamin D, low calcium
            (5, 1200),  # Low Vitamin D, high calcium
            (20, 700),  # High Vitamin D, low calcium
            (20, 1200)  # High Vitamin D, high calcium
        ]
        
        results = []
        for vitamin_d_level, calcium_intake in scenarios:
            self.vitamin_d.level = vitamin_d_level
            self.calcium.intake = calcium_intake
            self.pth.update_level(self.vitamin_d, self.calcium)
            results.append((vitamin_d_level, calcium_intake, self.pth.level))
        
        return results

def main():
    world = World()
    results = world.simulate()
    
    for vitamin_d_level, calcium_intake, pth_level in results:
        print(f"Vitamin D Level: {vitamin_d_level} ng/mL, Calcium Intake: {calcium_intake} mg/d, PTH Level: {pth_level}")
    
    # Check if the claim is supported or refuted
    # Claim states that Vitamin D is important for the relationship between calcium and PTH
    # If PTH level changes with varying Vitamin D and Calcium, the claim is supported
    if any(pth_level == 1 for _, _, pth_level in results) and any(pth_level == 0 for _, _, pth_level in results):
        print("Claim Supported: Vitamin D is an important factor in the relationship between calcium and parathyroid hormone.")
    else:
        print("Claim Refuted: Vitamin D is not an important factor in the relationship between calcium and parathyroid hormone.")

if __name__ == "__main__":
    main()
