# Think about using V2, better for children's speech

from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import torch
import re, platform
import pandas as pd
from src.file_path import get_file_path
from src.textgrid import use_text_grids
from src.constants import WHISPER_MODEL_NAME
from src.cuda import DEVICE

def main():
    run_whisper()

def run_whisper():
    # CHOREC: Tier 2 = prompts, Tier 3 = orthographic transcription
    file_path = "files//test_glob//S01C001M1//S01C002V1_3+4LG.wav"

    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    model_id = WHISPER_MODEL_NAME

    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True)
    model.to(DEVICE)

    processor = AutoProcessor.from_pretrained(model_id)
    
    # may need to take this out 
    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        max_new_tokens=128,
        chunk_length_s=30,
        batch_size=16,
        return_timestamps=True,
        torch_dtype=torch_dtype,
        device=DEVICE,
    )

    result = pipe(file_path)
    print("- - - - - - - - - RESULT\n")
    print(result)
    print("- - - - - - - - - RESULT\n")

    ASR_transcription = re.sub(r'\s+', "", result['text'])
    


    print("- - - - - - - - - JUST TEXT\n")
    print(ASR_transcription)
    print("- - - - - - - - - JUST TEXT\n")

    # output = pipe(file_path, chunk_length_s=10, stride_length_s=(4, 2))

    # ASR_transcription = re.sub(r'\s+', ' ', output['text'])
    
    # # print(output)
    # # print(ASR_transcription)

    # return ASR_transcription

