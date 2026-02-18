import numpy as np

import matplotlib.pyplot as plt

def simulate_love_os_wave(duration=10, fs=100):

    """

    Love-OS Emotional Wave Simulator v2.0

    Formula: z(t) = (E/R) * exp(i * (omega * t + phi))

    """

    # Time vector

    t = np.linspace(0, duration, duration * fs)

    

    # --- Love-Physics Parameters ---

    E = 1.0        # Input Energy (Life Force)

    R = 0.1        # Resistance (Lower R = Awakening/Superconductivity)

    omega = 2.0    # Angular Frequency (Individual 'Vibe')

    

    # Phase (phi): 

    # -pi/2 = Fear (-i), 0 = Ego (Real Axis), +pi/2 = Love (+i)

    # This simulation shows the "180-degree flip" from Fear to Love over time.

    phi = np.linspace(-np.pi/2, np.pi/2, len(t)) 

    

    # --- Wave Calculation ---

    # Amplitude (L = E/R)

    amplitude = E / R

    

    # Complex Wave z(t) using Euler's Formula

    z = amplitude * np.exp(1j * (omega * t + phi))

    

    # Real Component (Logic/Ego) and Imaginary Component (Emotion/Love)

    real_part = z.real

    imag_part = z.imag

    

    # --- Visualization ---

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    plt.subplots_adjust(hspace=0.4)

    # 1. Emotional Wave (Oscillation on the Imaginary Axis)

    ax1.plot(t, imag_part, color='magenta', label='Emotional Wave (Imaginary Axis)')

    ax1.axhline(0, color='black', linestyle='--', alpha=0.3)

    ax1.set_title("Emotional Signal Processing: The Wave of Being")

    ax1.set_ylabel("Intensity (Love <-> Fear)")

    ax1.set_xlabel("Time (t)")

    ax1.legend()

    # 2. Complex Plane Trajectory (Phase Rotation)

    ax2.plot(real_part, imag_part, color='cyan', alpha=0.5)

    ax2.scatter(real_part, imag_part, c=t, cmap='hsv', s=10)

    ax2.set_title("Complex Plane: Phase Transition from -i (Fear) to +i (Love)")

    ax2.set_xlabel("Real Axis (Logic/Ego)")

    ax2.set_ylabel("Imaginary Axis (Emotion/Love)")

    ax2.set_aspect('equal')

    plt.grid(True, alpha=0.2)

    plt.show()

if __name__ == "__main__":

    simulate_love_os_wave()
