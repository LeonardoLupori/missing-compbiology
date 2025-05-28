import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Set random seed for reproducibility
np.random.seed(42)

# Create different types of synthetic images
def create_dark_image(size=(100, 100)):
    """Create a dark image with low pixel values"""
    base = np.random.normal(50, 20, size)
    return np.clip(base, 0, 255).astype(np.uint8)

def create_bright_image(size=(100, 100)):
    """Create a bright image with high pixel values"""
    base = np.random.normal(200, 30, size)
    return np.clip(base, 0, 255).astype(np.uint8)

def create_low_contrast_image(size=(100, 100)):
    """Create a low contrast image with narrow range"""
    base = np.random.normal(128, 25, size)
    return np.clip(base, 0, 255).astype(np.uint8)

def create_high_contrast_image(size=(100, 100)):
    """Create a high contrast image with wide range"""
    # Create regions of different intensities
    img = np.zeros(size)
    img[:50, :50] = np.random.normal(50, 15, (50, 50))  # Dark region
    img[:50, 50:] = np.random.normal(200, 15, (50, 50))  # Bright region
    img[50:, :50] = np.random.normal(80, 20, (50, 50))   # Mid-dark region
    img[50:, 50:] = np.random.normal(170, 20, (50, 50))  # Mid-bright region
    return np.clip(img, 0, 255).astype(np.uint8)

# Generate the four different image types
images = [
    create_dark_image(),
    create_bright_image(), 
    create_low_contrast_image(),
    create_high_contrast_image()
]

image_labels = [
    'Dark Image\n(Underexposed)',
    'Bright Image\n(Overexposed)', 
    'Low Contrast\n(Narrow Range)',
    'High Contrast\n(Wide Range)'
]

# Create the visualization
fig, axes = plt.subplots(2, 4, figsize=(16, 8))
fig.suptitle('Image Histogram Analysis: Understanding Pixel Intensity Distribution', 
             fontsize=14, fontweight='bold', y=0.95)

# Colors for histograms
colors = ['darkblue', 'orange', 'green', 'red']

for i, (img, label, color) in enumerate(zip(images, image_labels, colors)):
    # Image subplot (top row)
    img_ax = axes[0, i]
    img_ax.imshow(img, cmap='gray', vmin=0, vmax=255)
    img_ax.set_title(label, fontsize=11, pad=10)
    img_ax.set_xticks([])
    img_ax.set_yticks([])
    
    # Add intensity value annotations on images
    mean_val = np.mean(img)
    std_val = np.std(img)
    img_ax.text(0.02, 0.98, f'Mean: {mean_val:.0f}\nStd: {std_val:.0f}', 
                transform=img_ax.transAxes, verticalalignment='top',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8),
                fontsize=9)
    
    # Histogram subplot (bottom row)
    hist_ax = axes[1, i]
    
    # Calculate histogram
    hist_values, bin_edges = np.histogram(img.flatten(), bins=50, range=(0, 255))
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    
    # Plot histogram with filled area
    hist_ax.fill_between(bin_centers, hist_values, alpha=0.7, color=color)
    hist_ax.plot(bin_centers, hist_values, color=color, linewidth=2)
    
    # Add vertical lines for key statistics
    mean_val = np.mean(img)
    hist_ax.axvline(mean_val, color='red', linestyle='--', linewidth=2, 
                   alpha=0.8)
    
    # Set histogram properties
    hist_ax.set_xlim(0, 255)
    hist_ax.set_xlabel('Pixel Intensity (0-255)', fontsize=10)
    hist_ax.set_ylabel('Pixel Count', fontsize=10)
    hist_ax.grid(True, alpha=0.3)
    
    # Add range information
    min_val = np.min(img)
    max_val = np.max(img)
    dynamic_range = max_val - min_val
    

plt.tight_layout()
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.06, right=0.94)
plt.show()