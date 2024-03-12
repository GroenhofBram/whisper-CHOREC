
from models.participant_session import ParticipantSession
from sctk import run_sctk
from sctk_align import get_repr_df
from textgrid import load_text_grid_as_df
from wav2vec2_asr import wav2vec2_asr
from os.path import join
from os import makedirs

def process_session(sesh: ParticipantSession, base_output_dir_in_repo: str):
    print(f"\nProcessing {sesh.participant_audio_id}")
    sesh_audio_id_words = f"{sesh.participant_audio_id}-words"
    wav2vec2_ran_transforms_asr_transcription = wav2vec2_asr(sesh.wav_participant_file)
    base_session_folder = join(base_output_dir_in_repo, sesh.participant_audio_id)
    makedirs(base_session_folder, exist_ok=True)
    sctk_output_folder = join(base_session_folder, "sctk_out_unaligned")
    makedirs(sctk_output_folder, exist_ok=True)
    
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
    
    run_sctk(
        output_folder=sctk_output_folder,
        ref_csv_path=ref_csv_path,
        hyp_csv_path=hyp_csv_path,
    )