from models.participant_session import ParticipantSession

def proccess_unaligned_csvs(sesh: ParticipantSession, base_output_dir_in_repo: str):
    print(base_output_dir_in_repo, sesh.participant_audio_id)