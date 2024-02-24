from transformers import pipeline
import re, os

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

def main():
    print("fuck yuoj")

    # CHOREC: Tier 2 = prompts, Tier 3 = orthographic transcription
    file_path = os.path.join("..", "files/S01C002V1_2LG.wav")
    model_name="GroNLP/wav2vec2-dutch-large-ft-cgn"
    # pipe = pipeline(model=model_name)

    # # Chunk length = windows (?)
    # # Stides = context for each window for better inference (?)
    # output = pipe(file_path, chunk_length_s=10, stride_length_s=(4, 2))

    # ASR_transcription = re.sub(r'\s+', ' ', output['text'])
    # print(output)
    # print(ASR_transcription)