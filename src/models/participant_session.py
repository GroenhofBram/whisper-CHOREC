from dataclasses import dataclass

from pandas import DataFrame

from src.models.participantfile import ParticipantFile

@dataclass
class ParticipantSession:
    textgrid_participant_file: ParticipantFile
    wav_participant_file: ParticipantFile
    participant_audio_id: str



@dataclass
class ProcessedParticipantSession:
    base_session_folder: str
    sctk_out_unaligned_folder: str

    # aligned_csv_dataframe_path: Optional[str] = None

    # def with_filtered_dataframe(self, df_path: str):
    #     self.aligned_csv_dataframe_path = df_path
    #     return self
    

@dataclass
class FilteredDataframeSession:
    filtered_df: DataFrame
    filtered_df_file_path: str

@dataclass
class AlignedSession:
    aligned_sctk_output_folder: str
    aligned_ref_csv_path: str
    aligned_hyp_csv_path: str