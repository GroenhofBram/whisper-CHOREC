import pandas as pd
import re
from constants import WAV2VEC2_MODEL_NAME_FLDR
from os.path import join
from pathing import get_abs_folder_path

def main():
    # Preparing files
    filepath, filepath_output = get_filename(csv_name = "training_set_base.csv")
    print(filepath_output)
    data = read_error_csv(filepath)
    error_type_df = create_empty_error_type_df()

    error_type_df = add_nospace(data, error_type_df)
    error_type_df = add_oe_oo(data, error_type_df)
    error_type_df = add_k_c(data, error_type_df)
    error_type_df = add_long_short_vowel(data, error_type_df) 
    error_type_df = add_au_ou(data, error_type_df)
    error_type_df = add_start_plosive(data, error_type_df)
    error_type_df = add_end_plosive(data, error_type_df)
    error_type_df = add_double_single_consonant(data, error_type_df, asterisk = True)
    error_type_df = add_double_single_consonant(data, error_type_df, asterisk = False)
    error_type_df = add_i_replace(data, error_type_df)
    error_type_df = add_ch_sh(data, error_type_df)
    error_type_df = add_start_fricative(data, error_type_df)
    error_type_df = add_nasal(data, error_type_df)


    ################################################### TODO
    # Insertion errors i.e., verstoppertje/verstoppetje
    # Deletion of final W i.e., gauw/gau
    # Reductions, i.e.: Chocolade/chocola
    # Changing plosive + liquid to just plosive i.e.: groen/goen

    print(error_type_df)

    print(sum(error_type_df["count"]))

    save_to_csv(error_type_df, filepath_output)

def save_to_csv(error_type_df, filepath_output):
    error_type_df.to_csv(filepath_output)

def add_nasal(data, error_type_df):
    rows_to_add = []


    for i, row in data.iterrows():
        if differ_by_nasal(row['prompt'], row['hypothesis']):
            new_row = {
                'error_type': 'nasal',
                'prompt': row['prompt'],
                'hypothesis': row['hypothesis'],
                'count': row['count'],
                'prompt_aligned': row['prompt_aligned']
            }
            rows_to_add.append(new_row)

    if rows_to_add:
        error_type_df = pd.concat([error_type_df, pd.DataFrame(rows_to_add)], ignore_index=True)
    
    return error_type_df


def differ_by_nasal(prompt, hypothesis):
    nasal_pairs = [('n', 'm'), ('m', 'n'), ('n', 'ng'),
                   ('ng', 'n'), ('m', 'ng'), ('ng', 'm'),
                   ('n', 'nk'), ('nk', 'n'), ('m', 'nk'), ('nk', 'm'), ('ng', 'nk'), ('nk', 'ng')]
    
    for p1, p2 in nasal_pairs:
        if (p1 in prompt and p2 in hypothesis) or (p1 in hypothesis and p2 in prompt):
            transformed_prompt = prompt.replace(p1, p2)
            transformed_hypothesis = hypothesis.replace(p1, p2)
            if transformed_prompt == transformed_hypothesis:
                return True
            
    return False

def add_start_fricative(data, error_type_df):
    rows_to_add = []


    for i, row in data.iterrows():
        if differ_by_start_fricative(row['prompt'], row['hypothesis']):
            new_row = {
                'error_type': 'start_fricative',
                'prompt': row['prompt'],
                'hypothesis': row['hypothesis'],
                'count': row['count'],
                'prompt_aligned': row['prompt_aligned']
            }
            rows_to_add.append(new_row)

    if rows_to_add:
        error_type_df = pd.concat([error_type_df, pd.DataFrame(rows_to_add)], ignore_index=True)
    
    return error_type_df

def differ_by_start_fricative(prompt, hypothesis):
    fricative_pairs = [("f", "v"), ("s", "z"), ("g", "ch")]
    
    for p1, p2 in fricative_pairs:
        if (prompt.startswith(p1) and hypothesis.startswith(p2) and prompt[1:] == hypothesis[1:]) or \
           (prompt.startswith(p2) and hypothesis.startswith(p1) and prompt[1:] == hypothesis[1:]):
            return True
    return False

