import pandas as pd
import json


def main():
    corpus = pd.read_json('corpus.jsonl', lines=True)
    train_df = pd.read_json('claims_train.jsonl', lines=True)

    train_df = train_df[train_df['evidence'] != {}].reset_index(drop=True)

    # iter through train_df and get the abstract and title from the cited_doc_ids by mapping them to corpus
    # then making new columns in train_df containing the abstract, title, gold_evidence sentences, label 

    extended_train_df = pd.DataFrame(columns=['id', 'claim', 'abstract', 'title', 'gold_evidence', 'label', 'cited_doc_ids', 'evidence'])

    for i, row in train_df.iterrows():
        id = row['id']
        claim = row['claim']
        evidence = row['evidence']
        cited_doc_ids = row['cited_doc_ids']
        cited_doc_ids = [int(x) for x in cited_doc_ids]

        for doc_id in cited_doc_ids:
            if str(doc_id) not in evidence:
                continue
            document = corpus[corpus['doc_id'] == doc_id].iloc[0]
            abstract = document['abstract']
            title = document['title']
            gold_evidence = []
            label = []
            for evidence_dict in evidence[str(doc_id)]:         
                gold_evidence.extend([sentence for i,sentence in enumerate(abstract) if i in evidence_dict['sentences']])
                label.append(evidence_dict['label'])
            label = list(set(label))[0]

            extended_train_item = {
                'id': id,
                'claim': claim,
                'abstract': " ".join(abstract),
                'title': title,
                'gold_evidence': gold_evidence,
                'label': label,
                'cited_doc_ids': cited_doc_ids,
                'evidence': evidence
            }

            with open('./data/data/processed_data/extended_train.jsonl', 'a+') as f:
                f.write(json.dumps(extended_train_item) + '\n')
            
            extended_train_df.loc[len(extended_train_df)] = [id, claim, " ".join(abstract), title, gold_evidence, label, cited_doc_ids, evidence]

    extended_train_df.to_csv('./data/data/processed_data/extended_claims_train.csv', index=False)

if __name__ == '__main__':
    main()