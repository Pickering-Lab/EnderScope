# Import packages
import os
import cv2
import numpy as np
from tifffile import imwrite, imread

# Function to load images from a folder with a specified file extension (e.g., ".bmp")
def load_images_from_folder(folder_path):
    images = []
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith(".bmp"):
            img_path = os.path.join(folder_path, filename)
            image = cv2.imread(img_path)
            images.append(image)
    return images

# Function to segment plastics on a filter paper by detecting background pixels
def detect_plastic(image):
    threshold = [100, 100, 100] # Threshold for the background - any pixel which is above this value on all channels is background
    
    mask = np.all(image >= threshold, axis=-1) # background is any pixel greater than threshold
    
    num_black_pixels = np.count_nonzero(mask == 0) # count the number of "False" or non-background pixels
    
    return num_black_pixels, mask

# Function to overlay a mask on an RGB image for visualization
def overlay_mask_on_rgb_image(image, mask):
    plastic = mask == 0  # Invert the mask to identify non-background pixel
    result_image = image.copy()
    result_image[plastic] = [255, 0, 0]  # Set detected pixels to red
    return result_image

folder_path = r'file/path/' # replace with the directory where your images are saved
images_bf = load_images_from_folder(folder_path)  # Load in Bright field images

# Parameters
image_width_mm = 6.7  # Width of each image
image_height_mm = 5.0  # Height of each image
overlap_x_mm = 0.5  # Overlap in the x direction
overlap_y_mm = 0.5  # Overlap in the y direction

# Convert mm to pixels based on the specified pixel dimensions
pixels_per_mm_x = 1014 / image_width_mm
pixels_per_mm_y = 760 / image_height_mm
overlap_x_pixels = int(overlap_x_mm * pixels_per_mm_x)
overlap_y_pixels = int(overlap_y_mm * pixels_per_mm_y)

# Define the image size in pixels based on the specified dimensions
image_width_pixels = int(image_width_mm * pixels_per_mm_x)
image_height_pixels = int(image_height_mm * pixels_per_mm_y)

# Set up a variable to save detections to
plastic_px = 0

# Optional: Create the "bin_masks" directory
#bin_masks_directory = os.path.join(folder_path, 'bin_masks')
#os.makedirs(bin_masks_directory, exist_ok=True)

# Create the "overlay" directory
#overlay_directory = os.path.join(folder_path, 'overlay_images') 
#os.makedirs(overlay_directory, exist_ok=True)

# For each image, we crop the overlap regions between frames, threshold the plastic particles from the background and count the pixels of plastic
for idx, image in enumerate(images_bf):  
    
    image = image[:image_height_pixels - overlap_y_pixels, :image_width_pixels - overlap_x_pixels, :] # crop the image to remove overlap region
    num_plastic_pixels, mask = detect_plastic(image) # Segment plastics from the background
    plastic_px += num_plastic_pixels # add to tally
    #overlay = overlay_mask_on_rgb_image(image, mask) # Optional: Save an image of detections overlayed on image
    
    # Optional: Save Masks as separate images and overlayed on original image
    #imwrite(os.path.join(bin_masks_directory, f'{idx + 1}.tif'), mask)
    #imwrite(os.path.join(overlay_directory, f'{idx + 1}.tif'), overlay)

print('Processing all images is complete')

# Convert pixels to mm
one_px_area = np.square((1/px_to_mm))
plastic_mm = plastic_px * one_px_area

print(f'Total area of detected plastics is {plastic_px} pixels, or {plastic_mm} mm sq.' ) 
