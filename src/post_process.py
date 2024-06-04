from os import makedirs
import pandas as pd

from constants import WAV2VEC2_MODEL_NAME_FLDR
from os.path import join
from pathing import get_abs_folder_path


def main():
    # This is based on the model defined as a constant.
    # CHANGE ARGUMENT IF YOU WANT TO USE A DIFFERENT FILE AS STARTING POINT
    validation_filepath_input = get_validation_filepath("total_alldata_df.csv", type = "input")
    validation_filepath_output = get_validation_filepath("total_alldata_df_V2.csv", type = "output")
    validaton_filepath_freqdf = get_validation_filepath("total_alldata_df_freq.csv", type = "freq")
    check_filepaths(validation_filepath_input, validation_filepath_output, validaton_filepath_freqdf)

    validation_df = read_validation_file(validation_filepath_input)
    validation_df_FP_only = filter_FPs(validation_df)
    print(f"Number of false positives at at start\t: {len(validation_df_FP_only)}")
    validation_df_FP_freq = get_freq_FP_prompts(validation_df_FP_only)
    export_validation_df_FP_freq(validaton_filepath_freqdf, validation_df_FP_freq)


def export_validation_df_FP_freq(filepath: str, freq_df):
    freq_df.to_csv(filepath, index=False)



def get_validation_filepath(file_name: str, type: str):
    base_output_dir_in_repo = get_abs_folder_path("output")
    csv_dir = join(base_output_dir_in_repo, WAV2VEC2_MODEL_NAME_FLDR)
    csv_dir_input = join(csv_dir, "all_data_output")
    csv_dir = join(csv_dir_input, "post_processing")
    makedirs(csv_dir, exist_ok=True) 

    if type == "input":
        csv_input_filepath = join(csv_dir_input, file_name)
        return csv_input_filepath
    
    elif type == "output":
        csv_output_filepath = join(csv_dir, file_name)
        return csv_output_filepath
    
    elif type == "freq":
        csv_freq_output_filepath = join(csv_dir, file_name)
        return csv_freq_output_filepath

def check_filepaths(s1: str, s2: str, s3: str):
    print(f"\n+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ \nPlease check the filepaths:\nInput\t:{s1}\nOutput\t:{s2}\nFreq\t:{s3}\n+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
    input("\nPress any key to continue...")

def read_validation_file(validation_filepath: str):
    df = pd.read_csv(validation_filepath)

    return df

def filter_FPs(validation_df):
    filtered_df = validation_df[(validation_df['prompts_plus_orth'] == 0) &
                                (validation_df['prompts_plus_hypo'] == 1)]
    return filtered_df

def get_freq_FP_prompts(validation_df_FP_only):
    freq_df = validation_df_FP_only['prompt'].value_counts().reset_index()
    
    return freq_df