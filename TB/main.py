import cv2
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from scipy.ndimage import gaussian_filter

xray_path = '1.png'
mask_path = '2.tif'

xray_image = cv2.imread(xray_path, cv2.IMREAD_GRAYSCALE)
if xray_image is None:
    raise FileNotFoundError(f"Failed to load X-ray image. Check the path: {xray_path}")

mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
if mask is None:
    raise FileNotFoundError(f"Failed to load TB mask. Check the path: {mask_path}")

h, w = xray_image.shape

# Resize the mask to match the X-ray image dimensions
if mask.shape != xray_image.shape:
    print(f"Resizing mask from {mask.shape} to {xray_image.shape}")
    mask = cv2.resize(mask, (xray_image.shape[1], xray_image.shape[0]))

# Smooth the mask for more natural radial profiles
smoothed_mask = gaussian_filter(mask.astype(float), sigma=10)

# Step 1: Display 2D overlay with TB label
def show_2d_overlay(xray, mask):
    """
    Displays a 2D overlay of the X-ray image with the TB mask.
    """
    plt.figure(figsize=(8, 10))
    plt.imshow(xray, cmap='gray')
    plt.imshow(mask, cmap='Reds', alpha=0.5)  # Overlay the mask in red
    plt.title("X-ray with TB Mask Highlighted")
    plt.axis("off")
    plt.show()

# Show the 2D overlay
show_2d_overlay(xray_image, mask)

# Step 2: Enhance the radius profile by amplifying the mask influence
radius_profile = (np.mean(smoothed_mask, axis=1) / 255.0 * (w // 2)) + 20  # Add base radius
radius_profile = gaussian_filter(radius_profile, sigma=5)  # Smooth the profile

# Create 3D revolution (volume from radius profile)
theta = np.linspace(0, 2 * np.pi, 200)
z = np.arange(h)
theta_grid, z_grid = np.meshgrid(theta, z)
radius_grid = np.tile(radius_profile[:, np.newaxis], (1, len(theta)))

# Convert to Cartesian coordinates
x = radius_grid * np.cos(theta_grid)
y = radius_grid * np.sin(theta_grid)

# Grayscale intensity from X-ray image (average over rows)
intensity_gray = np.mean(xray_image, axis=1) / 255.0
intensity_gray = np.tile(intensity_gray[:, np.newaxis], (1, len(theta)))

# Red color mask: highlight TB mask area
mask_binary = mask > 127
red_overlay = np.mean(mask_binary, axis=1)
red_overlay = np.tile(red_overlay[:, np.newaxis], (1, len(theta)))

# Adjust the color mapping for realism
r = np.clip(intensity_gray + red_overlay * 1.5, 0, 1)  # Amplify red for TB areas
g = intensity_gray * (1 - red_overlay)
b = intensity_gray * (1 - red_overlay)

# Combine into RGB string format for plotly
colors = np.stack([r, g, b], axis=-1)
colors_rgb = (colors * 255).astype(np.uint8)
colors_hex = ['rgb({},{},{})'.format(r_, g_, b_) for r_, g_, b_ in colors_rgb.reshape(-1, 3)]
colors_hex = np.reshape(colors_hex, x.shape)

# Debugging: Print shapes of arrays
print(f"x shape: {x.shape}, y shape: {y.shape}, z shape: {z_grid.shape}")
print(f"surfacecolor shape: {np.mean(colors[..., :3], axis=-1).shape}")

# Step 3: Plot with Plotly
fig = go.Figure(data=[
    go.Surface(
        x=x, y=y, z=z_grid,
        surfacecolor=np.mean(colors[..., :3], axis=-1),  # Use grayscale intensity
        colorscale=[[0, 'gray'], [1, 'red']],  # Gray for healthy, red for TB
        showscale=True,  # Show color scale for better interpretation
        hoverinfo='skip',
        opacity=0.9  # Add slight transparency for realism
    ),
    # Add a scatter3d trace for the annotation
    go.Scatter3d(
        x=[0], y=[0], z=[h // 2],  # Position of the annotation
        mode='markers+text',
        marker=dict(size=5, color='red'),
        text=["TB Lesion Highlighted"],  # Annotation text
        textposition='top center'
    )
])

# Update layout with lighting and background
fig.update_layout(
    title='3D Revolved X-ray with TB Lesion Highlight',
    scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Height',
        aspectmode='data',
        xaxis=dict(showbackground=True, backgroundcolor="rgb(230, 230, 230)"),
        yaxis=dict(showbackground=True, backgroundcolor="rgb(230, 230, 230)"),
        zaxis=dict(showbackground=True, backgroundcolor="rgb(230, 230, 230)"),
    ),
    scene_camera=dict(eye=dict(x=1.3, y=1.3, z=1.3)),
    margin=dict(l=0, r=0, b=0, t=40)
)

# Show the 3D plot
fig.show()
