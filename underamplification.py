import numpy as np
import matplotlib.pyplot as plt

def analog_to_digital_with_quantization(signal, bit_depth, input_range):
    """
    Convert an analog signal to digital with quantization visualization
    
    Args:
        signal: The original analog signal
        bit_depth: Number of bits to use for quantization
        input_range: Tuple of (min, max) representing ADC input range
    
    Returns:
        Tuple of (digital signal, utilized levels, total levels)
    """
    # Calculate number of quantization levels
    total_levels = 2**bit_depth
    
    # Get input range limits
    min_range, max_range = input_range
    
    # Clip signal to the ADC input range (saturation/clipping)
    saturated_signal = np.clip(signal, min_range, max_range)
    
    # Normalize to [0, 1] for quantization
    normalized = (saturated_signal - min_range) / (max_range - min_range)
    
    # Calculate the raw quantization levels (before rounding)
    raw_levels = normalized * (total_levels - 1)
    
    # Quantize to specified bit depth
    quantized_levels = np.round(raw_levels)
    quantized = quantized_levels / (total_levels - 1)
    
    # Calculate how many unique levels are actually used
    utilized_levels = len(np.unique(quantized_levels))
    
    # Scale back to original range
    digital_signal = quantized * (max_range - min_range) + min_range
    
    return digital_signal, utilized_levels, total_levels

def generate_base_signal(num_samples=1000):
    """Generate a moderate-amplitude base signal"""
    t = np.linspace(0, 1, num_samples)
    
    # Base frequency
    freq = 5
    
    # Create a sinusoidal signal with some harmonics for interest
    signal = np.sin(2 * np.pi * freq * t) + 0.3 * np.sin(2 * np.pi * freq * 3 * t)
    
    return t, signal

def visualize_under_amplification():
    # Generate our base signal
    t, base_signal = generate_base_signal()
    
    # Set up the figure
    fig, axs = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
    
    # ADC parameters - keeping this constant across all plots
    bit_depth = 8  # 8-bit ADC = 256 possible levels
    input_range = (-1.0, 1.0)  # Fixed ADC input range
    
    # Different amplification factors to demonstrate under-utilization
    amplifications = [
        0.05,   # Very low amplification - poor utilization
        0.2,    # Low amplification - moderate utilization
        0.8     # Good amplification - better utilization
    ]
    
    amp_labels = ["Very Low Amplification (0.05×)", 
                  "Low Amplification (0.2×)", 
                  "Good Amplification (0.8×)"]
    
    # Loop through each amplification and plot
    for i, (amp_factor, label) in enumerate(zip(amplifications, amp_labels)):
        # Amplify (or in this case, attenuate) the base signal
        analog_signal = base_signal * amp_factor
        
        # Perform analog to digital conversion with quantization info
        digital_signal, utilized_levels, total_levels = analog_to_digital_with_quantization(
            analog_signal, bit_depth, input_range)
        
        # Calculate percentage of ADC range utilized
        signal_min, signal_max = np.min(analog_signal), np.max(analog_signal)
        range_min, range_max = input_range
        range_utilization = (signal_max - signal_min) / (range_max - range_min) * 100
        
        # Calculate effective bit depth (based on levels actually used)
        effective_bits = np.log2(utilized_levels) if utilized_levels > 0 else 0
        lost_resolution = bit_depth - effective_bits
        
        # Plot the original analog signal
        axs[i].plot(t, analog_signal, 'blue', alpha=0.4, label='Analog Signal')
        
        # Plot the digital signal
        axs[i].step(t, digital_signal, 'green', where='post', 
                   linewidth=1.2, label=f'Digital Signal ({bit_depth}-bit ADC)')
        
        # Plot the ADC input range
        min_range, max_range = input_range
        axs[i].axhline(y=min_range, color='r', linestyle='--', alpha=0.5)
        axs[i].axhline(y=max_range, color='r', linestyle='--', alpha=0.5)
        
        # Shade the utilized portion of the ADC range
        axs[i].axhspan(signal_min, signal_max, color='green', alpha=0.1, 
                      label=f'Utilized Range: {range_utilization:.1f}%')
        
        # Draw some quantization levels to show resolution
        if amp_factor <= 0.2:  # Only for the low amplification cases
            # Calculate the step size
            step_size = (max_range - min_range) / (total_levels - 1)
            
            # Draw a small section of quantization levels to demonstrate resolution
            num_levels_to_show = 10
            level_start = total_levels // 2 - num_levels_to_show // 2
            
            for level in range(level_start, level_start + num_levels_to_show):
                level_value = min_range + level * step_size
                if signal_min <= level_value <= signal_max:  # Only show levels in signal range
                    axs[i].axhline(y=level_value, color='gray', linestyle='-', 
                                 alpha=0.3, linewidth=0.5)
        
        # Customize subplot
        axs[i].set_ylabel('Amplitude')
        title_text = (f"{label}\n"
                     f"Utilized Levels: {utilized_levels}/{total_levels} "
                     f"({utilized_levels/total_levels*100:.1f}% of ADC range)\n"
                     f"Effective Resolution: {effective_bits:.1f} bits "
                     f"(Lost: {lost_resolution:.1f} bits)")
        axs[i].set_title(title_text)
        axs[i].legend(loc='upper right')
        axs[i].grid(True, alpha=0.3)
        
        # Set y-limits to show full ADC range
        axs[i].set_ylim(-1.2, 1.2)
        
        # Add text annotations for ADC range limits
        axs[i].text(0.02, min_range + 0.1, f'ADC Min: {min_range}', 
                  backgroundcolor='white', alpha=0.7)
        axs[i].text(0.02, max_range - 0.1, f'ADC Max: {max_range}', 
                  backgroundcolor='white', alpha=0.7)
        
        # Add zoom inset for the very low amplitude case to see quantization clearly
        if i == 0:  # Only for the first subplot
            from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes, mark_inset
            
            # Create the zoomed inset
            zoom_ax = zoomed_inset_axes(axs[i], 6, loc='center right', bbox_to_anchor=(0.98, 0.5), bbox_transform=axs[i].transAxes)
            zoom_ax.plot(t[400:450], analog_signal[400:450], 'blue', alpha=0.4)
            zoom_ax.step(t[400:450], digital_signal[400:450], 'green', where='post', linewidth=1.5)
            
            # Show the quantization levels in the zoomed region
            for level in range(level_start, level_start + num_levels_to_show):
                level_value = min_range + level * step_size
                if signal_min <= level_value <= signal_max:
                    zoom_ax.axhline(y=level_value, color='gray', linestyle='-', 
                                  alpha=0.3, linewidth=0.5)
            
            # Set the limits for the zoomed region
            y_center = np.mean(analog_signal[400:450])
            y_range = 0.1
            zoom_ax.set_xlim(t[400], t[450])
            zoom_ax.set_ylim(y_center - y_range/2, y_center + y_range/2)
            zoom_ax.grid(True, alpha=0.3)
            
            # Add connecting lines to show the zoomed region
            mark_inset(axs[i], zoom_ax, loc1=2, loc2=4, fc="none", ec="0.5")
    
    
    # Final touches for the entire figure
    plt.xlabel('Time')
    # fig.suptitle('Under-Amplification and Poor ADC Range Utilization', 
                # fontsize=16, y=0.98)
    plt.tight_layout()
    plt.subplots_adjust(top=0.92, bottom=0.08)
    
    # plt.savefig('under_amplification_visualization.png', dpi=300)
    plt.show()

if __name__ == "__main__":
    visualize_under_amplification()
