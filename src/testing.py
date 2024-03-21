import json
import os
import platform
import re
import pandas as pd
from pathlib import Path


def main():
    json_data = read_json()
    
    json_data_words = extract_json(json_data)

    print("\nParsing json")
    df_data_words = json_to_df(json_data)


def get_file_path():
    if platform.system().lower() == "linux":
        pth = os.path.abspath(os.path.join(__file__, "../../report/unaligned/hyp1.trn.pra.json"))
        print(pth)
        return pth
    return "D:\\repos\\wav2vec-CHOREC\\output_single\\report\\unaligned\\hyp1.trn.pra.json"

def read_json():
    # file_path = Path("D:\\repos\\wav2vec-CHOREC\\report\\hyp1.trn.pra.json")

    file_path = get_file_path()
    
    with open(file_path, "r") as fp:
        # file_data = file.readlines()
        return json.load(fp)
    
def extract_json(json_data) -> dict: # Type hinting
    json_data_words = json_data["speakers"]['S01C002V1_2LG']['(S01C002V1_2LG-words)']["words"]

    return json_data_words


# def to_df(input_words):


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
    
    df.to_csv("000000UNFILTEREDTEST", index=False)


    filtered_file_name = f'output/{speaker_id}-filtered-dataframe.csv'

    
    df_filtered = df[df["reference"] != "*"]
    df_filtered = df_filtered[df_filtered["reference"] != "*s"]


    # pattern = r'\((.*?)\)' # Find anything between parentheses.

    df_filtered = df[df["reference"] != "*"]
    df_filtered = df_filtered[df_filtered["reference"] != "*s"]
    df_filtered['reference'] = df_filtered['reference'].apply(lambda x: extract_text(x))
    df_filtered = df_filtered[df_filtered['reference'] != ""]
    df_filtered = df_filtered.drop_duplicates(subset='reference', keep='last')
    df_filtered['hypothesis'] = df_filtered['hypothesis'].apply(lambda x: x if x.strip() != '' else 'SKIPPED')

        # for index, row in df.iterrows():
    #     reference = row['reference']
    #     hypothesis = row['hypothesis']
    #     if reference in hypothesis:
    #         df_filtered.at[index, 'hypothesis'] = reference
    #         df_filtered.at[index, 'evaluation_label'] = 'C'

    hypothesis_values = df['hypothesis'].unique()
    print(hypothesis_values)
    if "hoofdijn" in hypothesis_values:
        print("GEVONDEN")
    else:
        print("NIET GEVONDEN")

    for index, row in df_filtered.iterrows():
        reference = row['reference']
        print(f"\tREF: {reference}") 
        # Check if the reference value exactly matches any value in the hypothesis list
        if reference in hypothesis_values:
            print(f"\tMATCHEDREF: {reference}") 
            # Update the "hypothesis" value to the reference value
            df_filtered.at[index, 'hypothesis'] = reference
            # Update the "evaluation_label" to 'C'
            df_filtered.at[index, 'evaluation_label'] = 'C'
    
    df_filtered.to_csv("000000FILTEREDTEST", index=False)
            
    # print("\n UNFILTERED DF")
    # print(df)
    print("\n FILTERED DF")
    print(df_filtered)
    return df

pattern = r'\((.*?)\)'

def extract_text(text):
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    else:
        return text