def add_ch_sh(data, error_type_df):
    rows_to_add = []

    for i, row in data.iterrows():
        if differ_by_sc_ch(row['prompt'], row['hypothesis']):
            new_row = {
                'error_type': 'ch/sh',
                'prompt': row['prompt'],
                'hypothesis': row['hypothesis'],
                'count': row['count'],
                'prompt_aligned': row['prompt_aligned']
            }
            rows_to_add.append(new_row)

    if rows_to_add:
        error_type_df = pd.concat([error_type_df, pd.DataFrame(rows_to_add)], ignore_index=True)
    return error_type_df

def differ_by_sc_ch(prompt, hypothesis):
    condition1 = prompt.replace("ch", "sh") == hypothesis
    condition2 = prompt.replace("sh", "ch") == hypothesis
    return condition1 or condition2 

def add_i_replace(data, error_type_df):
    rows_to_add = []

    for i, row in data.iterrows():
        if differ_by_i(row['prompt'], row['hypothesis']):
            new_row = {
                'error_type': 'i_replace',
                'prompt': row['prompt'],
                'hypothesis': row['hypothesis'],
                'count': row['count'],
                'prompt_aligned': row['prompt_aligned']
            }
            rows_to_add.append(new_row)

    if rows_to_add:
        error_type_df = pd.concat([error_type_df, pd.DataFrame(rows_to_add)], ignore_index=True)
    return error_type_df

def differ_by_i(prompt, hypothesis):
    condition1 = prompt.replace("i", "y") == hypothesis
    condition2 = prompt.replace("y", "i") == hypothesis
    return condition1 or condition2 

def add_double_single_consonant(data, error_type_df, asterisk):
    rows_to_add = []

    if asterisk:
        for i, row in data.iterrows():
            if differ_by_double_single_consonant(row['prompt'], row['hypothesis']):
                new_row = {
                    'error_type': 'double/single consonant',
                    'prompt': row['prompt'],
                    'hypothesis': row['hypothesis'],
                    'count': row['count'],
                    'prompt_aligned': row['prompt_aligned']
                }
                rows_to_add.append(new_row)
    
    else:
         for i, row in data.iterrows():
            if differ_by_double_single_consonant_no_asterisk(row['prompt'], row['hypothesis']):
                new_row = {
                    'error_type': 'double/single consonant',
                    'prompt': row['prompt'],
                    'hypothesis': row['hypothesis'],
                    'count': row['count'],
                    'prompt_aligned': row['prompt_aligned']
                }
                rows_to_add.append(new_row)       

    if rows_to_add:
        error_type_df = pd.concat([error_type_df, pd.DataFrame(rows_to_add)], ignore_index=True)

    return error_type_df

def differ_by_double_single_consonant_no_asterisk(prompt, hypothesis):
    pattern = r'([bcdfghjklmnpqrstvwxyz])\1|\*([bcdfghjklmnpqrstvwxyz])'
    base_prompt = re.sub(pattern, r'\1', prompt)
    base_hypothesis = re.sub(pattern, r'\1', hypothesis)
    
    return base_prompt == base_hypothesis    

def differ_by_double_single_consonant(prompt, hypothesis):
    pattern_double_to_single = r'([bcdfghjklmnpqrstvwxyz])\1'  # Matches double consonants
    pattern_single_to_double = r'\*([bcdfghjklmnpqrstvwxyz])'  # Matches "* followed by single consonant"
    

    base_prompt_double_to_single = re.sub(pattern_double_to_single, r'*\1', prompt)
    base_prompt_single_to_double = re.sub(pattern_single_to_double, r'\1\1', prompt)
    
    base_hypothesis_double_to_single = re.sub(pattern_double_to_single, r'*\1', hypothesis)
    base_hypothesis_single_to_double = re.sub(pattern_single_to_double, r'\1\1', hypothesis)
    
    return (base_prompt_double_to_single == base_hypothesis_double_to_single) or \
           (base_prompt_single_to_double == base_hypothesis_single_to_double)

