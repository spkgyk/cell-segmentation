import matplotlib.pyplot as plt
from openslide import OpenSlide
from cellpose import models
from tqdm.auto import tqdm
from typing import List
import numpy as np


def extract_patches(wsi_path: str, patch_size: int, level: int, num_patches: int) -> List[np.ndarray]:
    """
    Extracts random patches from a whole-slide image.

    Args:
        wsi_path (str): Path to the whole-slide image file.
        patch_size (int): Size of the patches to extract.
        level (int): Magnification level at which to extract the patches.
        num_patches (int): Number of patches to extract.

    Returns:
        List[np.ndarray]: List of extracted patches as NumPy arrays.
    """
    slide = OpenSlide(wsi_path)
    dimensions = slide.level_dimensions[level]

    patches = []
    step_size = int(patch_size * 1.1)  # Ensure non-overlapping patches with some buffer
    x_steps = dimensions[0] // step_size
    y_steps = dimensions[1] // step_size

    selected_positions = []
    while len(patches) < num_patches:
        x = np.random.randint(0, x_steps) * step_size
        y = np.random.randint(0, y_steps) * step_size
        if (x, y) not in selected_positions:
            patch = slide.read_region((x, y), level, (patch_size, patch_size))
            selected_positions.append((x, y))
            if np.array(patch).mean() < 220:  # Skip white background
                patches.append(np.array(patch))
    return patches


def cell_segmentation(patches: List[np.ndarray], batch_size: int = 10) -> List[np.ndarray]:
    """
    Performs cell segmentation on a list of patches.

    Args:
        patches (List[np.ndarray]): List of patches as NumPy arrays.
        batch_size (int): Number of patches to process in a single batch.

    Returns:
        List[np.ndarray]: List of segmented patches as NumPy arrays.
    """
    model = models.Cellpose(gpu=True, model_type="cyto3")
    segmented_patches = []

    # Perform segmentation for each color channel
    pbar = tqdm(range(4))
    masks_grey, flows, styles, diams = model.eval(patches, diameter=None, channels=[0, 0], batch_size=batch_size)
    pbar.update(1)
    masks_red, flows, styles, diams = model.eval(patches, diameter=None, channels=[1, 0], batch_size=batch_size)
    pbar.update(1)
    masks_green, flows, styles, diams = model.eval(patches, diameter=None, channels=[2, 0], batch_size=batch_size)
    pbar.update(1)
    masks_blue, flows, styles, diams = model.eval(patches, diameter=None, channels=[3, 1], batch_size=batch_size)
    pbar.update(1)

    # Split patches into batches
    for j in range(len(patches)):
        segmented_patches.append((masks_grey[j], masks_red[j], masks_green[j], masks_blue[j]))

    return segmented_patches


def visualize_segmentation(patches: List[np.ndarray], segmented_patches: List[np.ndarray]) -> None:
    """
    Visualizes the original and segmented patches side by side.

    Args:
        patches (List[np.ndarray]): List of original patches as NumPy arrays.
        segmented_patches (List[np.ndarray]): List of segmented patches as NumPy arrays.
    """
    for patch, seg in zip(patches, segmented_patches):
        fig, ax = plt.subplots(2, 3, figsize=(18, 8))

        # Display original patch
        ax[0, 0].imshow(patch)
        ax[0, 0].set_title("Original Patch")

        # Display segmented patches
        ax[0, 1].imshow(patch)
        ax[0, 1].imshow(seg[0], alpha=0.55, cmap="jet")
        ax[0, 1].set_title("Segmented Patch (Grey, cyto3)")

        ax[0, 2].imshow(patch)
        ax[0, 2].imshow(seg[1], alpha=0.55, cmap="jet")
        ax[0, 2].set_title("Segmented Patch (Red, cyto3)")

        ax[1, 1].imshow(patch)
        ax[1, 1].imshow(seg[2], alpha=0.55, cmap="jet")
        ax[1, 1].set_title("Segmented Patch (Green, cyto3)")

        ax[1, 2].imshow(patch)
        ax[1, 2].imshow(seg[3], alpha=0.55, cmap="jet")
        ax[1, 2].set_title("Segmented Patch (Blue, cyto3)")

        # Make ax[1, 0] blank
        ax[1, 0].axis("off")

        plt.show()
