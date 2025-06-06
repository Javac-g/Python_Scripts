import librosa
import numpy as np
import soundfile as sf
from scipy.signal import butter, lfilter, fftconvolve
from librosa.effects import pitch_shift, time_stretch

# === Параметры ===
INPUT_AUDIO = "your_sound.mp3"
OUTPUT_AUDIO = "mutated_output.wav"
GRAIN_MS = 80                     # Длительность зерна
MODULATION_FREQ = 3              # Частота амплитудной модуляции (Гц)
MODULATION_DEPTH = 0.01          # Глубина амплитудной модуляции
NORMALIZE_LEVEL = 0.89           # Уровень нормализации

# === Загрузка аудио ===
print("Загружаем аудио...")
y, sr = librosa.load(INPUT_AUDIO, sr=None)
duration = librosa.get_duration(y=y, sr=sr)
grain_samples = int(GRAIN_MS * sr / 1000)

# === Granular synthesis с Pitch Shift и Time Stretch ===
print("Применяем granular synthesis...")
grains = [y[i:i + grain_samples] for i in range(0, len(y), grain_samples)]

processed = []
for i, g in enumerate(grains):
    if len(g) < grain_samples // 2:
        continue

    pitch_shift_amt = np.random.uniform(-1.0, 1.0)
    shifted = pitch_shift(y=g, sr=sr, n_steps=pitch_shift_amt)

    rate = np.random.uniform(0.85, 1.15)
    try:
        stretched = time_stretch(y=shifted, rate=rate)
    except:
        stretched = shifted  # Fallback

    processed.append(stretched)

print("Объединяем зерна...")
output = np.concatenate(processed)
output = output[:len(y)]

# === Амплитудная модуляция ===
print("Добавляем амплитудную модуляцию...")
t = np.linspace(0, duration, len(output))
modulation = 1 + MODULATION_DEPTH * np.sin(2 * np.pi * MODULATION_FREQ * t)
output *= modulation

# === Реверберация ===
def apply_reverb(signal, sr, decay=0.3, delay=0.015):
    delay_samples = int(delay * sr)
    impulse = np.zeros(delay_samples * 4)
    impulse[::delay_samples] = decay ** np.arange(4)
    return fftconvolve(signal, impulse, mode='full')[:len(signal)]

print("Добавляем реверберацию...")
output = apply_reverb(output, sr)

# === Случайная полосовая фильтрация ===
def butter_bandpass(lowcut, highcut, fs, order=4):
    nyq = 0.5 * fs
    low = max(lowcut / nyq, 0.001)
    high = min(highcut / nyq, 0.999)
    return butter(order, [low, high], btype='band')

def bandpass_filter(data, sr, lowcut, highcut):
    b, a = butter_bandpass(lowcut, highcut, sr)
    return lfilter(b, a, data)

low = np.random.uniform(100, 600)
high = np.random.uniform(3000, 8000)
print(f"Применяем фильтрацию: {int(low)}–{int(high)} Гц")
output = bandpass_filter(output, sr, low, high)

# === Нормализация ===
print("Нормализуем...")
output = np.clip(output, -1.0, 1.0)
output /= np.max(np.abs(output)) + 1e-6
output *= NORMALIZE_LEVEL

# === Сохранение ===
sf.write(OUTPUT_AUDIO, output, sr)
print(f"✅ Аудио сохранено как: {OUTPUT_AUDIO}")
