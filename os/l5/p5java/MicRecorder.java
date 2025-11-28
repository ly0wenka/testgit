import javax.sound.sampled.*;
import java.io.*;

public class MicRecorder {

static final String OUTPUT_FILE = "record.wav";
static final int SECONDS_TO_RECORD = 5;
static final float SAMPLE_RATE = 44100;
static final int SAMPLE_SIZE_BITS = 16;
static final int CHANNELS = 1;

public static void main(String[] args) {
    AudioFormat format = new AudioFormat(
            SAMPLE_RATE,
            SAMPLE_SIZE_BITS,
            CHANNELS,
            true,  // signed
            false  // little endian
    );

    DataLine.Info info = new DataLine.Info(TargetDataLine.class, format);
    if (!AudioSystem.isLineSupported(info)) {
        System.out.println("Line not supported");
        return;
    }

    try (TargetDataLine line = (TargetDataLine) AudioSystem.getLine(info)) {
        line.open(format);
        line.start();

        System.out.println("Recording in progress... (" + SECONDS_TO_RECORD + " seconds)");

        ByteArrayOutputStream out = new ByteArrayOutputStream();
        byte[] buffer = new byte[4096];
        int bytesRead;
        long endTime = System.currentTimeMillis() + SECONDS_TO_RECORD * 1000;

        while (System.currentTimeMillis() < endTime) {
            bytesRead = line.read(buffer, 0, buffer.length);
            out.write(buffer, 0, bytesRead);
        }

        byte[] audioData = out.toByteArray();

        // Save WAV file
        try (ByteArrayInputStream bais = new ByteArrayInputStream(audioData);
             AudioInputStream ais = new AudioInputStream(bais, format, audioData.length / format.getFrameSize())) {

            AudioSystem.write(ais, AudioFileFormat.Type.WAVE, new File(OUTPUT_FILE));
        }

        line.stop();
        System.out.println("Recording finished. Saved to: " + OUTPUT_FILE);

    } catch (LineUnavailableException | IOException ex) {
        ex.printStackTrace();
    }
}

}
