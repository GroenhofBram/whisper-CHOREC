import json
from pathlib import Path

def main():
    json_data = read_json()
    print(json_data)
    json_data_words = extract_json(json_data)    
    print(json_data_words)

def read_json():
    # file_path = Path("D:\\repos\\wav2vec-CHOREC\\report\\hyp1.trn.pra.json")
    
    with open('D:\\repos\\wav2vec-CHOREC\\report\\hyp1.trn.pra.json', "r") as fp:
        # file_data = file.readlines()
        return json.load(fp)
    
def extract_json(json_data) -> dict: # Type hinting
    json_data_words = json_data["speakers"]['S01C002V1_2LG']['(S01C002V1_2LG-words)']["words"]

    return json_data_words

