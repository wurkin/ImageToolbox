import rawpy
import imageio
import os

def convert_raw_to_jpeg(raw_image_path, output_path):
    """
    Converts a RAW image to JPEG format.
    
    Parameters:
    - raw_image_path: The path to the RAW image file.
    - output_path: The directory where the converted JPEG will be saved.
    """
    try:
        # Use rawpy to open and process the RAW image
        with rawpy.imread(raw_image_path) as raw:
            rgb = raw.postprocess()
        
        # Define the output file name
        base_name = os.path.splitext(os.path.basename(raw_image_path))[0]
        jpeg_path = os.path.join(output_path, f"{base_name}.jpg")
        
        # Use imageio to save the processed image as JPEG
        imageio.imsave(jpeg_path, rgb)
        
        print(f"Converted {raw_image_path} to {jpeg_path}")
    except Exception as e:
        print(f"Error converting {raw_image_path}: {e}")

def batch_convert_raw_to_jpeg(directory_path, output_path):
    """
    Converts all RAW images in a directory to JPEG format.
    
    Parameters:
    - directory_path: The directory containing RAW images.
    - output_path: The directory where the converted JPEG images will be saved.
    """
    # Ensure the output directory exists
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    # Iterate over all files in the directory
    for filename in os.listdir(directory_path):
        if filename.lower().endswith(('.raw', '.cr2', '.nef', '.arw', '.dng')):
            raw_image_path = os.path.join(directory_path, filename)
            convert_raw_to_jpeg(raw_image_path, output_path)

if __name__ == "__main__":
    # Example usage
    directory_path = 'path/to/raw/images'
    output_path = 'path/to/save/jpeg'
    batch_convert_raw_to_jpeg(directory_path, output_path)
