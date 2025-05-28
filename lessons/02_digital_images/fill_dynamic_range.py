import numpy as np
import matplotlib.pyplot as plt

# Generate time vector
sample_rate = 1000  # Hz
duration = 2.0  # seconds
time = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# Create a composite analog signal (sine wave + noise)
frequency_1 = 5  # Hz
frequency_2 = 12  # Hz
original_signal = (0.8 * np.sin(2 * np.pi * frequency_1 * time) + 
                  0.3 * np.sin(2 * np.pi * frequency_2 * time) + 
                  0.1 * np.random.normal(0, 1, len(time)))

# Define amplification levels
amplification_levels = [0.5, 1.0, 2.0, 4.0]
amplification_labels = ['0.5x (Under-amplified)', '1.0x (Original)', 
                       '2.0x (Well-amplified)', '4.0x (Over-amplified)']

# ADC parameters
adc_bits = 8  # 8-bit ADC
adc_levels = 2**adc_bits
adc_max_voltage = 5.0  # Full scale voltage
adc_min_voltage = 0.0

# Create the plot
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
# fig.suptitle('Analog Signal Amplification and Dynamic Range Utilization', 
#              fontsize=16, fontweight='bold')

# Colors for different amplification levels
colors = ['blue', 'green', 'orange', 'red']

for i, (amp_level, label, color) in enumerate(zip(amplification_levels, 
                                                 amplification_labels, colors)):
    row = i // 2
    col = i % 2
    ax = axes[row, col]
    
    # Amplify the signal
    amplified_signal = original_signal * amp_level
    
    # Offset signal to fit within ADC range (0 to 5V)
    signal_offset = amplified_signal + adc_max_voltage/2
    
    # Clip signal to ADC range
    clipped_signal = np.clip(signal_offset, adc_min_voltage, adc_max_voltage)
    
    # Quantize the signal (simulate ADC conversion)
    quantized_signal = np.round(clipped_signal / adc_max_voltage * (adc_levels - 1))
    digital_signal = quantized_signal * adc_max_voltage / (adc_levels - 1)
    
    # # Plot analog signal (before ADC) - smooth continuous line
    # ax.plot(time[:500], amplified_signal[:500], color=color, linewidth=2, 
    #         alpha=0.8, label='Analog (continuous)', linestyle='-')
    
    # Plot digitized signal - thick stepped line with markers
    ax.step(time[:500], digital_signal[:500], color=color, linewidth=2.5, 
            where='post', alpha=0.9, label='Digital (quantized)', linestyle='-')
    
    # Add quantization levels as horizontal grid lines
    # quantization_levels = np.linspace(adc_min_voltage, adc_max_voltage, adc_levels)
    # for level in quantization_levels[::16]:  # Show every 16th level to avoid clutter
    #     ax.axhline(y=level, color='gray', linestyle=':', alpha=0.4, linewidth=0.5)
    
    # Add ADC range indicators
    ax.axhline(y=adc_max_voltage, color='red', linestyle='--', alpha=0.7, linewidth=2)
    ax.axhline(y=adc_min_voltage, color='red', linestyle='--', alpha=0.7, linewidth=2)
    ax.fill_between(time[:500], adc_min_voltage, adc_max_voltage, 
                   alpha=0.08, color='lightblue', label='ADC Range')
    
    # Calculate dynamic range utilization
    signal_range = np.max(clipped_signal) - np.min(clipped_signal)
    utilization = (signal_range / adc_max_voltage) * 100
    
    # Calculate number of quantization levels used
    unique_levels = len(np.unique(quantized_signal))
    
    ax.set_title(f'{label}\nRange Utilization: {utilization:.1f}%\n'
                f'Levels Used: {unique_levels}/{adc_levels}', fontsize=11)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Voltage (V)')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper right', fontsize=8)
    ax.set_ylim(-0.5, 5.5)
    ax.set_xlim(0, 0.5)

plt.tight_layout()
plt.subplots_adjust(top=0.93, bottom=0.12)
plt.show()
