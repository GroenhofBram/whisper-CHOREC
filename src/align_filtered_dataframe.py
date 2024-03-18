from pandas import DataFrame
from os.path import join
from coltolist import column_to_list
from models.participant_session import AlignedSession
from sctk import run_sctk
from sctk_align import get_repr_df

def create_aligned_csvs(f_df: DataFrame, participant_audio_id: str, base_dir: str) -> AlignedSession:
    s_words_str = f"{participant_audio_id}-words"
    f_df_hyp_words = column_to_list(f_df, "hypothesis")
    f_hyp_df = get_repr_df(s_words_str, f_df_hyp_words)
    f_hyp_file_name = join(base_dir, 'hyp_filtered.csv')
    f_hyp_df.to_csv(f_hyp_file_name, index=False)


    f_df_ref_words = column_to_list(f_df, "reference")
    f_ref_df = get_repr_df(s_words_str,f_df_ref_words)
    f_ref_file_name = join(base_dir, 'ref_filtered.csv')
    f_ref_df.to_csv(f_ref_file_name, index=False)

    sctk_output_folder = join(base_dir, "sctk_out_aligned")
    
    run_sctk(
        output_folder=sctk_output_folder,
        ref_csv_path=f_ref_file_name,
        hyp_csv_path=f_hyp_file_name,
    )

    return AlignedSession(
        aligned_sctk_output_folder=sctk_output_folder,
        aligned_ref_csv_path=f_ref_file_name,
        aligned_hyp_csv_path=f_hyp_file_name,
    )