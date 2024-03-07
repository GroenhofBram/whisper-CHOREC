### NaN in dataframe[Reference] needs to be filtered out.
### Doubles in dataframe? only keep the last one of the two (reference).

import os
# from sklearn.metrics import confusion_matrix
import numpy as np
import pandas as pd

# If it finds nan replace with " "
def main():
    al_df = read_aligned_file_as_df("S01C002V1-filtered-dataframe.csv")
    print(al_df)

    base_df = pd.DataFrame.from_dict({
        'prompt': read_prompt_file("2LG_words.txt")
    })

    print(base_df)

    # prompts  orths   asr
    # 
    
    base_df['prompts_plus_orth']
    # do what you need to with sizes

    # ref_list = al_df["reference"]
    # hyp_list = al_df["hypothesis"]
    

def calc_prompt_plus_orth(actual_word: str, input_word: str):
    return 1
    # confusion_matrix = create_confusion_matrix(df_all_words)

def get_abs_path(base_path: str, file_name: str):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", base_path, file_name)) 

def read_aligned_file_as_df(file_name):
    file_path = get_abs_path("output", file_name)
    return pd.read_csv(filepath_or_buffer=file_path)


def read_prompt_file(file_name):
    file_path = get_abs_path("files_static", file_name)
    with open(file_path, "r") as fp:
            return [str(line.strip()) for line in fp.readlines()]

  


def create_confusion_matrix(df_all_words):
    # Example true labels and predicted labels
    prompt_orth_list = np.array([0, 1, 0, 1, 1, 0, 0])
    prompt_hypo_list = np.array([0, 1, 0, 1, 0, 1, 0])

    # Compute confusion matrix
    cm = confusion_matrix(prompt_orth_list,
                          prompt_hypo_list)
    
    # cm[0, 0] = TN
    # cm[0, 1] = FP
    # cm[1, 0] = FN
    # cm[1, 1] = TP
    print("Confusion Matrix:")
    print(cm)
