from pathing import get_abs_folder_path
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
from sctk import run_sctk

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


def main_generalised():
    print("Running generalised process")
    base_dir = get_base_dir_for_generalised_path()
    base_output_dir_in_repo = get_abs_folder_path("output")
    wav_files = glob(f"{base_dir}/**/*.wav", recursive=True)
    wav_files_with_properties = generate_file_properties(wav_files, base_dir)
    participant_sessions = get_participant_sessions_with_textgrids(wav_files_with_properties, base_dir)

    print(f"Found sessions: {len(participant_sessions)}")
    for sesh in participant_sessions:
        print(f"Processing {sesh.participant_audio_id}")
        sesh_audio_id_words = f"{sesh.participant_audio_id}-words"
        wav2vec2_ran_transforms_asr_transcription = wav2vec2_asr(sesh.wav_participant_file)
        base_session_folder = join(base_output_dir_in_repo, sesh.participant_audio_id)
        makedirs(base_session_folder, exist_ok=True)
        
        hyp_csv_path = join(base_session_folder, "hyp.csv")
        ref_csv_path = join(base_session_folder, "ref.csv")

        # print(base_session_folder)
        # print(hyp_csv_path)
        # print(ref_csv_path)
        # return None
        
        asr_hyp_transcription_df = get_repr_df(
            sesh_id_words_id=sesh_audio_id_words,
            words=wav2vec2_ran_transforms_asr_transcription.lower()
        )
        asr_hyp_transcription_df.to_csv(hyp_csv_path, index=False)

        tgt_df_repr = load_text_grid_as_df(sesh.textgrid_participant_file.full_file_path)
        tgt_df_repr_orth_transcription = " ".join(tgt_df_repr.orthography.values)
        
        orth_ref_transcription_df = get_repr_df(
            sesh_id_words_id=sesh_audio_id_words,
            words=tgt_df_repr_orth_transcription
        )
        orth_ref_transcription_df.to_csv(ref_csv_path, index=False)
        
        # run_sctk(
        #     output_folder=join(base_session_folder, "sctk_out_unaligned"),
        #     ref_csv_path=ref_csv_path,
        #     hyp_csv_path=hyp_csv_path,
        # )