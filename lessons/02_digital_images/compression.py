import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
from skimage.measure import block_reduce

# Set random seed for reproducibility
np.random.seed(42)

def create_test_image(size=(64, 64)):
    """Create a test image with various features"""
    img = np.zeros(size)
    
    # Add geometric shapes
    x, y = np.meshgrid(np.linspace(-1, 1, size[1]), np.linspace(-1, 1, size[0]))
    
    # Circle
    circle = ((x-0.3)**2 + (y-0.3)**2) < 0.15**2
    img[circle] = 200
    
    # Rectangle
    rect = (np.abs(x+0.3) < 0.2) & (np.abs(y+0.3) < 0.15)
    img[rect] = 150
    
    # Gradient background
    gradient = 50 + 30 * (x + y)
    img = np.maximum(img, gradient)
    
    # Add some texture/noise
    texture = np.random.normal(0, 10, size)
    img = img + texture
    
    return np.clip(img, 0, 255).astype(np.uint8)

def simulate_jpeg_compression(img, quality_factor):
    """Simulate JPEG-like compression effects"""
    if quality_factor >= 95:
        return img  # No compression
    
    # Simulate block-based compression artifacts
    block_size = max(1, int(8 / (quality_factor / 20)))
    
    # Downsample and upsample to simulate compression
    compressed = block_reduce(img, (block_size, block_size), np.mean)
    compressed = np.repeat(np.repeat(compressed, block_size, axis=0), block_size, axis=1)
    
    # Crop to original size if needed
    compressed = compressed[:img.shape[0], :img.shape[1]]
    
    # Add quantization noise based on quality
    noise_level = (100 - quality_factor) / 10
    noise = np.random.normal(0, noise_level, img.shape)
    compressed = compressed + noise
    
    # Apply slight blur for lower quality
    if quality_factor < 70:
        sigma = (70 - quality_factor) / 30
        compressed = gaussian_filter(compressed, sigma=sigma)
    
    return np.clip(compressed, 0, 255).astype(np.uint8)

def simulate_tiff_lzw_compression(img):
    """Simulate TIFF LZW lossless compression"""
    # LZW is lossless, so image quality remains the same
    # Only file size changes based on image complexity
    return img.copy()

def calculate_compression_ratio(img, compression_type, quality=100):
    """Calculate realistic compression ratios for different formats"""
    base_pixels = img.size
    
    if compression_type == 'RAW':
        # RAW: typically 12-16 bits per pixel, uncompressed
        return 1.0  # No compression
    elif compression_type == 'JPEG_HIGH':
        # JPEG high quality: 10-20:1 compression ratio
        return 0.08  # ~12:1 ratio
    elif compression_type == 'JPEG_LOW':
        # JPEG low quality: 20-50:1 compression ratio
        return 0.03  # ~33:1 ratio
    elif compression_type == 'TIFF_LZW':
        # TIFF LZW: lossless, 2-4:1 typical compression for natural images
        return 0.35  # ~3:1 ratio
    return 1.0

# Create original test image
original_img = create_test_image()

# Different compression types and levels
compression_types = ['RAW', 'JPEG_HIGH', 'JPEG_LOW', 'TIFF_LZW']
compression_labels = ['RAW\n(Uncompressed)', 'JPEG High\n(85% Quality)', 
                     'JPEG Low\n(30% Quality)', 'TIFF LZW\n(Lossless)']
compression_qualities = [100, 85, 30, 100]  # Quality factors for simulation

# Generate compressed versions
compressed_images = []
for quality in compression_qualities:
    if quality == 100:
        compressed_images.append(original_img)
    else:
        compressed_images.append(simulate_jpeg_compression(original_img, quality))

# Create the visualization
fig, axes = plt.subplots(2, 4, figsize=(16, 8))
fig.suptitle('Digital Image Compression: RAW vs JPEG vs TIFF LZW Comparison', 
             fontsize=14, fontweight='bold', y=0.95)

# Colors for different compression levels
colors = ['green', 'blue', 'orange', 'red']

for i, (img, comp_type, quality, label, color) in enumerate(zip(compressed_images, compression_types, 
                                                                compression_qualities, compression_labels, colors)):
    # Image subplot (top row)
    img_ax = axes[0, i]
    img_ax.imshow(img, cmap='gray', vmin=0, vmax=255)
    img_ax.set_title(label, fontsize=11, pad=10)
    img_ax.set_xticks([])
    img_ax.set_yticks([])
    
    # Calculate compression metrics
    compression_ratio = calculate_compression_ratio(img, comp_type, quality)
    relative_size = compression_ratio * 100
    
    # Calculate quality metrics (compared to original)
    if comp_type in ['RAW', 'TIFF_LZW']:
        mse = 0
        psnr = float('inf')
        quality_loss = 0
    else:
        mse = np.mean((original_img.astype(float) - img.astype(float))**2)
        if mse == 0:
            psnr = float('inf')
            quality_loss = 0
        else:
            psnr = 20 * np.log10(255.0 / np.sqrt(mse))
            quality_loss = (100 - quality) if comp_type.startswith('JPEG') else 0
    
    # Add compression info on images
    if comp_type == 'RAW':
        info_text = f'Size: 100%\nLossless\nNo Artifacts'
    elif comp_type == 'TIFF_LZW':
        info_text = f'Size: {relative_size:.0f}%\nLossless\nNo Artifacts'
    else:
        if psnr == float('inf'):
            info_text = f'Size: {relative_size:.0f}%\nPSNR: ∞ dB'
        else:
            info_text = f'Size: {relative_size:.0f}%\nPSNR: {psnr:.1f} dB'
    
    img_ax.text(0.02, 0.98, info_text, 
                transform=img_ax.transAxes, verticalalignment='top',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8),
                fontsize=9)
    
    # Quality vs Size plot (bottom row)
    bar_ax = axes[1, i]
    
    # Create bar chart showing size and quality trade-off
    categories = ['File Size\n(%)', 'Quality\n(PSNR)']
    
    # Normalize PSNR for visualization (cap at 50 dB for scaling)
    psnr_norm = min(psnr, 50) if psnr != float('inf') else 50
    values = [relative_size, psnr_norm * 2]  # Scale PSNR for better visualization
    
    bars = bar_ax.bar(categories, values, color=[color, 'lightgray'], alpha=0.7, 
                     edgecolor='black', linewidth=1)
    
    # Add value labels on bars
    bar_ax.text(0, relative_size + 2, f'{relative_size:.0f}%', 
               ha='center', va='bottom', fontweight='bold')
    
    if psnr == float('inf'):
        bar_ax.text(1, psnr_norm * 2 + 2, '∞ dB', 
                   ha='center', va='bottom', fontweight='bold')
    else:
        bar_ax.text(1, psnr_norm * 2 + 2, f'{psnr:.1f} dB', 
                   ha='center', va='bottom', fontweight='bold')
    
    bar_ax.set_ylim(0, 120)
    bar_ax.set_ylabel('Relative Value', fontsize=10)
    bar_ax.grid(True, alpha=0.3, axis='y')
    # bar_ax.set_title(f'Compression: {100-quality}%', fontsize=10)
    
    # # Add compression artifacts indicator
    # if quality < 100:
    #     artifact_level = (100 - quality) / 100
    #     bar_ax.axhspan(0, artifact_level * 120, alpha=0.1, color='red', 
    #                   label='Artifacts' if i == 1 else "")

plt.tight_layout()
plt.subplots_adjust(top=0.88, bottom=0.12, left=0.06, right=0.94)
plt.show()
