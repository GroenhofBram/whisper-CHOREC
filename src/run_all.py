from os import makedirs
from os.path import join

from pandas import DataFrame, concat, read_csv

from align_filtered_dataframe import create_aligned_csvs
from coltolist import column_to_list
from constants import WAV2VEC2_MODEL_NAME_FLDR
from csvtodataframe import csv_to_df
from pathing import get_abs_folder_path, get_base_dir_folder_path
from process_confmatrix import process_conf_matrix
from process_session import process_session
from processunaligned import process_unaligned_json_to_filtered_csv
from sctk_align import get_repr_df
from src.wav2vec2chorec import main as wav2vec2chorec_main
from src.sctkrun import main as sctk_run_unaligned
from src.wav2vec2chorecjson import main as wav2vec2chorec_json
from src.filteredalignment import main as align_filtered
from src.sctk_run_aligned import main as sctk_run_aligned
from src.confusion_matrix import main as conf_mat

from generalisedbasedir import get_base_dir_for_generalised_path
from glob_properties import generate_file_properties
from participantsession import  get_participant_sessions_with_textgrids
from glob import glob


# def main():
#     wav2vec2chorec_main()
#     sctk_run_unaligned()
#     wav2vec2chorec_json()
#     align_filtered()
#     sctk_run_aligned()
#     conf_mat()

# Do not use: 'S07C049M8_1LG'
def main_generalised():
    print("- Running generalised process -")
    base_dir = get_base_dir_for_generalised_path()
    base_output_dir_in_repo = get_base_dir_folder_path("output", WAV2VEC2_MODEL_NAME_FLDR)
    makedirs(base_output_dir_in_repo, exist_ok=True)
    wav_files = glob(f"{base_dir}/**/*LG.wav", recursive=True)
    # print(wav_files)
    wav_files_with_properties = generate_file_properties(wav_files, base_dir)
    participant_sessions = get_participant_sessions_with_textgrids(wav_files_with_properties, base_dir)

    print(participant_sessions)
    print(f"\nFound sessions: {len(participant_sessions)}")

    failed_runs = []
    for sesh in participant_sessions:
        try:
            processed_session = process_session(sesh, base_output_dir_in_repo)
            filtered_df_session = process_unaligned_json_to_filtered_csv(sesh, processed_session)
            aligned_session = create_aligned_csvs(
                f_df=filtered_df_session.filtered_df,
                participant_audio_id=sesh.participant_audio_id,
                base_dir=processed_session.base_session_folder
            )

            ret = process_conf_matrix(aligned_session, filtered_df_session.filtered_df, sesh.participant_audio_id, processed_session.base_session_folder)

        except Exception as e:
            msg = e
            if hasattr(e, 'message'):
                msg = e.message
            
            failed_runs.append({
                'id': sesh.participant_audio_id,
                'ex': msg
            })

    if len(failed_runs) > 0:  
        print(failed_runs)
    
    process_all_conf_matrices(base_dir=base_output_dir_in_repo)
    process_all_data_files(base_dir=base_output_dir_in_repo)



def process_all_conf_matrices(base_dir: str):
    conf_mat_output_folder = join(base_dir, "all_data_output")
    makedirs(conf_mat_output_folder, exist_ok=True)
    conf_mat_big_file_name = join(conf_mat_output_folder, "total_conf_matrix.csv")



    empty_conf_mat_df = DataFrame([[0, 0], [0, 0]], index=None)
    # print(empty_conf_mat_df)
    for data_file_path in glob(f"{base_dir}/**/all_data/Conf_matrix.csv"):
        loaded_df = read_csv(data_file_path, header=None)
        empty_conf_mat_df = empty_conf_mat_df.add(loaded_df, fill_value=0)
    empty_conf_mat_df.to_csv(conf_mat_big_file_name, index=False, header=None)
        


def process_all_data_files(base_dir: str):
    all_data_files = glob(f"{base_dir}/**/all_data/*LG.csv")
    conf_mat_big_file_name = join(base_dir, "all_data_output", "total_alldata_df.csv")

    base_df = DataFrame(columns=["id","prompt","reference","hypothesis","prompts_plus_orth","prompts_plus_hypo"])

    for data_file_path in all_data_files:
        loaded_df = read_csv(data_file_path)
        base_df = concat([base_df, loaded_df])
    base_df.to_csv(conf_mat_big_file_name, index=False)
    
