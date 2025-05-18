import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Create figure and axis
fig, ax = plt.subplots(figsize=(10, 5))

# Time axis
t = np.linspace(0, 6, 1000)
ax.set_xlim(0, 6)
ax.set_ylim(0, 3)

# Exposure time as square wave
exposure_wave = np.zeros_like(t)
for i in range(6):
    exposure_wave[(t >= i+0) & (t < i+0.75)] = 1


# Plot exposure wave
ax.plot(t, exposure_wave*0.8 + 0.5, 'b-', linewidth=2.5, label='Exposure Time (1/60s)')

# Frame periods (sampling rate) as boxes
y_frames = 2
for i in range(6):
    frame = Rectangle((i, y_frames-0.25), 1, 0.5, 
                     edgecolor='black', facecolor='none', linewidth=1.5)
    ax.add_patch(frame)

# Add vertical lines at frame boundaries
for i in range(7):
    ax.axvline(x=i, color='gray', linestyle=':', alpha=0.5)

# Labels
ax.text(-0.3, y_frames, 'Sampling Rate\n(30 fps)', fontsize=11, va='center')
ax.text(-0.3, 0.9, 'Exposure Time\n(1/60s)', fontsize=11, va='center')

# Axis formatting
ax.set_xlabel('Time (s)', fontsize=12)
ax.set_xticks(np.arange(0, 7))
ax.set_xticklabels([f"{i}/30" for i in range(7)])
ax.set_yticks([])

# Title
ax.set_title('Sampling Rate vs. Exposure Time', fontsize=14, fontweight='bold')

# Remove unnecessary spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)

plt.tight_layout()
plt.show()