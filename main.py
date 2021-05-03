from enhanced_subject_verb_object_extract import findSVOs, nlp
from nltk_subject_verb_object_extraction import SVO

import os
import json

def get_all_data_files(base_dir='data'):
    data_files = []
    for root, _, files in os.walk(base_dir):
        for file in files:
            filename = [root, file]
            data_files.append(filename)
    return data_files

def extract_svos(data):
    svos = {}

    nltksvo = SVO()

    for dialog in data:
        svo = {
            "dialogue_id": dialog["dialogue_id"],
            "turns": []
        }
        print(dialog["dialogue_id"])
        for turn in dialog["turns"]:
            
            # esvo extraction
            etokens = nlp(turn["utterance"])
            esvo_extraction = findSVOs(etokens)

            # nltk svo extraction
            ntokens = nltksvo.sentence_split(turn["utterance"])
            nsvo_extraction = []
            for s in ntokens:
                root_tree = nltksvo.get_parse_tree(s)
                nsvo_extraction.append(nltksvo.process_parse_tree(next(root_tree)))

            turn = {
                "speaker": turn["speaker"],
                "turn_id": turn["turn_id"],
                "utterance": turn["utterance"],
                "esvo": esvo_extraction,
                "nsvo": nsvo_extraction
            }
            svo["turns"].append(turn)
            print(turn)
        svos.append(svo)
    return svos

if __name__ == '__main__':
    files = get_all_data_files()

    for f in files:
        datafile = open(f"{f[0]}/{f[1]}", encoding='utf8', mode='r')
        data = json.loads(datafile.read())
        datafile.close()

        svo_data = extract_svos(data)
        
        svo_datafile = open(f"{f[0]}/svo_{f[1]}", encoding='utf8', mode='w')
        svo_datafile.write(json.dumps(svo_data))
        svo_datafile.close()