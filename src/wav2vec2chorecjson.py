import json
import os
import re
import pandas as pd

from json_load_file import extract_words_from_json, load_json_file
from src.extract_text import extract_text
from src.islinux import is_linux


def main():
    json_data = read_json()
    
    json_data_words = extract_words_from_json(json_data)

    df_data_words = json_to_df(json_data)


def get_file_path():
    if is_linux():
        pth = os.path.abspath(os.path.join(__file__, "../../report/hyp1.trn.pra.json"))
        print(pth)
        return pth
    return "D:\\repos\\wav2vec-CHOREC\\report\\hyp1.trn.pra.json"


def read_json():
    # file_path = Path("D:\\repos\\wav2vec-CHOREC\\report\\hyp1.trn.pra.json")

    file_path = get_file_path()
    
    return load_json_file(file_path)
    

def json_to_df(json_data_words):
    speaker_list = []
    sentence_id_list = []
    word_count_list = []
    reference_list = []
    hypothesis_list = []
    evaluation_label_list = []

    for speaker, data_dict in json_data_words['speakers'].items():
        for sentence_id, sentence_data in data_dict.items():
            for word_info in sentence_data['words']:
                speaker_list.append(speaker)
                sentence_id_list.append(sentence_id)
                word_count_list.append(sentence_data['word_count'])
                reference_list.append(word_info['ref'])
                hypothesis_list.append(word_info['hyp'])
                evaluation_label_list.append(word_info['eval_label'])

    df = pd.DataFrame({
        'speaker': speaker_list,
        'sentence_id': sentence_id_list,
        'word_count': word_count_list,
        'reference': reference_list,
        'hypothesis': hypothesis_list,
        'evaluation_label': evaluation_label_list
    })

    speaker_id = df['speaker'].iloc[0].split('_')[0]
    file_name = f'output/{speaker_id}-dataframe.csv'
    df.to_csv(file_name, index=False)


    filtered_file_name = f'output/{speaker_id}-filtered-dataframe.csv'
    df_filtered = df[df["reference"] != "*"]
    df_filtered = df_filtered[df_filtered["reference"] != "*s"]

    df_filtered['reference'] = df_filtered['reference'].apply(lambda x: extract_text(x))
    df_filtered = df_filtered[df_filtered['reference'] != ""]
    df_filtered = df_filtered.drop_duplicates(subset='reference', keep='last')
    df_filtered['hypothesis'] = df_filtered['hypothesis'].apply(lambda x: x if x.strip() != '' else '[SKIPPED]')

    df_filtered.to_csv(filtered_file_name, index=False)
    print(df_filtered)
    return df





