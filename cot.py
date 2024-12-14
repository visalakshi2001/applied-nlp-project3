import os
import openai
import pandas as pd
import re
from ast import literal_eval
from tqdm import tqdm

client = openai.OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
print("openai authenticated")

with open('simulation_utils.py', 'r') as f:
    simulation_template = f.read()

with open('bacteria.py', 'r') as f:
    example_bacteria = f.read()


def get_gpt_response(id, claim, reference_text, gold_evidence, model="gpt-4o-mini", **kwargs):

    if not os.path.exists('gpt_results/'):
        os.makedirs('gpt_results/')

    system_prompt = """
        You are a scientific claim inspector, who can catch fake claims accurately and verify correct claims efficiently.
        Your main process is building simulation for building environment for testing out claims. You compare the results
        of a simulation with a given claim and provide verification results as Supported (for True claims) and Refuted (for False claims).

        You will be given the following information below:
        1. A Claim
        2. A passage of supporting text from a scientific article that can be used to help verify the claim.
           Sometimes you will be provided with specific gold_sentences where the evidence of claim's veracity can be found.
        3. An example simulation that can be used as a template to help guide your construction of a simulation

        Your output will be a Python simulation whose output will clearly determine whether the claim is likely supported or refuted.
       
        Also, You must output the simulation between clodeblocks (```), or the simulation will not be correctly parsed.
        
        For example:
        ```
        # python comment stating the input claim
        # code fo the simulation
        # print the output of the simulation
        print(result)
        ```
    """

    user_prompt = f"""
        Claim: {claim}
        Reference Text: {reference_text}

        Gold Sentence that can provide the evidence of claim verification: {''.join(gold_evidence)}
        
        ```
        # simulation_utils.py
        {simulation_template}

        # bacteria simulation example
        {example_bacteria}
        ```

        Rules for the output:
        1. Generate simulation according to the given Claim, take Reference Text to figure out the objects of the simulation and their properties.
        2. The generated code should not generate any errors
        3. If you are extending upon the given base template, or using code from the base template, include it in your code by using either of the two ways mentioned below:
            a. import statements (importing the classes from base template simulation_utils.py)
            OR
            b. writing the whole base template code before your simulation code

        4. Make sure the output of the simulation is appropriate to the given instructions. 
        5. It clearly determines/shows if the  claim is supported or refuted.

        Please generate your simulation now
    """

    messages=[{"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}]

    kwargs["temperature"] = 0.0
    kwargs["top_p"] = 1
    kwargs["frequency_penalty"] = 0.0
    kwargs["presence_penalty"] = 0.0
    kwargs["timeout"] = 4*10*60  # 40 minutes
    kwargs["model"] = model
    kwargs["messages"] = messages
    

    response = client.chat.completions.create(**kwargs)

    with open(f'gpt_results/prompt_{id}.txt', 'w', encoding='utf-8') as f:
        f.write(user_prompt)

    with open(f'gpt_results/response_{id}.txt', 'w', encoding='utf-8') as f:
        f.write(response.choices[0].message.content.strip())
    
    print(f"Responses saved to gpt_results/response_{id}")

    return response.choices[0].message.content.strip()


def parse_gpt_response(id, response):
    if not os.path.exists('simscripts/'):
        os.makedirs('simscripts/')

    code_block_pattern = r'```(.*?)```'
    code_blocks = re.findall(code_block_pattern, response, re.DOTALL)
    code_block = ''.join(code_blocks)

    code_filepath = f'simscripts/simulation_{id}.py'
    with open(code_filepath, 'w', encoding='utf-8') as f:
        f.write(code_block)
    
    print(f"simscripts/simulation_{id}.py")

    return code_block, code_filepath

def run_generated_simulation(id, code_filepath):

    std_out = ""
    std_err = ""

    stdoutfile = 'simscripts/' + f"std_out_{id}.txt"
    stderrfile = 'simscripts/' + f"std_err_{id}.txt"
    command = "python " + code_filepath + " > " + stdoutfile + " 2> " + stderrfile

    print("Running command: " + command)
    os.system(command)

    with open(stdoutfile, "r") as f:
        std_out = f.read()
    with open(stderrfile, "r") as f:
        std_err = f.read()

        
    return std_out, std_err


def get_gpt_verification(id, sim_output, claim, model="gpt-4o-mini", **kwargs):

    if not os.path.exists('gpt_ver_results/'):
        os.makedirs('gpt_ver_results/')

    system_prompt = """
        You are a scientific claim inspector, who can catch fake claims accurately and verify correct claims efficiently.
        Your main responsibility is to look at the output of a simulation. 
        The simulation was run with the elements relevant to the given claim, and it displays a output that can give you details of the veraicity of the claim.
        
        Inspect the output and understand the claim, to verify if the claim is supported or refuted.

        You will be given the following information below:
        1. A Claim
        2. The output of a Simulation that can be used to help verify the claim.
        
        Your output will be a python dictionary containing the following information:
        {
            "claim": the given claim as it is,
            "verification_result": "Supported" or "Refuted" or None if you are unable to verify the claim,
            "reason": reason of the verification result, or reason of the None output
        }
        
    """

    user_prompt = f"""
        Claim: {claim}
        Simulation Output: {sim_output}


        Rules for the output:
        1. Make sure the output of the simulation is appropriate to the given instructions.
        2. If your verification_result is None, make sure to include the reason as to why you were note able to determine the result
        3. Your verification result should only include None if the simulation output is an execution error, otherwise you should provide a definite result and a definite reason.

        Please generate your verification result now
    """

    messages=[{"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}]

    kwargs["temperature"] = 0.0
    kwargs["top_p"] = 1
    kwargs["frequency_penalty"] = 0.0
    kwargs["presence_penalty"] = 0.0
    kwargs["timeout"] = 4*10*60  # 40 minutes
    kwargs["model"] = model
    kwargs["messages"] = messages
    

    response = client.chat.completions.create(**kwargs)

    with open(f'gpt_ver_results/prompt_{id}.txt', 'w', encoding='utf-8') as f:
        f.write(user_prompt)

    with open(f'gpt_ver_results/response_{id}.txt', 'w', encoding='utf-8') as f:
        f.write(response.choices[0].message.content.strip())

    
    print(f"gpt_ver_results/response_{id}.txt")

    return response.choices[0].message.content.strip()


train_annotated = pd.read_json('data/data/processed_data/extended_train_annotated.jsonl', lines=True)

def gen_and_run_sims():
    for i, row in tqdm(train_annotated[train_annotated['category'].isin(['directional'])].iterrows()):
        id = row['id']
        claim = row['claim']
        abstract = row['abstract']
        gold_evidence = row['gold_evidence']

        response = get_gpt_response(id, claim, abstract, gold_evidence)
        code_block, code_filepath = parse_gpt_response(id, response)

        std_out, std_err = run_generated_simulation(id, code_filepath)

        sim_output = f"""
                Simulation Output:
                {std_out}

                Simulation Error:
                {std_err}
            """

        response = get_gpt_verification(id, sim_output, claim)


if __name__ == '__main__':
    gen_and_run_sims()
