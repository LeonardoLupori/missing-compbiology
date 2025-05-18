import numpy as np
import matplotlib.pyplot as plt

def analog_to_digital(signal, bit_depth):
    """
    Convert an analog signal to digital based on the specified bit depth
    
    Args:
        signal: The original analog signal
        bit_depth: Number of bits to use for quantization
    
    Returns:
        Digitized signal with quantization based on bit depth
    """
    # Calculate number of quantization levels (2^bit_depth)
    levels = 2**bit_depth
    
    # Find min and max of signal to normalize
    signal_min = np.min(signal)
    signal_max = np.max(signal)
    
    # Normalize signal to range [0, 1]
    normalized = (signal - signal_min) / (signal_max - signal_min)
    
    # Quantize to specified bit depth
    quantized = np.round(normalized * (levels - 1)) / (levels - 1)
    
    # Scale back to original range
    digital_signal = quantized * (signal_max - signal_min) + signal_min
    
    return digital_signal

# Generate analog signal (a sine wave with some noise)
def generate_signal(num_samples=1000):
    t = np.linspace(0, 1, num_samples)
    # Create a composite signal with two frequencies and some noise
    signal = 0.5 * np.sin(2 * np.pi * 3 * t) + 0.3 * np.sin(2 * np.pi * 10 * t)
    # Add some noise
    noise = np.random.normal(0, 0.05, num_samples)
    return t, signal + noise

# Create figure to visualize bit depth effects
def visualize_bit_depth():
    # Generate our sample signal
    t, analog_signal = generate_signal()
    
    # Create a figure with subplots for different bit depths
    fig, axs = plt.subplots(4, 1, figsize=(10, 12), sharex=True)
    
    # List of bit depths to demonstrate
    bit_depths = [1, 2, 4, 8]
    
    # Plot original analog signal on all subplots with higher visibility
    for ax in axs:
        ax.plot(t, analog_signal, 'blue', linewidth=1, alpha=0.4, label='Analog')
    
    # Plot each digital representation with different bit depths
    for i, bits in enumerate(bit_depths):
        digital_signal = analog_to_digital(analog_signal, bits)
        
        # Calculate and display quantization error
        error = np.sqrt(np.mean((analog_signal - digital_signal)**2))
        
        # Plot digital signal
        axs[i].step(t, digital_signal, where='post', linewidth=1.5, 
                   label=f'{bits}-bit (Levels: {2**bits})')
        
        # Customize subplot
        axs[i].set_ylabel('Amplitude')
        axs[i].set_title(f'{bits}-bit Quantization ({2**bits} levels), RMSE: {error:.4f}')
        axs[i].legend(loc='upper right')
        axs[i].grid(True, alpha=0.3)
    
    # Add a zoomed inset for the 8-bit plot to show detail
    from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes, mark_inset
    
    # Create the zoomed inset
    zoom_ax = zoomed_inset_axes(axs[3], 4, loc='center right')
    zoom_ax.plot(t, analog_signal, 'blue', linewidth=1, alpha=0.4)
    zoom_ax.step(t, analog_to_digital(analog_signal, 8), where='post', linewidth=1.5)
    
    # Set the limits for the zoomed region
    zoom_region_start = 400
    zoom_region_end = 450
    y_min = min(analog_signal[zoom_region_start:zoom_region_end]) - 0.05
    y_max = max(analog_signal[zoom_region_start:zoom_region_end]) + 0.05
    
    zoom_ax.set_xlim(t[zoom_region_start], t[zoom_region_end])
    zoom_ax.set_ylim(y_min, y_max)
    zoom_ax.grid(True, alpha=0.3)
    
    # Add connecting lines to show the zoomed region
    mark_inset(axs[3], zoom_ax, loc1=1, loc2=3, fc="none", ec="0.5")
    
    # Final touches for the entire figure
    plt.xlabel('Time')
    fig.suptitle('Effect of Bit Depth on Analog-to-Digital Conversion', fontsize=16)
    plt.tight_layout()
    plt.subplots_adjust(top=0.94)
    
    plt.savefig('bit_depth_visualization.png', dpi=300)
    plt.show()

if __name__ == "__main__":
    visualize_bit_depth()