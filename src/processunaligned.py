from os.path import join
from build_unfiltered_dataframe import build_unfiltered_and_filtered_dataframes
from models.participant_session import ParticipantSession, ProcessedParticipantSession

from json_load_file import extract_words_from_json, load_json_file

def process_unaligned_json_to_filtered_csv(sesh: ParticipantSession, processed_session: ProcessedParticipantSession):
    print(f"Processing unaligned CSVs for {sesh.participant_audio_id}")
    print(f"Folder BASE: {processed_session.base_session_folder}")

    unaligned_json_file_path = join(processed_session.sctk_out_unaligned_folder, "hyp1.trn.pra.json")

    unaligned_sctk_output = load_json_file(unaligned_json_file_path)

    filtered_sesh = build_unfiltered_and_filtered_dataframes(unaligned_sctk_output, processed_session.base_session_folder)
    return filtered_sesh