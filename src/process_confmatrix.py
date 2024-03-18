from os import makedirs
from pandas import DataFrame
from os.path import join
from confusion_matrix import add_binaries, create_confusion_matrix, export_conf_matrix, export_df_data, get_binary_lists, read_prompt_file
from models.participant_session import AlignedSession


def process_conf_matrix(sesh: AlignedSession, filtered_df: DataFrame, participant_audio_id: str, base_dir: str):
    print(f"Processing Confusion matrix for path {sesh.aligned_sctk_output_folder}")
    base_df_with_binaries = process_df(participant_audio_id)
    base_data_dir = join(base_dir, "all_data")
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

    ref_list_binary, hyp_list_binary = get_binary_lists(base_df_with_binaries)
    conf_matrix = create_confusion_matrix(ref_list_binary, hyp_list_binary)
    export_conf_matrix(base_data_dir, conf_matrix)


def get_prompt_file_name(participant_audio_id: str):
    if '2LG' in participant_audio_id:
        return "2LG_words.txt"
    elif '1LG' in participant_audio_id:
        return "1LG_words.txt"
    return "3+4LG_words.txt"


def process_df(participant_audio_id: str):
    prompt_file_name = get_prompt_file_name(participant_audio_id)
    base_df = DataFrame.from_dict({
        'id': participant_audio_id,
        'prompt': read_prompt_file(prompt_file_name)
    })

    base_df_with_binaries = add_binaries(base_df)

    return base_df_with_binaries