def add_end_plosive(data, error_type_df):
    rows_to_add = []

    # Loop through each row in the data DataFrame
    for _, row in data.iterrows():
        if differ_by_end_plosive(row['prompt'], row['hypothesis']):
            # Create a new row with error_type "end_plosive"
            new_row = {
                'error_type': 'end_plosive',
                'prompt': row['prompt'],
                'hypothesis': row['hypothesis'],
                'count': row['count'],
                'prompt_aligned': row['prompt_aligned']
            }
            # Append the new row to the list
            rows_to_add.append(new_row)

    # Concatenate the rows_to_add to error_type_df
    if rows_to_add:
        error_type_df = pd.concat([error_type_df, pd.DataFrame(rows_to_add)], ignore_index=True)
    
    return error_type_df

def differ_by_end_plosive(prompt, hypothesis):
    plosive_pairs = [("p", "b"), ("t", "d"), ("k", "g")]
    
    for p1, p2 in plosive_pairs:
        if (prompt.endswith(p1) and hypothesis.endswith(p2) and prompt[:-1] == hypothesis[:-1]) or \
           (prompt.endswith(p2) and hypothesis.endswith(p1) and prompt[:-1] == hypothesis[:-1]):
            return True
    return False

def add_start_plosive(data, error_type_df):
    rows_to_add = []


    for i, row in data.iterrows():
        if differ_by_start_plosive(row['prompt'], row['hypothesis']):
            new_row = {
                'error_type': 'start_plosive',
                'prompt': row['prompt'],
                'hypothesis': row['hypothesis'],
                'count': row['count'],
                'prompt_aligned': row['prompt_aligned']
            }
            rows_to_add.append(new_row)

    if rows_to_add:
        error_type_df = pd.concat([error_type_df, pd.DataFrame(rows_to_add)], ignore_index=True)
    
    return error_type_df

def differ_by_start_plosive(prompt, hypothesis):
    plosive_pairs = [("p", "b"), ("t", "d"), ("k", "g")]
    
    for p1, p2 in plosive_pairs:
        if (prompt.startswith(p1) and hypothesis.startswith(p2) and prompt[1:] == hypothesis[1:]) or \
           (prompt.startswith(p2) and hypothesis.startswith(p1) and prompt[1:] == hypothesis[1:]):
            return True
    return False

def add_long_short_vowel(data, error_type_df):
    rows_to_add = []

    # Loop through each row in the data DataFrame
    for i, row in data.iterrows():
        if differ_by_long_short_vowel(row['prompt'], row['hypothesis']):
            # Create a new row with error_type "long/short vowel"
            new_row = {
                'error_type': 'long/short vowel',
                'prompt': row['prompt'],
                'hypothesis': row['hypothesis'],
                'count': row['count'],
                'prompt_aligned': row['prompt_aligned']
            }
            # Append the new row to the list
            rows_to_add.append(new_row)

    # Concatenate the rows_to_add to error_type_df
    if rows_to_add:
        error_type_df = pd.concat([error_type_df, pd.DataFrame(rows_to_add)], ignore_index=True)
    
    return error_type_df

def differ_by_long_short_vowel(prompt, hypothesis):
    long_vowels = ["aa", "ee", "oo", "uu", "ii",
                   "ei", "ij", "ie", 
                   "au", "ou", "eu",
                   "aai", "ooi", "eeu"]
    
    for long_vowel in long_vowels:
        # Check if long vowel in prompt is replaced by a single vowel or a vowel with a "*"
        if long_vowel in prompt:
            single_vowel = long_vowel[0]
            if (prompt.replace(long_vowel, single_vowel) == hypothesis or 
                prompt.replace(long_vowel, f"{single_vowel}*") == hypothesis or
                prompt.replace(long_vowel, f"*{single_vowel}") == hypothesis):
                return True
        # Check if single vowel or vowel with "*" in prompt is replaced by long vowel
        if long_vowel in hypothesis:
            single_vowel = long_vowel[0]
            if (hypothesis.replace(long_vowel, single_vowel) == prompt or 
                hypothesis.replace(long_vowel, f"{single_vowel}*") == prompt or
                hypothesis.replace(long_vowel, f"*{single_vowel}") == hypothesis):
                return True
    return False

