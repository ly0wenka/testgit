#include <windows.h>
#include <mmsystem.h>
#include <stdio.h>

#pragma comment(lib, "winmm.lib")

#define SECONDS_TO_WRITE 5
#define BUFFER_SIZE 44100*SECONDS_TO_WRITE
#define WAV_FILE_NAME "record.wav"

WAVEHDR header;
HWAVEIN hWaveIn;
short buffer[BUFFER_SIZE];

// Function to save WAV file
void saveWavFile(const char *filename, short *data, int dataSize, int sampleRate) {
    FILE *file = fopen(filename, "wb");

    if (!file) {
        printf("Error opening file for writing.\n");
        return;
    }

    // WAV file header
    int subchunk1Size = 16;
    short audioFormat = 1;
    short numChannels = 1;
    short bitsPerSample = 16;
    int byteRate = sampleRate * numChannels * bitsPerSample / 8;
    short blockAlign = numChannels * bitsPerSample / 8;
    int subchunk2Size = dataSize * sizeof(short);
    int chunkSize = 4 + (8 + subchunk1Size) + (8 + subchunk2Size);

    // Write RIFF header
    fwrite("RIFF", 1, 4, file);
    fwrite(&chunkSize, 4, 1, file);
    fwrite("WAVE", 1, 4, file);

    // fmt chunk
    fwrite("fmt ", 1, 4, file);
    fwrite(&subchunk1Size, 4, 1, file);
    fwrite(&audioFormat, 2, 1, file);
    fwrite(&numChannels, 2, 1, file);
    fwrite(&sampleRate, 4, 1, file);
    fwrite(&byteRate, 4, 1, file);
    fwrite(&blockAlign, 2, 1, file);
    fwrite(&bitsPerSample, 2, 1, file);

    // data chunk
    fwrite("data", 1, 4, file);
    fwrite(&subchunk2Size, 4, 1, file);
    fwrite(data, sizeof(short), dataSize, file);

    fclose(file);
    printf("Audio saved to file: %s\n", filename);
}

int main() {
    SetConsoleCP(1251);           // Set input code page to Windows-1251
    SetConsoleOutputCP(1251);     // Set output code page to Windows-1251

    WAVEFORMATEX format;
    format.wFormatTag = WAVE_FORMAT_PCM;
    format.nChannels = 1;
    format.nSamplesPerSec = 44100;
    format.wBitsPerSample = 16;
    format.nBlockAlign = format.nChannels * format.wBitsPerSample / 8;
    format.nAvgBytesPerSec = format.nSamplesPerSec * format.nBlockAlign;
    format.cbSize = 0;

    if (waveInOpen(&hWaveIn, WAVE_MAPPER, &format, 0L, 0L, CALLBACK_NULL) != MMSYSERR_NOERROR) {
        printf("Error opening microphone\n");
        return 1;
    }

    header.lpData = (LPSTR)buffer;
    header.dwBufferLength = sizeof(buffer);
    header.dwFlags = 0L;
    header.dwLoops = 0L;
    waveInPrepareHeader(hWaveIn, &header, sizeof(WAVEHDR));
    waveInAddBuffer(hWaveIn, &header, sizeof(WAVEHDR));
    waveInStart(hWaveIn);

    printf("Recording in progress... (5 seconds)\n");
    Sleep(SECONDS_TO_WRITE*1000);

    waveInStop(hWaveIn);
    waveInUnprepareHeader(hWaveIn, &header, sizeof(WAVEHDR));
    waveInClose(hWaveIn);

    printf("Recording finished. Saving to file...\n");

    // Save the recording
    saveWavFile(WAV_FILE_NAME, buffer, BUFFER_SIZE, 44100);

    return 0;
}
