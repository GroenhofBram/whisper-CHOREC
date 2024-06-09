from os import makedirs
import sys
from pandas import DataFrame, Series, concat, merge
from os.path import join
from adagt.run_init import two_way_alignment
from confusion_matrix import add_binaries, create_confusion_matrix, export_conf_matrix, export_df_data, get_binary_lists, read_prompt_file

def process_conf_matrix(asr_transcriptions: str, participant_audio_id: str, base_session_folder: str, ortho_df: DataFrame):
    print(f"Processing Confusion matrix for path {base_session_folder}")
    base_df_with_binaries = process_df(participant_audio_id, asr_transcriptions, ortho_df)
    base_data_dir = join(base_session_folder, "all_data")
    makedirs(base_data_dir, exist_ok=True) 

    csv_filename = f"{participant_audio_id}.csv"
    export_df_data(
        df=base_df_with_binaries,
        file_name=csv_filename,
        base_dir=base_data_dir,
        is_csv=True
    )

    json_filename = f"{participant_audio_id}.json"
    export_df_data(
        df=base_df_with_binaries,
        file_name=json_filename,
        base_dir=base_data_dir,
        is_csv=False
    )

    print(f"Created {base_data_dir} =====> {csv_filename}")
    ref_list_binary, hyp_list_binary = get_binary_lists(base_df_with_binaries)
    conf_matrix = create_confusion_matrix(ref_list_binary, hyp_list_binary)
    export_conf_matrix(base_data_dir, conf_matrix)

# Prompts
def get_prompt_file_name(participant_audio_id: str):
    if '2LG' in participant_audio_id:
        return "2LG_words.txt"
    elif '1LG' in participant_audio_id:
        return "1LG_words.txt"
    return "3+4LG_words.txt"

def generate_df(prompts_list: list[str], asr_transcriptions: str):
    prompts = " ".join(prompts_list)
    aligned_df = two_way_alignment(prompts, asr_transcriptions.lower())
    print("\n\nADAGT\n\n")
    print(aligned_df)
    return aligned_df.reset_index().rename(columns={"index": "prompt", "aligned_asrTrans": "hypothesis", "reversed_aligned_asrTrans": "hypothesis_rev"})
    
# DF created for binaries
def process_df(participant_audio_id: str, asr_transcriptions: str, ortho_df: DataFrame):
    prompt_file_name = get_prompt_file_name(participant_audio_id)
    prompts_list = read_prompt_file(prompt_file_name)
    print(prompts_list)
    end_df = generate_df(prompts_list, asr_transcriptions)
    print(len(end_df.index))
    print(len(ortho_df["orthography"]))
    print(ortho_df)
    base_df = concat([end_df, ortho_df["orthography"]], axis=1)
    print("\nDF WITHOUT BINARIES")
    print(base_df)

    base_df = base_df.rename(columns = {"orthography": "reference"})
    base_df_with_binaries = add_binaries(base_df)

    base_df_with_binaries = base_df_with_binaries.drop(columns=['correct'])
    base_df_with_binaries['id'] = participant_audio_id


    print("\nDF WITH BINARIES")
    print(base_df_with_binaries)


    return base_df_with_binaries