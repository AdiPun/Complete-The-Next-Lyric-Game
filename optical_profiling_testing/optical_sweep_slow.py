# optical_sweep_slow.py
import csv
import numpy as np
import matplotlib.pyplot as plt
import time

def load_wavelengths():
    # Pretend we load laser wavelengths from a CSV
    with open("wavelengths.csv", "r") as f:
        reader = csv.reader(f)
        return [float(row[0]) for row in reader]

def measure_power(wavelength):
    # Fake optical measurement
    time.sleep(0.001)  # simulate instrument delay
    power = np.sin(wavelength / 10) + np.random.normal(0, 0.05)
    return power

def run_sweep():
    wavelengths = load_wavelengths()
    powers = []
    for w in wavelengths:
        power = measure_power(w)
        powers.append(power)
    return wavelengths, powers

def analyze_data(wavelengths, powers):
    # Inefficient calculation using Python loops
    avg_power = sum(powers) / len(powers)
    smooth = []
    for i in range(len(powers)):
        # simple smoothing (inefficient)
        left = powers[i - 1] if i > 0 else powers[i]
        right = powers[i + 1] if i < len(powers) - 1 else powers[i]
        smooth.append((left + powers[i] + right) / 3)
    return avg_power, smooth

def plot_results(wavelengths, powers, smooth):
    plt.plot(wavelengths, powers, label="Raw")
    plt.plot(wavelengths, smooth, label="Smoothed")
    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Power (a.u.)")
    plt.legend()
    plt.show()

def main():
    wavelengths, powers = run_sweep()
    avg, smooth = analyze_data(wavelengths, powers)
    print(f"Average Power: {avg:.3f}")
    plot_results(wavelengths, powers, smooth)

if __name__ == "__main__":
    main()
