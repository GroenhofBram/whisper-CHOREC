#################### INSPECT OUTPUT, SOMETHING WARNING

import os
import librosa
import numpy as np
from glob import glob
import pandas as pd

from generalisedbasedir import get_base_dir_for_generalised_path
from glob_properties import generate_file_properties
from participantsession import get_participant_sessions_with_textgrids
from pathing import get_abs_folder_path

def main():
    base_dir = get_base_dir_for_generalised_path()
    # base_output_dir_in_repo = get_abs_folder_path("output")

    wav_file_folders = os.path.join(base_dir, "output")
    wav_files_in_folder = os.path.join(wav_file_folders, "**/*LG.wav")

    wav_files = glob(wav_files_in_folder, recursive=True)
    print(wav_files)
    wav_files_with_properties = generate_file_properties(wav_files, base_dir)
    participant_sessions = get_participant_sessions_with_textgrids(wav_files_with_properties, base_dir)
    participant_SNR_df_empty = get_empty_SNR_df(participant_sessions)
    participant_SNR_df_filled = fill_SNR_values(wav_files, participant_SNR_df_empty)
    export_participant_SNR_df_filled_to_csv(participant_SNR_df_filled)

def export_participant_SNR_df_filled_to_csv(participant_SNR_df_filled):
    output_folder = os.path.abspath(os.path.join(__file__, "../../output/all_data_output"))
    file_name = os.path.join(output_folder, "SNR_data.csv")

    participant_SNR_df_filled.to_csv(file_name, index=False)
    print(f"SNR saved at: {file_name}")


def get_empty_SNR_df(participant_sessions):
    participant_list = fill_participant_list(participant_sessions)
    #participant_SNR_df_empty = pd.DataFrame(participant_list)
    participant_SNR_df_empty = pd.DataFrame(participant_list, columns=['id', 'SNR'])  
    return participant_SNR_df_empty

def fill_participant_list(participant_sessions) -> list:
    participant_list = []

    for session in participant_sessions:
        participant_audio_id = session.participant_audio_id
        snr = 0  # Set SNR to 0 for now, changing later

        participant_list.append(
            {
                'id': participant_audio_id,
                'SNR': snr
                })
    
    return participant_list

def fill_SNR_values(wav_files, participant_SNR_df_empty):
    for index, row in participant_SNR_df_empty.iterrows():
        participant_audio_id = row['id']
        wav_file_path = find_wav_file(wav_files, participant_audio_id)
        if wav_file_path:
            snr = calculate_SNR(wav_file_path)
            participant_SNR_df_empty.at[index, 'SNR'] = snr
        else:
            print(f"No WAV file found for participant {participant_audio_id}")
    participant_SNR_df_empty['SNR'] = participant_SNR_df_empty['SNR'].astype(float)
    return participant_SNR_df_empty

def find_wav_file(wav_files, participant_audio_id):
    for wav_file in wav_files:
        if participant_audio_id in wav_file:
            return wav_file
    return None

def calculate_SNR(wav_file_path):
    y, sr = librosa.load(wav_file_path)
    signal_power = np.sum(y ** 2) / len(y)
    noise_power = np.mean(y ** 2)
    snr = 10 * np.log10(signal_power / noise_power)
    return snr






