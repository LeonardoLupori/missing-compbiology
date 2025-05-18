import numpy as np
import matplotlib.pyplot as plt

# Parameters
fs = 1000              # Sampling frequency (Hz)
t = np.arange(0, 1, 1/fs)  # Time vector (1 second)
f1 = 5                 # Frequency of signal (Hz)

# Create analog signal (continuous sine wave)
analog_signal = np.sin(2 * np.pi * f1 * t)

# Create digital signal (sampled version with lower sampling rate)
fs_low = 80            # Low sampling rate (Hz)
t_digital = np.arange(0, 1 + 1/fs_low, 1/fs_low)
digital_signal = np.sin(2 * np.pi * f1 * t_digital)

# Create figure
plt.figure(figsize=(10, 6))

# Plot analog signal
plt.subplot(2, 1, 1)
plt.plot(t, analog_signal, 'b-', linewidth=1.5)
plt.title('Analog Signal')
plt.ylabel('Amplitude')
plt.grid(True)
plt.xlim(0, 1)
plt.ylim(-1.2, 1.2)

# Plot digital signal
plt.subplot(2, 1, 2)
plt.stem(t_digital, digital_signal, 'r', markerfmt='ro', basefmt=' ', use_line_collection=True)
plt.plot(t, analog_signal, 'b--', linewidth=0.5)
plt.title('Digital Signal (Sampled)')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.grid(True)
plt.xlim(0, 1)
plt.ylim(-1.2, 1.2)
plt.legend(['Original analog signal', 'Samples'])

# Add overall title
plt.suptitle('Comparison of Analog and Digital Signals', fontsize=14)

# Adjust layout
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# Add annotation explaining the difference
plt.figtext(0.5, 0.01, 
           'The analog signal is continuous in time, while the digital signal consists of discrete samples taken at specific time intervals.',
           ha='center', fontsize=10, bbox={'facecolor':'white', 'alpha':0.5, 'pad':5})

plt.show()