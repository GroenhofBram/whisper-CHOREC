import numpy as np
import matplotlib.pyplot as plt
import librosa

def main():
    wavFile = "D:\\repos\\wav2vec-CHOREC\\files\\test_glob\\S01\\S01C001M1\\S01C001M1_1LG.wav"
    y,sr = librosa.load(wavFile, sr=16000)
    noiseIntensity, signalIntensity, snr, sortedIntensityList, plot = computeSNR(y, sr, 0.25)
    print(snr)


# This function returns the intensity of the audio signal.
def getIntensity(s):
    return 10*np.log10(sum(s*s)/(len(s)*4*10**(-10)))


def computeSNR(signal, samplingrate, windowsize):
    intensityList = []
    for begin in np.arange(0, len(signal), samplingrate*windowsize):
        sample = signal[int(begin):int(begin + samplingrate*windowsize)]
        intensity = getIntensity(sample)
        intensityList.append(intensity)

    sortedIntensityList = sorted(intensityList)
    plot = plt.plot(sortedIntensityList)

    noiseIntensity = sortedIntensityList[int(len(intensityList)*0.05)]
    signalIntensity = sortedIntensityList[int(len(intensityList)*0.95)]
    snr = round(signalIntensity - noiseIntensity, 4)

    return noiseIntensity, signalIntensity, snr, sortedIntensityList, plot


def calculate_snr(wav_file_path: str) -> float:
    print(f"Calculating SNR for: ==== {wav_file_path}")
    sample_rate = 16000
    y,sr = librosa.load(wav_file_path, sr=sample_rate)
    _noiseIntensity, _signalIntensity, snr, _sortedIntensityList, _plot = computeSNR(y, sr, 0.25)
    return snr