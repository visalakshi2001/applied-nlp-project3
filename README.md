# Scientific Discovery

## Write-up

See PDF file: [`Project3_ScientificReasoning.pdf`](https://github.com/visalakshi2001/applied-nlp-project3/blob/main/Project3_ScientificReasoning.pdf) for write-up 

## Description
This project implements a novel approach to verifying scientific claims by generating and running Python simulations. The approach is applied to the SciFact dataset, with a focus on claims from the train subset and further filtered for those with cited evidence. The system uses GPT-based models to generate simulations based on claims and supporting evidence and subsequently analyzes the simulation results to classify the claims as Supported, Refuted, or Unverifiable.

## Features
1. Claim-Specific Simulations:
The GPT model generates custom Python simulation scripts based on the given claim, reference text, and evidence sentences. These scripts are designed to model the claim’s underlying scientific phenomena.

2. Execution and Output Analysis:
The generated simulations are executed, and their outputs are passed back to the GPT model for analysis. This ensures the claim is verified using simulation results rather than raw text-based reasoning.

3. Category-Based Processing:
Claims are categorized (e.g., medicine, cellular, directional, etc.) and processed sequentially, allowing domain-specific evaluation and analysis.

4. Error Logging and Debugging:
Detailed logs of simulation generation, execution, and verification results are maintained, aiding in the identification and resolution of errors in the pipeline.

### Prerequisites
- Python 3.11.7
- pip 23.2.1
- virtualenv (highly recommended)
- packages listed in the `requirements.txt` file

### Setup and Run
After cloning the repository into an environment, install the required packages using the following command on your terminal in the directory of the project:
```
pip install -r requirements.txt
```

### File and Folder Contents

```graphql
├── data/
│   ├── *.jsonl          # Actual Dataset from SciFact Dataset
│   ├── processed_data/  # Annotated SciFact train subset with additional labels
├── gpt_results/         # Logs of GPT prompts and responses
├── gpt_ver_results/     # Logs of GPT verification outputs
├── simscripts/          # Generated simulation scripts and execution logs
├── src/
├── cot.py               # Main script for claim verification
├── data_filter.py       # Script for filtering and preprocessing dataset
├── evaluation.py        # Script for evaluating simulation results
├── simulation_utils.py  # Base simulation utilities
├── bacteria.py          # Example simulation script for bacterial growth
├── example_bacteria.py  # Example simulation script for bacteria
├── link.txt                    # Reference links and resources for the project
├── Project3_ScientificReasoning.pdf  # Project report on scientific reasoning using simulations
└── README.md            # Project documentation
```

