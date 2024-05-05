
from os.path import join

from pandas import DataFrame, Series, concat

from calculate_snr import calculate_snr
from models.participant_session import ParticipantSession
from models.participantfile import ParticipantFile

def process_snr_data(base_dir: str, sessions: list[ParticipantSession]):
    snr_file_name = join(base_dir, "all_data_output", "snr_data_output.csv")

    base_df = DataFrame(columns=["participant_id","snr"])

    for session in sessions:
        snr = calculate_snr(session.wav_participant_file.full_file_path)
        base_df.loc[len(base_df)] = { "participant_id": session.participant_audio_id, "snr": snr }

    base_df.to_csv(snr_file_name, index=False)
    