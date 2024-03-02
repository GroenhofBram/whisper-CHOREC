import json
import pandas as pd
from pathlib import Path


def main():
    json_data = read_json()
    print(json_data)
    
    
    json_data_words = extract_json(json_data)    
    print(json_data_words)


    df_data_words = json_to_df(json_data_words)

def read_json():
    # file_path = Path("D:\\repos\\wav2vec-CHOREC\\report\\hyp1.trn.pra.json")
    
    with open('D:\\repos\\wav2vec-CHOREC\\report\\hyp1.trn.pra.json', "r") as fp:
        # file_data = file.readlines()
        return json.load(fp)
    
def extract_json(json_data) -> dict: # Type hinting
    json_data_words = json_data["speakers"]['S01C002V1_2LG']['(S01C002V1_2LG-words)']["words"]

    return json_data_words

def json_to_df(json_data_words):
    speaker_list = []
    sentence_id_list = []
    word_count_list = []
    reference_list = []
    reference_text_list = []
    hypothesis_list = []
    hypothesis_text_list = []
    evaluation_label_list = []

    for speaker, data_dict in json_data_words['speakers'].items():
        for sentence_id, sentence_data in data_dict.items():
            for word_info in sentence_data['words']:
                speaker_list.append(speaker)
                sentence_id_list.append(sentence_id)
                word_count_list.append(sentence_data['word_count'])
                reference_list.append(word_info['ref'])
                reference_text_list.append(word_info['ref'])
                hypothesis_list.append(word_info['hyp'])
                hypothesis_text_list.append(word_info['hyp'])
                evaluation_label_list.append(word_info['eval_label'])

    # Create DataFrame
    df = pd.DataFrame({
        'speaker': speaker_list,
        'sentence_id': sentence_id_list,
        'word_count': word_count_list,
        'reference': reference_list,
        'reference_text': reference_text_list,
        'hypothesis': hypothesis_list,
        'hypothesis_text': hypothesis_text_list,
        'evaluation_label': evaluation_label_list
})
    
    print(df)

    return df

