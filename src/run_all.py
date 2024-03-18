from os.path import join

from align_filtered_dataframe import create_aligned_csvs
from coltolist import column_to_list
from pathing import get_abs_folder_path
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


def main():
    wav2vec2chorec_main()
    sctk_run_unaligned()
    wav2vec2chorec_json()
    align_filtered()
    sctk_run_aligned()
    conf_mat()

# Do not use: 'S07C049M8_1LG'
def main_generalised():
    print("- Running generalised process -")
    base_dir = get_base_dir_for_generalised_path()
    base_output_dir_in_repo = get_abs_folder_path("output")
    wav_files = glob(f"{base_dir}/**/*LG.wav", recursive=True)
    # print(wav_files)
    wav_files_with_properties = generate_file_properties(wav_files, base_dir)
    participant_sessions = get_participant_sessions_with_textgrids(wav_files_with_properties, base_dir)

    print(f"\nFound sessions: {len(participant_sessions)}")

    failed_runs = []
    for sesh in list(participant_sessions[0:3]):
        try:
            processed_session = process_session(sesh, base_output_dir_in_repo)
            filtered_df_session = process_unaligned_json_to_filtered_csv(sesh, processed_session)
            aligned_session = create_aligned_csvs(
                f_df=filtered_df_session.filtered_df,
                participant_audio_id=sesh.participant_audio_id,
                base_dir=processed_session.base_session_folder
            )

            process_conf_matrix(aligned_session, filtered_df_session.filtered_df, sesh.participant_audio_id, processed_session.base_session_folder)

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
    
    process_big_file(base_dir='')


def process_big_file(base_dir: str):
    all_files = glob(f"{base_dir}/all_data/**.csv")