import os
from sklearn.metrics import confusion_matrix
import numpy as np
import pandas as pd

def main():
    base_df = create_base_df()
    base_df_binaries = add_binaries(base_df)
    export_df_data_csv(base_df_binaries)
    export_df_data_json(base_df_binaries)
    ref_list_binary, hyp_list_binary = get_binary_lists(base_df_binaries)
    conf_matrix = create_confusion_matrix(ref_list_binary, hyp_list_binary)
    export_conf_matrix(conf_matrix)

    

def get_abs_path(base_path: str, file_name: str):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", base_path, file_name)) 

def read_aligned_file_as_df(file_name):
    file_path = get_abs_path("output", file_name)
    return pd.read_csv(filepath_or_buffer=file_path)

def read_prompt_file(file_name):
    file_path = get_abs_path("files_static", file_name)
    with open(file_path, "r") as fp:
            return [str(line.strip()) for line in fp.readlines()]

def add_binaries(base_df):
     base_df_empty_binaries = add_binary_cols(base_df)
     # print(base_df_empty_binaries)
     base_df_binaries = fill_binary_cols(base_df_empty_binaries)
     return base_df_binaries

def fill_binary_cols(base_df_empty_binaries):
     base_df_binaries = fill_binary_values(base_df_empty_binaries)
     return base_df_binaries
     # print(base_df_binaries)

def fill_binary_values(base_df_empty_binaries):
     base_df_empty_binaries.loc[base_df_empty_binaries['prompt'] != base_df_empty_binaries['reference'], 'prompts_plus_orth'] = 1
     base_df_empty_binaries.loc[base_df_empty_binaries['prompt'] != base_df_empty_binaries['hypothesis'], 'prompts_plus_hypo'] = 1
     return base_df_empty_binaries

def add_binary_cols(base_df):
     base_df.insert(len(base_df.columns), "prompts_plus_orth", 0)
     base_df.insert(len(base_df.columns), "prompts_plus_hypo", 0)
     return base_df


# This is hard-coded
def create_base_df():
    al_df = read_aligned_file_as_df("S01C002V1-filtered-dataframe.csv")
    base_df = pd.DataFrame.from_dict({
        'prompt': read_prompt_file("2LG_words.txt")
    })
    base_df.insert(0, 'id', 'S01C002V12LG')
    base_df = pd.merge(base_df, al_df[['reference', "hypothesis"]], left_index=True, right_index=True)
    return base_df

def export_df_data_csv(base_df_binaries):
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'all_data_output'))
    os.makedirs(output_dir, exist_ok=True) 
    file_name = "All_data.csv"
    file_path = os.path.join(output_dir, file_name)
    base_df_binaries.to_csv(file_path, index=False)

def export_df_data_json(base_df_binaries):
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'all_data_output'))
    os.makedirs(output_dir, exist_ok=True) 
    file_name = "All_data.json"
    file_path = os.path.join(output_dir, file_name)
    base_df_binaries.to_json(file_path, index=False)     

def get_binary_lists(base_df_binaries):
     ref_list_binary = base_df_binaries["prompts_plus_orth"].tolist()
     hyp_list_binary = base_df_binaries["prompts_plus_hypo"].tolist()
     return ref_list_binary, hyp_list_binary

def create_confusion_matrix(ref_list_binary, hyp_list_binary):
    conf_matrix = confusion_matrix(ref_list_binary,
                          hyp_list_binary)
       
    # cm[0, 0] = TN
    # cm[0, 1] = FP
    # cm[1, 0] = FN
    # cm[1, 1] = TP
    return conf_matrix

def export_conf_matrix(conf_matrix):
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'all_data_output'))
    file_name = 'Conf_matrix.csv'
    file_path = os.path.join(output_dir, file_name)
    
    # Are these useful?
    descriptions = np.array([['TN', 'FP'],
                             ['FN', 'TP']])
    conf_matrix_with_desc = np.hstack((descriptions, conf_matrix))
    
    np.savetxt(file_path, conf_matrix_with_desc, delimiter=',', fmt='%s')