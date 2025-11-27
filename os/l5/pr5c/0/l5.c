#include <windows.h>
#include <mmsystem.h>
#include <stdio.h>

#pragma comment(lib, "winmm.lib")

#define BUFFER_SIZE 44100

WAVEHDR header;
HWAVEIN hWaveIn;
short buffer[BUFFER_SIZE];

int main() {
    WAVEFORMATEX format;
    format.wFormatTag = WAVE_FORMAT_PCM;
    format.nChannels = 1;
    format.nSamplesPerSec = 44100;
    format.wBitsPerSample = 16;
    format.nBlockAlign = format.nChannels * format.wBitsPerSample / 8;
    format.nAvgBytesPerSec = format.nSamplesPerSec * format.nBlockAlign;
    format.cbSize = 0;

    if (waveInOpen(&hWaveIn, WAVE_MAPPER, &format, 0L, 0L, CALLBACK_NULL) != MMSYSERR_NOERROR) {
        printf("Помилка відкриття мікрофону\n");
        return 1;
    }

    header.lpData = (LPSTR)buffer;
    header.dwBufferLength = sizeof(buffer);
    header.dwFlags = 0L;
    header.dwLoops = 0L;
    waveInPrepareHeader(hWaveIn, &header, sizeof(WAVEHDR));
    waveInAddBuffer(hWaveIn, &header, sizeof(WAVEHDR));
    waveInStart(hWaveIn);

    printf("Запис триває... (5 сек)\n");
    Sleep(5000);

    waveInStop(hWaveIn);
    waveInUnprepareHeader(hWaveIn, &header, sizeof(WAVEHDR));
    waveInClose(hWaveIn);

    printf("Запис завершено. Дані у буфері.\n");

    return 0;
}
