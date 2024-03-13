from pathing import get_abs_folder_path
from process_session import process_session
from processunaligned import proccess_unaligned_csvs
from sctk_align import get_repr_df
from src.wav2vec2chorec import main as wav2vec2chorec_main
from src.sctkrun import main as sctk_run_unaligned
from src.wav2vec2chorecjson import main as wav2vec2chorec_json
from src.filteredalignment import main as align_filtered
from src.sctk_run_aligned import main as sctk_run_aligned
from src.confusion_matrix import main as conf_mat


from generalisedbasedir import get_base_dir_for_generalised_path
from glob_properties import generate_file_properties
from textgrid import load_text_grid_as_df
from wav2vec2_asr import wav2vec2_asr
from participantsession import  get_participant_sessions_with_textgrids
from glob import glob

from os.path import join
from os import makedirs
from os.path import exists


def main():
    wav2vec2chorec_main()
    sctk_run_unaligned()
    wav2vec2chorec_json()
    align_filtered()
    sctk_run_aligned()
    conf_mat()

# Do not use: 'S04C031M2_1LGPseudo' & 'S07C049M8_1LG'
def main_generalised():
    print("- Running generalised process -")
    base_dir = get_base_dir_for_generalised_path()
    base_output_dir_in_repo = get_abs_folder_path("output")
    wav_files = glob(f"{base_dir}/**/*.wav", recursive=True)
    # No pseudo
    # wav_files = glob(f"{base_dir}/**/*LG.wav", recursive=True)
    wav_files_with_properties = generate_file_properties(wav_files, base_dir)
    participant_sessions = get_participant_sessions_with_textgrids(wav_files_with_properties, base_dir)

    print(f"\nFound sessions: {len(participant_sessions)}")

    failed_runs = []
    for sesh in participant_sessions:
        # process_session(sesh, base_output_dir_in_repo) # #
        try:
            process_session(sesh, base_output_dir_in_repo)
            proccess_unaligned_csvs(sesh, base_output_dir_in_repo)
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