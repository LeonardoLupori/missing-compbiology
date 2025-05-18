import numpy as np
import matplotlib.pyplot as plt

def analog_to_digital_with_saturation(signal, bit_depth, input_range):
    """
    Convert an analog signal to digital with saturation effects
    
    Args:
        signal: The original analog signal
        bit_depth: Number of bits to use for quantization
        input_range: Tuple of (min, max) representing ADC input range
    
    Returns:
        Tuple of (digital signal, saturated mask)
    """
    # Calculate number of quantization levels
    levels = 2**bit_depth
    
    # Get input range limits
    min_range, max_range = input_range
    
    # Clip signal to the ADC input range (this is the saturation)
    saturated_signal = np.clip(signal, min_range, max_range)
    
    # Create a mask to identify where saturation occurred
    saturation_mask = (signal < min_range) | (signal > max_range)
    
    # Normalize to [0, 1] for quantization
    normalized = (saturated_signal - min_range) / (max_range - min_range)
    
    # Quantize to specified bit depth
    quantized = np.round(normalized * (levels - 1)) / (levels - 1)
    
    # Scale back to original range
    digital_signal = quantized * (max_range - min_range) + min_range
    
    return digital_signal, saturation_mask

def generate_base_signal(num_samples=1000):
    """Generate a base signal with constant amplitude"""
    t = np.linspace(0, 1, num_samples)
    
    # Base frequency
    freq = 5
    
    # Create a sinusoidal signal with some harmonics for interest
    signal = np.sin(2 * np.pi * freq * t) + 0.3 * np.sin(2 * np.pi * freq * 3 * t)
    
    return t, signal

def visualize_saturation():
    # Generate our base signal
    t, base_signal = generate_base_signal()
    
    # Set up the figure
    fig, axs = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
    
    # ADC parameters - keeping this constant across all plots
    bit_depth = 8
    input_range = (-1.0, 1.0)  # Fixed ADC input range
    
    # Different amplification factors to demonstrate saturation
    amplifications = [
        0.5,    # Low amplification - no saturation
        1.2,    # Medium amplification - moderate saturation
        2.0     # High amplification - severe saturation
    ]
    
    amp_labels = ["Low Amplification (0.5×)", "Medium Amplification (1.2×)", "High Amplification (2.0×)"]
    
    # Loop through each amplification and plot
    for i, (amp_factor, label) in enumerate(zip(amplifications, amp_labels)):
        # Amplify the base signal
        analog_signal = base_signal * amp_factor
        
        # Perform analog to digital conversion with potential saturation
        digital_signal, saturation_mask = analog_to_digital_with_saturation(
            analog_signal, bit_depth, input_range)
        
        # Plot the original analog signal
        axs[i].plot(t, analog_signal, 'blue', alpha=0.4, label='Analog Signal')
        
        # Plot the digital signal (potentially saturated)
        axs[i].step(t, digital_signal, 'green', where='post', 
                   label=f'Digital Signal ({bit_depth}-bit)')
        
        # Highlight saturated regions
        if np.any(saturation_mask):
            # Calculate percentage of samples that are saturated
            saturation_percent = np.sum(saturation_mask) / len(saturation_mask) * 100
            saturation_text = f"Saturation: {saturation_percent:.1f}% of samples"
        else:
            saturation_text = "No Saturation"
        
        # Draw the ADC input range as horizontal lines
        min_range, max_range = input_range
        axs[i].axhline(y=min_range, color='r', linestyle='--', alpha=0.5)
        axs[i].axhline(y=max_range, color='r', linestyle='--', alpha=0.5)
        
        # Fill the area outside the ADC range with light red
        axs[i].fill_between(t, min_range, np.minimum(analog_signal, min_range), 
                          color='red', alpha=0.2)
        axs[i].fill_between(t, max_range, np.maximum(analog_signal, max_range), 
                          color='red', alpha=0.2)
        
        # Customize subplot
        axs[i].set_ylabel('Amplitude')
        axs[i].set_title(f'{label}: {saturation_text}')
        axs[i].legend(loc='upper right')
        axs[i].grid(True, alpha=0.3)
        
        # Set y-limits with some padding to keep scale consistent across plots
        axs[i].set_ylim(-2.5, 2.5)
        
        # Add text annotations for ADC range limits
        axs[i].text(0.02, min_range + 0.1, f'ADC Min: {min_range}', 
                  backgroundcolor='white', alpha=0.7)
        axs[i].text(0.02, max_range - 0.1, f'ADC Max: {max_range}', 
                  backgroundcolor='white', alpha=0.7)
    
    # Remove the arrow annotation about increasing amplitude

    
    # Final touches for the entire figure
    plt.xlabel('Time')
    fig.suptitle('Signal Amplification and ADC Saturation', 
                fontsize=16, y=0.98)
    plt.tight_layout()
    plt.subplots_adjust(top=0.92, bottom=0.08)
    
    plt.savefig('saturation_visualization.png', dpi=300)
    plt.show()

if __name__ == "__main__":
    visualize_saturation()
