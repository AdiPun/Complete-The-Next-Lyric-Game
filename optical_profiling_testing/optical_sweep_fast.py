# optical_sweep_fast.py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time

def run_sweep_fast(csv_path):
    wavelengths = pd.read_csv(csv_path, header=None).values.flatten()
    time.sleep(2)  # simulate total sweep delay instead of per-step
    powers = np.sin(wavelengths / 10) + np.random.normal(0, 0.05, len(wavelengths))
    return wavelengths, powers

def analyze_fast(powers):
    kernel = np.ones(3) / 3
    smooth = np.convolve(powers, kernel, mode='same')
    return np.mean(powers), smooth

def plot_results(wavelengths, powers, smooth):
    plt.plot(wavelengths, powers, label="Raw")
    plt.plot(wavelengths, smooth, label="Smoothed")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    w, p = run_sweep_fast("wavelengths.csv")
    avg, s = analyze_fast(p)
    print(f"Average Power: {avg:.3f}")
    plot_results(w, p, s)
