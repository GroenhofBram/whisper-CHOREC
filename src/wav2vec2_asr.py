from re import sub as regex_sub
from transformers import pipeline

from constants import WAV2VEC2_MODEL_NAME
from src.models.participantfile import ParticipantFile
from src.cuda import DEVICE

def wav2vec2_asr(input_participant_wav_file: ParticipantFile) -> str:
    # CHOREC: Tier 2 = prompts, Tier 3 = orthographic transcription
    file_path = input_participant_wav_file.full_file_path
    # may need to take this out 
    pipe = pipeline(model=WAV2VEC2_MODEL_NAME, device=DEVICE)

    # Chunk length = windows (?)
    # Stides = context for each window for better inference (?)
    output = pipe(file_path, chunk_length_s=10, stride_length_s=(4, 2))

    ASR_transcription = regex_sub(r'\s+', ' ', output['text'])

    return ASR_transcription