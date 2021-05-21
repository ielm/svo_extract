import os

import pandas as pd

from collections import OrderedDict


def get_all_data_files(base_dir='data'):
    data_files = []
    for root, _, files in os.walk(base_dir):
        for file in files:
            filename = [root, file]
            data_files.append(filename)
    return data_files


def process_persuasion_data(data_file: str):
    dialogs = OrderedDict()
    dialog_ids = []

    header = ["index", "text", "turn", "speaker", "dialog_id"]

    # with open(data_file, 'r') as input_file:
    data = pd.read_csv(data_file)

    # for line in data:
        # print(line)

    for _, row in data.iterrows():
        # print(row)÷
        # print(type(row))
        # print(row["DialogID"])
        # if dialog id has been seen, 
        #   append turn to dialog id, 
        # else create new dialog dict

        if row["dialog_id"] in dialog_ids:
            turn = {
                "speaker": row["role"],
                "turn": row["turn"], 
                "utterance": row["text"], 
                "esvo": get_esvos(row["text"]),
                "nsvo": get_nsvos(row["text"])
            }
            dialogs[row["dialog_id"]]["turns"].append()
            


    # print(dialogs.head())



if __name__ == '__main__':
    process_persuasion_data('data/Persuasion/full_dialog.csv')