import os
import queue
import sounddevice as sd
import vosk
import sys
import json

# ตั้งค่าโมเดล
model_path = "vosk-model-small-en-us-0.15"
if not os.path.exists(model_path):
    print(f"Please download the model from https://alphacephei.com/vosk/models and unpack as '{model_path}' in the current folder.")
    sys.exit(1)

model = vosk.Model(model_path)
samplerate = 16000  # ค่าความถี่ของเสียง

q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

# เริ่มการบันทึกเสียงและประมวลผลคำพูด
with sd.RawInputStream(samplerate=samplerate, blocksize=8000, dtype='int16',
                       channels=1, callback=callback):
    print('#' * 80)
    print('Start speaking now, press Ctrl+C to stop the recording.')
    print('#' * 80)

    rec = vosk.KaldiRecognizer(model, samplerate)
    while True:
        data = q.get()
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            print(result['text'])
        else:
            print(rec.PartialResult())