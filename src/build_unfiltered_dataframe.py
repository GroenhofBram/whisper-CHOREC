import os
from pandas import DataFrame

from extract_text import extract_text
from models.participant_session import FilteredDataframeSession

def build_unfiltered_and_filtered_dataframes(json_data: dict, base_dir: str) -> FilteredDataframeSession:
    speaker_list = []
    sentence_id_list = []
    word_count_list = []
    reference_list = []
    hypothesis_list = []
    evaluation_label_list = []

    for speaker, data_dict in json_data['speakers'].items():
        for sentence_id, sentence_data in data_dict.items():
            for word_info in sentence_data['words']:
                speaker_list.append(speaker)
                sentence_id_list.append(sentence_id)
                word_count_list.append(sentence_data['word_count'])
                reference_list.append(word_info['ref'])
                hypothesis_list.append(word_info['hyp'])
                evaluation_label_list.append(word_info['eval_label'])

    df = DataFrame({
        'speaker': speaker_list,
        'sentence_id': sentence_id_list,
        'word_count': word_count_list,
        'reference': reference_list,
        'hypothesis': hypothesis_list,
        'evaluation_label': evaluation_label_list
    })
    df.to_csv(f'session_df_unfiltered.csv', index=False)

    df_filtered = df[df["reference"] != "*"]
    df_filtered = df_filtered[df_filtered["reference"] != "*s"]

    df_filtered['reference'] = df_filtered['reference'].apply(lambda x: extract_text(x))
    df_filtered = df_filtered[df_filtered['reference'] != ""]
    df_filtered = df_filtered.drop_duplicates(subset='reference', keep='last')
    df_filtered['hypothesis'] = df_filtered['hypothesis'].apply(lambda x: x if x.strip() != '' else 'o')
    filtered_df_file_name = 'session_df_filtered.csv'
    df_filtered.to_csv(filtered_df_file_name, index=False)

    return FilteredDataframeSession(
        filtered_df=df_filtered,
        filtered_df_file_path=os.path.join(base_dir, filtered_df_file_name)
    )
