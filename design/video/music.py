"""Original background music for the Setting video (no samples, no licensing).
Light, upbeat and gentle: D major, 100 BPM, I-V-vi-IV.
Usage: python3 music.py out.wav [seconds]
"""
import sys, wave
import numpy as np

SR = 44100
BPM = 100
BEAT = 60 / BPM
BAR = 4 * BEAT
DUR = float(sys.argv[2]) if len(sys.argv) > 2 else 30.0
N = int(SR * (DUR + 3))
L = np.zeros(N); R = np.zeros(N)
rng = np.random.default_rng(7)

def hz(m): return 440.0 * 2 ** ((m - 69) / 12)

def add(sig, t, gain=1.0, pan=0.0):
    i = int(t * SR)
    if i >= N: return
    sig = sig[: N - i] * gain
    L[i:i + len(sig)] += sig * np.sqrt(0.5 * (1 - pan))
    R[i:i + len(sig)] += sig * np.sqrt(0.5 * (1 + pan))

def env(n, a=0.005, d=0.6):
    t = np.arange(n) / SR
    e = np.exp(-t / d)
    na = max(1, int(a * SR)); e[:na] *= np.linspace(0, 1, na)
    return e

def epiano(m, length=1.6, vel=1.0):
    n = int(length * SR); t = np.arange(n) / SR; f = hz(m)
    s = (np.sin(2*np.pi*f*t) + 0.35*np.sin(2*np.pi*2*f*t)*np.exp(-t/0.25)
         + 0.12*np.sin(2*np.pi*3*f*t)*np.exp(-t/0.12)
         + 0.25*np.sin(2*np.pi*f*t + 1.2*np.sin(2*np.pi*f*t))*np.exp(-t/0.3))
    s *= 1 + 0.08*np.sin(2*np.pi*4.5*t)  # soft tremolo
    return s * env(n, 0.004, 0.9) * vel

def marimba(m, vel=1.0):
    n = int(0.9 * SR); t = np.arange(n) / SR; f = hz(m)
    s = np.sin(2*np.pi*f*t) + 0.25*np.sin(2*np.pi*4*f*t)*np.exp(-t/0.05)
    return s * env(n, 0.002, 0.32) * vel

def pluck(m, vel=1.0, length=0.7):
    # Karplus-Strong
    f = hz(m); p = int(SR / f); n = int(length * SR)
    buf = rng.uniform(-1, 1, p); out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % p]
        buf[i % p] = 0.5 * (buf[i % p] + buf[(i + 1) % p]) * 0.996
    return out * vel * env(n, 0.001, 0.5)

def bass(m, length):
    n = int(length * SR); t = np.arange(n) / SR; f = hz(m)
    s = np.sin(2*np.pi*f*t) + 0.2*np.sin(2*np.pi*2*f*t)
    e = np.minimum(1, t / 0.02) * np.exp(-t / 0.9)
    return s * e

def pad(ms, length):
    n = int(length * SR); t = np.arange(n) / SR; s = np.zeros(n)
    for m in ms:
        for det in (-0.08, 0.0, 0.08):
            s += np.sin(2*np.pi*hz(m + det)*t)
    e = np.minimum(1, t / 0.5) * np.minimum(1, (length - t) / 0.5)
    return s / (3 * len(ms)) * e

def kick():
    n = int(0.35 * SR); t = np.arange(n) / SR
    f = 50 + 70 * np.exp(-t / 0.03)
    return np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-t / 0.12)

def shaker(vel=1.0):
    n = int(0.08 * SR); x = rng.normal(0, 1, n)
    x = np.diff(np.concatenate([[0], x]))  # crude high-pass
    return x * np.exp(-np.arange(n) / SR / 0.018) * vel

def snap():
    n = int(0.15 * SR); t = np.arange(n) / SR
    x = rng.normal(0, 1, n); x = np.diff(np.concatenate([[0], x]))
    return (x * 0.6 + np.sin(2*np.pi*1800*t)*0.3) * np.exp(-t / 0.035)

