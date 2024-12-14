
# Claim: Students who perform poorly in the early years of medical school are at increased risk for professional misconduct later in their careers.
# This simulation will model the relationship between early academic performance and later professional misconduct.

from simulation_utils import GameObject, Container

class Student(GameObject):
    def __init__(self, name, early_performance, misconduct_risk):
        super().__init__(name)
        self.properties = {
            "early_performance": early_performance,  # 0 = poor, 1 = average, 2 = good
            "misconduct_risk": misconduct_risk  # Probability of misconduct based on early performance
        }

    def assess_misconduct_risk(self):
        if self.properties["early_performance"] == 0:  # Poor performance
            self.properties["misconduct_risk"] = 0.75  # High risk
        elif self.properties["early_performance"] == 1:  # Average performance
            self.properties["misconduct_risk"] = 0.25  # Moderate risk
        else:  # Good performance
            self.properties["misconduct_risk"] = 0.05  # Low risk

    def makeDescriptionStr(self):
        return f"{self.name} has early performance level {self.properties['early_performance']} and a misconduct risk of {self.properties['misconduct_risk']}."

class MedicalSchool(Container):
    def __init__(self):
        super().__init__("Medical School")

    def assess_students(self):
        for student in self.contains:
            student.assess_misconduct_risk()

    def makeDescriptionStr(self):
        outStr = f"In the {self.name}, you see: \n"
        for student in self.contains:
            outStr += "\t" + student.makeDescriptionStr() + "\n"
        return outStr

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.rootObject.assess_students()  # Assess misconduct risk based on early performance
        self.observationStr = self.rootObject.makeDescriptionStr()

    def _initialize_simulation(self):
        school = MedicalSchool()
        # Creating students with different early performance levels
        student1 = Student("Student A", early_performance=0, misconduct_risk=0)  # Poor performance
        student2 = Student("Student B", early_performance=1, misconduct_risk=0)  # Average performance
        student3 = Student("Student C", early_performance=2, misconduct_risk=0)  # Good performance
        school.addObject(student1)
        school.addObject(student2)
        school.addObject(student3)
        return school

def main():
    simulation = Simulation()
    print(simulation.observationStr)

if __name__ == "__main__":
    main()
