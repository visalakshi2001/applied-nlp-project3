
# Claim: Systemic lupus erythematosus is a risk factor for cardiovascular disease.
# The simulation will check if systemic lupus erythematosus (SLE) is included as a risk factor for cardiovascular disease.

from simulation_utils import GameObject, Container

class RiskFactor(GameObject):
    def __init__(self, name, isRiskFactor):
        super().__init__(name)
        self.isRiskFactor = isRiskFactor

class CardiovascularDiseaseRiskAssessment(Container):
    def __init__(self):
        super().__init__("Cardiovascular Disease Risk Assessment")
        self.riskFactors = []

    def addRiskFactor(self, riskFactor):
        self.riskFactors.append(riskFactor)

    def checkRiskFactor(self, riskFactorName):
        for riskFactor in self.riskFactors:
            if riskFactor.name == riskFactorName:
                return riskFactor.isRiskFactor
        return False

    def makeDescriptionStr(self):
        description = f"In the {self.name}, the following risk factors are considered:\n"
        for riskFactor in self.riskFactors:
            description += f"- {riskFactor.name} (Risk Factor: {riskFactor.isRiskFactor})\n"
        return description

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.result = self.checkClaim()

    def _initialize_simulation(self):
        assessment = CardiovascularDiseaseRiskAssessment()
        # Adding risk factors
        assessment.addRiskFactor(RiskFactor("Age", True))
        assessment.addRiskFactor(RiskFactor("Ethnicity", True))
        assessment.addRiskFactor(RiskFactor("Systolic Blood Pressure", True))
        assessment.addRiskFactor(RiskFactor("Body Mass Index", True))
        assessment.addRiskFactor(RiskFactor("Total Cholesterol: HDL Ratio", True))
        assessment.addRiskFactor(RiskFactor("Smoking", True))
        assessment.addRiskFactor(RiskFactor("Family History of Coronary Heart Disease", True))
        assessment.addRiskFactor(RiskFactor("Type 1 Diabetes", True))
        assessment.addRiskFactor(RiskFactor("Type 2 Diabetes", True))
        assessment.addRiskFactor(RiskFactor("Treated Hypertension", True))
        assessment.addRiskFactor(RiskFactor("Rheumatoid Arthritis", True))
        assessment.addRiskFactor(RiskFactor("Atrial Fibrillation", True))
        assessment.addRiskFactor(RiskFactor("Chronic Kidney Disease (Stage 4 or 5)", True))
        assessment.addRiskFactor(RiskFactor("Chronic Kidney Disease (Stage 3, 4, or 5)", True))
        assessment.addRiskFactor(RiskFactor("Migraine", True))
        assessment.addRiskFactor(RiskFactor("Corticosteroids", True))
        assessment.addRiskFactor(RiskFactor("Systemic Lupus Erythematosus (SLE)", True))  # Key risk factor
        assessment.addRiskFactor(RiskFactor("Atypical Antipsychotics", True))
        assessment.addRiskFactor(RiskFactor("Severe Mental Illness", True))
        assessment.addRiskFactor(RiskFactor("HIV/AIDS", False))  # Not statistically significant
        return assessment

    def checkClaim(self):
        # Check if SLE is a risk factor
        if self.rootObject.checkRiskFactor("Systemic Lupus Erythematosus (SLE)"):
            return "Supported"
        else:
            return "Refuted"

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    print(f"Claim Verification Result: {simulation.result}")

if __name__ == "__main__":
    main()