# D major: D=62, A=57/69, B=59, G=55
CHORDS = [  # (bass root, chord voicing)
    (38, [62, 66, 69, 74]),   # D
    (45, [61, 64, 69, 73]),   # A
    (47, [62, 66, 71, 74]),   # Bm
    (43, [62, 67, 71, 74]),   # G
]
MELODY = [  # (beat offset within 2 bars, midi, length factor) – pentatonic, gentle
    (0, 78, 1), (1, 76, 1), (1.5, 74, 1), (2.5, 76, 1), (4, 81, 1), (5, 78, 1), (6, 76, 1), (6.5, 74, 1),
]
MELODY2 = [(0, 74, 1), (0.5, 76, 1), (1, 78, 1), (2.5, 81, 1), (3, 78, 1), (4, 76, 1), (5.5, 74, 1), (6, 71, 1), (7, 74, 1)]

bars = int(np.ceil(DUR / BAR)) + 1
for b in range(bars):
    t0 = b * BAR
    root, ch = CHORDS[b % 4] if b < bars - 1 else CHORDS[0]
    # pad throughout
    add(pad([n - 12 for n in ch[:3]], BAR + 0.4), t0, 0.08)
    # e-piano: beat 1 and syncopated "and of 2", plus beat 4
    for off, v in ((0, 0.9), (1.5, 0.6), (3, 0.5)):
        for k, n in enumerate(ch):
            add(epiano(n, 1.4, v), t0 + off*BEAT + k*0.006, 0.09, pan=-0.25 + 0.15*k)
    # bass from bar 1
    if b >= 1:
        add(bass(root, BEAT*1.4), t0, 0.19)
        add(bass(root, BEAT*0.9), t0 + 2.5*BEAT, 0.14)
        add(bass(root + 7, BEAT*0.9), t0 + 3.5*BEAT, 0.10)
    # pluck arpeggio 8ths from bar 2
    if b >= 2:
        arp = [ch[0], ch[2], ch[1] + 12, ch[2], ch[3], ch[2], ch[1] + 12, ch[2]]
        for i, n in enumerate(arp):
            add(pluck(n + 12, 0.8 if i % 2 else 1.0), t0 + i*BEAT/2, 0.07, pan=0.35)
    # melody (marimba) in 2-bar phrases from bar 4
    if b >= 4 and b % 2 == 0:
        mel = MELODY if (b // 2) % 2 == 0 else MELODY2
        for off, n, _ in mel:
            add(marimba(n, 1.0), t0 + off*BEAT, 0.16, pan=-0.1)
    # percussion
    if b >= 2:
        for i in range(8):
            add(shaker(1.0 if i % 2 else 0.55), t0 + i*BEAT/2, 0.05, pan=0.4)
    if b >= 4:
        add(kick(), t0, 0.32); add(kick(), t0 + 2*BEAT, 0.27); add(kick(), t0 + 2.5*BEAT, 0.14)
        add(snap(), t0 + BEAT, 0.12, pan=-0.2); add(snap(), t0 + 3*BEAT, 0.12, pan=-0.2)

# reverb (FFT convolution with decaying noise)
def reverb(x, seed):
    r = np.random.default_rng(seed)
    n = int(1.8 * SR); t = np.arange(n) / SR
    ir = r.normal(0, 1, n) * np.exp(-t / 0.45); ir[:int(0.012*SR)] = 0; ir /= np.sqrt(np.sum(ir**2))
    m = len(x) + n; size = 1 << int(np.ceil(np.log2(m)))
    y = np.fft.irfft(np.fft.rfft(x, size) * np.fft.rfft(ir, size), size)[:len(x)]
    return y
L2 = L + 0.22 * reverb(L, 1); R2 = R + 0.22 * reverb(R, 2)

n = int(DUR * SR); out = np.stack([L2[:n], R2[:n]], axis=1)
fade_in = int(0.15 * SR); fade_out = int(2.8 * SR)
out[:fade_in] *= np.linspace(0, 1, fade_in)[:, None]
out[-fade_out:] *= (np.linspace(1, 0, fade_out) ** 1.6)[:, None]
out = np.tanh(out * 1.6) / 1.6
out *= 0.89 / np.max(np.abs(out))
pcm = (out * 32767).astype(np.int16)
with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('wrote', sys.argv[1], DUR, 's')
