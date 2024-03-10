import pandas as pd
from src.csvtodataframe import csv_to_df
from src.islinux import is_linux

def main():
    csv_filename = get_csv_filename()
    unaligned_df = csv_to_df(csv_filename)
    reference_list = get_column_as_list(unaligned_df, "reference")
    hypothesis_list = get_column_as_list(unaligned_df, "hypothesis")
    generate_csv_for_sctk_align(reference_list, hypothesis_list)

def get_csv_filename():
    csv_filename = "S01C002V1-filtered-dataframe.csv"
    
    linux_file_path_base = f"/vol/tensusers5/bgroenhof/wav2vec2_chorec_run/wav2vec2build/output/{csv_filename}"
    windows_local_file_path = f"D:\\repos\\wav2vec-CHOREC\\output\\{csv_filename}"

    if is_linux():
        return f"{linux_file_path_base}"
    return f"{windows_local_file_path}"


def get_column_as_list(df, col_name):
    return df[col_name].tolist()

def generate_csv_for_sctk_align(reference_list, hypothesis_list):
    hypothesis_list = [str(item) for item in hypothesis_list]
    reference_list = [str(item) for item in reference_list]

    # # # # HYPOTHESIS
    d = {'utterance_id': ["S01C002V1_2LG-words"] ,
        'transcript': [" ".join(hypothesis_list)]}
    df = pd.DataFrame(data=d)
    df.to_csv('output/hyp_filtered.csv', index=False)


    # # # # REFERENCE
    d = {'utterance_id': ["S01C002V1_2LG-words"],
        'transcript': [" ".join(reference_list)]}
    df = pd.DataFrame(data=d)
    df.to_csv('output/ref_filtered.csv', index=False)