def add_k_c(data, error_type_df):
    rows_to_add = []

    for i, row in data.iterrows():
        if differ_by_k_c(row['prompt'], row['hypothesis']):
            new_row = {
                'error_type': 'k/c',
                'prompt': row['prompt'],
                'hypothesis': row['hypothesis'],
                'count': row['count'],
                'prompt_aligned': row['prompt_aligned']
            }
            rows_to_add.append(new_row)

    if rows_to_add:
        error_type_df = pd.concat([error_type_df, pd.DataFrame(rows_to_add)], ignore_index=True)
    return error_type_df

def differ_by_k_c(prompt, hypothesis):
    condition1 = prompt.replace("k", "c") == hypothesis
    condition2 = prompt.replace("c", "k") == hypothesis
    return condition1 or condition2

def add_oe_oo(data, error_type_df):
    rows_to_add = []
    for i, row in data.iterrows():
        if differ_by_oe_oo(row['prompt'], row['hypothesis']):
            # Create a new row with error_type "oe/oo"
            new_row = {
                'error_type': 'oe/oo',
                'prompt': row['prompt'],
                'hypothesis': row['hypothesis'],
                'count': row['count'],
                'prompt_aligned': row['prompt_aligned']
            }
            # Append the new row to the list
            rows_to_add.append(new_row)

    
    if rows_to_add:
        error_type_df = pd.concat([error_type_df, pd.DataFrame(rows_to_add)], ignore_index=True)
    
    return error_type_df

def differ_by_oe_oo(prompt, hypothesis):
    condition1 = prompt.replace("oe", "oo") == hypothesis
    condition2 = prompt.replace("oo", "oe") == hypothesis
    return condition1 or condition2

def add_au_ou(data, error_type_df):
    rows_to_add = []

    for i, row in data.iterrows():
        if differ_by_au_ou(row['prompt'], row['hypothesis']):
            
            new_row = {
                'error_type': 'au/ou',
                'prompt': row['prompt'],
                'hypothesis': row['hypothesis'],
                'count': row['count'],
                'prompt_aligned': row['prompt_aligned']
            }
            
            rows_to_add.append(new_row)

    if rows_to_add:
        error_type_df = pd.concat([error_type_df, pd.DataFrame(rows_to_add)], ignore_index=True)
    
    return error_type_df

def differ_by_au_ou(prompt, hypothesis):
    condition1 = prompt.replace("au", "ou") == hypothesis
    condition2 = prompt.replace("ou", "au") == hypothesis

    return condition1 or condition2

def add_nospace(data, error_type_df):
    rows_to_add = []

    for i, row in data.iterrows():
        if check_nospace_conditions(row['prompt'], row['hypothesis']):
            new_row = {
                'error_type': 'nospace',
                'prompt': row['prompt'],
                'hypothesis': row['hypothesis'],
                'count': row['count'],
                'prompt_aligned': row['prompt_aligned']
            }
            rows_to_add.append(new_row)

    if rows_to_add:
        error_type_df = pd.concat([error_type_df, pd.DataFrame(rows_to_add)], ignore_index=True)
    
    return error_type_df

def check_nospace_conditions(prompt, hypothesis):
    hypothesis_no_space = hypothesis.replace(" ", "")
    same_without_spaces = hypothesis_no_space == prompt
    no_asterisk = "*" not in hypothesis
    return same_without_spaces and no_asterisk
    
def create_empty_error_type_df():
    columns = ['error_type', 'prompt', 'hypothesis', 'count', 'prompt_aligned']
    empty_df = pd.DataFrame(columns=columns)
    return empty_df

def read_error_csv(filepath: str):
    data = pd.read_csv(filepath)
    return data

def get_filename(csv_name: str):
    base_output_dir_in_repo = get_abs_folder_path("output")
    csv_dir = join(base_output_dir_in_repo, WAV2VEC2_MODEL_NAME_FLDR)
    csv_dir = join(csv_dir, "all_data_output")
    csv_dir = join(csv_dir, "post_processing")
    csv_dir = join(csv_dir, "confusion_pairs")
    csv_file_name = join(csv_dir, csv_name)
    csv_file_name_output = join(csv_dir, "ERR_TYPES-" + csv_name)

    return csv_file_name, csv_file_name_output