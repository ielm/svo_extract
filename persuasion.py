from enhanced_subject_verb_object_extract import findSVOs, nlp
from nltk_subject_verb_object_extraction import SVO
from collections import OrderedDict

import pandas as pd

from pprint import pprint


def get_nsvos(extractor: SVO, text: str):
    ntokens = extractor.sentence_split(text)
    nsvo_extraction = []
    for s in ntokens:
        root_tree = extractor.get_parse_tree(s)
        nsvo_extraction.append(extractor.process_parse_tree(next(root_tree)))
    return nsvo_extraction


def process_persuasion_data(data_file: str):
    dialogs = OrderedDict()
    dialog_ids = []

    header = ["index", "text", "turn", "speaker", "dialog_id"]

    data = pd.read_csv(data_file)

    nltksvo = SVO()

    for _, row in data.iterrows():

        if row["dialog_id"] in dialog_ids:
            turn = {
                "speaker": row["role"],
                "turn": row["turn"], 
                "utterance": row["unit"], 
                "esvo": findSVOs(nlp(row["unit"])),
                "nsvo": get_nsvos(nltksvo, row["unit"])
            }
            dialogs[row["dialog_id"]]["turns"].append(turn)
        else:
            dialog_ids.append(row["dialog_id"])
            dialogs[row["dialog_id"]] = {
                "dialog_id": row["dialog_id"], 
                "turns": [
                    {
                        "speaker": row["role"],
                        "turn": row["turn"], 
                        "utterance": row["unit"], 
                        "esvo": findSVOs(nlp(row["unit"])),
                        "nsvo": get_nsvos(nltksvo, row["unit"])
                    }
                ]
            }

    return [d for _, d in dialogs.items()]

if __name__ == '__main__':
    dialogs = process_persuasion_data('data/Persuasion/full_dialog.csv')

    svo_datafile = open(f"data/Persuasion/svo_dialogs.json", encoding="utf8", mode='w')
    svo_datafile.write(json.dumps(dialogs))
    svo_datafile.close()
