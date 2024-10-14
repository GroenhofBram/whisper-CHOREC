from transformers import pipeline
import re, platform
import pandas as pd
from file_path import get_file_path
from textgrid import use_text_grids
from constants import WAV2VEC2_MODEL_NAME
from cuda import DEVICE

transcription_audio_file_name = "S01C002V1_2LG.wav"
tgt_grid_file_name = "S01C002V1_2LG_f01.TextGrid"

def main():
    ASR_transcription = run_wav2vec2()
    tgt_df_repr = use_text_grids(tgt_grid_file_name)
    sctk_align(ASR_transcription, tgt_df_repr)


def run_wav2vec2():
    # CHOREC: Tier 2 = prompts, Tier 3 = orthographic transcription
    file_path = get_file_path(transcription_audio_file_name)
    # may need to take this out 
    pipe = pipeline(model=WAV2VEC2_MODEL_NAME, device=DEVICE)

    # Chunk length = windows (?)
    # Stides = context for each window for better inference (?)
    output = pipe(file_path, chunk_length_s=10, stride_length_s=(4, 2))

    ASR_transcription = re.sub(r'\s+', ' ', output['text'])
    
    # print(output)
    # print(ASR_transcription)

    return ASR_transcription

def sctk_align(ASR_transcription, tgt_df_repr):
    
    # # # # HYPOTHESIS
    d = {'utterance_id': ["S01C002V1_2LG-words"] ,
        'transcript': [ASR_transcription.lower()]}
    df = pd.DataFrame(data=d)
    df.to_csv('output/hyp.csv', index=False)


    # # # # REFERENCE
    d = {'utterance_id': ["S01C002V1_2LG-words"],
        'transcript': [" ".join(tgt_df_repr.orthography.values)]} # Or prompt: " ".join(tgt_df_repr.prompt.values)
    df = pd.DataFrame(data=d)
    df.to_csv('output/ref.csv', index=False)