from generalisedbasedir import get_base_dir_for_generalised_path
from pathing import get_abs_folder_path
from os.path import join
from sklearn.metrics import confusion_matrix
import pandas as pd
import numpy as np
import csv

from constants import WAV2VEC2_MODEL_NAME_FLDR

def main():
    all_data_csv_dir, all_data_csv_file_path = get_all_data_csv_file_path()
    all_data_df = read_in_all_data_csv(all_data_csv_file_path)
    
    conf_mat_file_name = get_file_name_conf_mat(all_data_csv_dir)
    print(f"Generating confusion matrix and matrix for:\t {conf_mat_file_name}")

    # # # FILTERS: UNCOMMENT IF YOU WANT DIFFERENT SUBSET OF DATA # # #
    ## Specific word lists ##
    # all_data_df = filter_df_1LG(all_data_df)
    # all_data_df = filter_df_2LG(all_data_df)
    # all_data_df = filter_df_34LG(all_data_df)

    ## Correct or Incorrect Only ##
    # HOW TO AVOID DIVISION BY 0 FOR Metrics? --> Does it even make sense to calculate these metrics?
    # all_data_df = filter_df_corr_only(all_data_df)
    # all_data_df = filter_df_incorr_only(all_data_df)


    print(all_data_df)

    ref_list_binary, hyp_list_binary = get_binary_lists(all_data_df)

    conf_matrix = create_confusion_matrix(ref_list_binary, hyp_list_binary)
    print(conf_matrix)
    print(f"Storing confusion matrix:\t {conf_mat_file_name}")

    export_conf_matrix_to_csv(conf_matrix, conf_mat_file_name)



    print("Generating Metrics...")

    calculate_metrics(conf_matrix)

def filter_df_1LG(all_data_df):
    df_1LG = all_data_df[all_data_df['id'].str.contains('1LG')]
    
    return df_1LG

def filter_df_2LG(all_data_df):
    df_2LG = all_data_df[all_data_df['id'].str.contains('2LG')]
    
    return df_2LG

def filter_df_34LG(all_data_df):
    df_34LG = all_data_df[all_data_df['id'].str.contains('4LG')]
    
    return df_34LG

def filter_df_corr_only(all_data_df):
    df_corr_only = all_data_df[all_data_df['prompts_plus_orth'] == 0]
    
    return df_corr_only  

def filter_df_incorr_only(all_data_df):
    df_incorr_only = all_data_df[all_data_df['prompts_plus_orth'] == 1]
    
    return df_incorr_only  


def calculate_metrics(conf_matrix):
    tn, fp = conf_matrix[0]
    

    fn, tp = conf_matrix[1]

    
    accuracy = round((tp + tn) / np.sum(conf_matrix),3)    
    precision = round(tp / (tp + fp),3)
    recall = round(tp / (tp + fn),3)
    f1_score = round(2 * (precision * recall) / (precision + recall),3)
    mcc = round((tp * tn - fp * fn) / np.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn)), 3)


    # Print the results
    print("Accuracy\t:", accuracy)
    print("Precision\t:", precision)
    print("Recall\t\t:", recall)
    print("F1-score\t:", f1_score)
    print("MCC\t\t:", mcc)


def export_conf_matrix_to_csv(conf_matrix, conf_mat_file_name):
    with open(conf_mat_file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(conf_matrix)

def create_confusion_matrix(ref_list_binary, hyp_list_binary):
    conf_matrix = confusion_matrix(ref_list_binary, hyp_list_binary)

    return np.array(conf_matrix)

def get_binary_lists(all_data_df):
    ref_list_binary = all_data_df["prompts_plus_orth"].tolist()
    hyp_list_binary = all_data_df["prompts_plus_hypo"].tolist()
    return ref_list_binary, hyp_list_binary


def get_all_data_csv_file_path():
    base_output_dir_in_repo = get_abs_folder_path("output")
    
    all_data_csv_dir = join(base_output_dir_in_repo, WAV2VEC2_MODEL_NAME_FLDR)
    all_data_csv_dir = join(all_data_csv_dir, "all_data_output")
    all_data_csv_file_path = join(all_data_csv_dir, "total_alldata_df.csv")
    return all_data_csv_dir, all_data_csv_file_path 

def read_in_all_data_csv(all_data_csv_file_path):
    all_data_df = pd.read_csv(all_data_csv_file_path)
    return all_data_df

def get_file_name_conf_mat(all_data_csv_dir):
    user_file_name_input = input("Please enter an identifier filename for the confusion matrix, e.g.: 'test.csv':\t")

    return join(all_data_csv_dir, user_file_name_input)

