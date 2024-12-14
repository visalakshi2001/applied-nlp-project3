from ast import literal_eval
import os
import re

import pandas as pd
import numpy as np


train_annotated = pd.read_json('data/data/processed_data/extended_train_annotated.jsonl', lines=True)
ver_dir = 'gpt_ver_results'
ver_files = [filename for filename in os.listdir(ver_dir) if filename.startswith("response")]

train_results = train_annotated[train_annotated['category'].isin(['medical', 'cellular', 'directional'])].copy()
train_results['label'] = np.where(train_results['label'] == 'CONTRADICT', 'Refuted', 'Supported')

train_results['verification_result'] = None
train_results['reason'] = None


for r in ver_files:
    with open(os.path.join(ver_dir, r), 'r') as f:
        ver_res = f.read()
    
    target_id = int(r.split('_')[-1].split('.')[0])
    from_code = re.findall(r'```python(.*?)```', ver_res, re.DOTALL)

    if from_code:
        ver_res = from_code[0].strip()
    
    ver_res = literal_eval(ver_res)
    
    train_results.loc[train_results['id'] == target_id, 'verification_result'] = ver_res['verification_result']
    train_results.loc[train_results['id'] == target_id, 'reason'] = ver_res['reason']

train_results['matched'] = train_results.apply(lambda x: x['verification_result'] == x['label'], axis=1)
train_results['verification_result'] = train_results['verification_result'].astype(str)

print("Total Claims Verified", len(train_results))

print(train_results[train_results['matched'] == False]['verification_result'].value_counts())

results = {}

groups = train_results.groupby('category')
for category, group in groups:
    # Calculate the sum of True values in 'matched' as correct_match
    correct_match = group['matched'].sum()
    
    # Calculate the sum of False values in 'matched' as incorrect_match (subtracted None results to get actual inaccurate)
    incorrect_match = (~group['matched']).sum() - (group['verification_result']=='None').sum()
    
    # Count the None values in 'verification_result' as errors
    errors = (group['verification_result']=='None').sum()

    total = len(group)
    
    # Store the results in the dictionary
    results[category] = {
        'correct_match': correct_match,
        'incorrect_match': incorrect_match,
        'errors': errors,
        'total': total
    }

print(pd.DataFrame(results).T)
