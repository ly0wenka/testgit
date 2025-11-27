using System;
using NAudio.Wave;

namespace Lr5
{
    class Program
    {
        static WaveInEvent waveIn;
        static WaveFileWriter writer;
        static string outputFilePath = "mic_record.wav";

        static void Main(string[] args)
        {
            Console.WriteLine("Натисніть Enter, щоб почати запис...");
            Console.ReadLine();

            waveIn = new WaveInEvent();
            waveIn.WaveFormat = new WaveFormat(44100, 1); // 44.1kHz, моно

            writer = new WaveFileWriter(outputFilePath, waveIn.WaveFormat);

            waveIn.DataAvailable += (s, a) =>
            {
                writer.Write(a.Buffer, 0, a.BytesRecorded);
            };

            waveIn.RecordingStopped += (s, a) =>
            {
                writer.Dispose();
                waveIn.Dispose();
                Console.WriteLine("Запис завершено. Файл збережено як: " + outputFilePath);
            };

            waveIn.StartRecording();

            Console.WriteLine("Запис йде... Натисніть Enter, щоб зупинити.");
            Console.ReadLine();

            waveIn.StopRecording();
        }
    }
}
