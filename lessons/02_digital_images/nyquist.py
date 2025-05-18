import numpy as np
import matplotlib.pyplot as plt

# Create figure with subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
fig.suptitle('Nyquist Theorem & Aliasing', fontsize=16, fontweight='bold')

# Time arrays
t_dense = np.linspace(0, 1, 1000)  # Dense time points for original signals

# Original signals (continuous)
freq_original_1 = 5  # Hz - well below Nyquist for our sampling
signal_1 = np.sin(2 * np.pi * freq_original_1 * t_dense)

freq_original_2 = 12  # Hz - above Nyquist for our sampling
signal_2 = np.sin(2 * np.pi * freq_original_2 * t_dense)

# Sampling rate and sampled points
fs = 10  # Hz - sampling frequency
t_sampled = np.arange(0, 1, 1/fs)  # Sampled time points

# Sampled signals
signal_1_sampled = np.sin(2 * np.pi * freq_original_1 * t_sampled)
signal_2_sampled = np.sin(2 * np.pi * freq_original_2 * t_sampled)

# Reconstructed signals (from samples)
# For signal 1 (properly sampled), reconstruction matches original
# For signal 2 (undersampled), reconstruction shows aliasing

# For signal 2, aliased frequency = |fs - (freq_original_2 % fs)| = |10 - (12 % 10)| = |10 - 2| = 8
aliased_freq = abs(fs - (freq_original_2 % fs))
signal_2_aliased = np.sin(2 * np.pi * aliased_freq * t_dense)

# Plot signal 1 (properly sampled)
ax1.plot(t_dense, signal_1, 'b-', linewidth=1.5, label=f'Original Signal ({freq_original_1} Hz)')
ax1.plot(t_sampled, signal_1_sampled, 'ro', markersize=8, label=f'Samples (fs = {fs} Hz)')
ax1.axhline(y=0, color='k', linestyle='-', alpha=0.2)

# Add Nyquist frequency indication
ax1.axvline(x=0.5, color='g', linestyle='--', alpha=0.7)
ax1.text(0.51, 1.1, f'Nyquist Rate = {fs/2} Hz', color='g', fontsize=10)

ax1.set_title(f'Proper Sampling: Signal Frequency ({freq_original_1} Hz) < Nyquist Frequency ({fs/2} Hz)')
ax1.set_ylim(-1.5, 1.5)
ax1.set_xlim(0, 1)
ax1.legend(loc='upper right')
ax1.set_ylabel('Amplitude')

# Plot signal 2 (undersampled - aliasing)
ax2.plot(t_dense, signal_2, 'b-', linewidth=1.5, label=f'Original Signal ({freq_original_2} Hz)')
ax2.plot(t_sampled, signal_2_sampled, 'ro', markersize=8, label=f'Samples (fs = {fs} Hz)')
ax2.plot(t_dense, signal_2_aliased, 'g--', linewidth=2, 
         label=f'Apparent Signal ({aliased_freq} Hz)')
ax2.axhline(y=0, color='k', linestyle='-', alpha=0.2)

# Add Nyquist frequency indication
ax2.axvline(x=0.5, color='g', linestyle='--', alpha=0.7)
ax2.text(0.51, 1.1, f'Nyquist Rate = {fs/2} Hz', color='g', fontsize=10)

ax2.set_title(f'Aliasing: Signal Frequency ({freq_original_2} Hz) > Nyquist Frequency ({fs/2} Hz)')
ax2.set_ylim(-1.5, 1.5)
ax2.set_xlim(0, 1)
ax2.legend(loc='upper right')
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Amplitude')

# Add explanatory text
fig.text(0.5, 0.01, 
         "Nyquist Theorem: To accurately sample a signal, sample rate must be ≥ 2× the highest frequency\n"
         "Aliasing: When undersampling, high frequencies appear as lower frequencies, creating false signals", 
         ha='center', fontsize=11, bbox=dict(facecolor='white', alpha=0.7))

plt.tight_layout()
plt.subplots_adjust(bottom=0.15)
plt.show()