import rawpy
import imageio
import os
from PIL import Image
import magic
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed
import app.gui
import logging
import csv
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications import  EfficientNetB7, MobileNetV2, ResNet50, InceptionV3

# For MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import decode_predictions, preprocess_input

# For ResNet50
from tensorflow.keras.applications.resnet50 import decode_predictions, preprocess_input

# For EfficientNetB7
from tensorflow.keras.applications.efficientnet import decode_predictions, preprocess_input

# For InceptionV3
from tensorflow.keras.applications.inception_v3 import decode_predictions, preprocess_input
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

models = {
    'EfficientNetB7': EfficientNetB7(weights='imagenet'),
    'MobileNetV2': MobileNetV2(weights='imagenet'),
    'ResNet50': ResNet50(weights='imagenet'),
    'InceptionV3': InceptionV3(weights='imagenet')
}
def write_results_to_csv(csv_file_path, predictions, image_path):
    # Open the CSV file in append mode ('a')
    with open(csv_file_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write a row for each prediction
        for label, probability in predictions:
            writer.writerow([image_path, label, probability])

def get_photo_type_with_pillow(file_path):
    try:
        with Image.open(file_path) as img:
            return img.format
    except IOError:
        return "Not a valid image file or unsupported format"

def get_photo_type_with_magic(file_path):
    mime = magic.Magic(mime=True)
    return mime.from_file(file_path)

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

def predict_images(image_paths,log_callback):
    results = []
    for photo_path in image_paths:
        photo_results = {'image': photo_path}
        for model_name, model in models.items():
            if photo_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                img = image.load_img(photo_path, target_size=model.input_shape[1:3])
                img_array = image.img_to_array(img)
                img_array_expanded_dims = np.expand_dims(img_array, axis=0)
                processed_image = preprocess_input(img_array_expanded_dims)
                predictions = model.predict(processed_image)
                decoded_predictions = decode_predictions(predictions, top=3)[0]
                photo_results[model_name] = predictions[0][1]
                #logging.INFO(f"Prediction made with {model_name} for {photo_path}: {decoded_predictions}")
                if log_callback:
                    log_callback(f"Prediction made with {model_name} for {photo_path}: {decoded_predictions}")
#            except Exception as e:
#                logging.info(f"Error making prediction with {model_name} for {photo_path}: {e}")
#                if log_callback:
#                    log_callback(f"Error making prediction with {model_name} for {photo_path}: {e}")
        results.append(decoded_predictions)
    write_results_to_csv(app.gui.self.output_dir_path.get() + '/results.csv', results, image_paths)
    return results
def predict_image(model,photo_path):
    if photo_path.lower().endswith(('.png', '.jpg', '.jpeg')):
        img = image.load_img(photo_path, target_size=model.input_shape[1:3])
        img_array = image.img_to_array(img)
        img_array_expanded_dims = np.expand_dims(img_array, axis=0)
        processed_image = preprocess_input(img_array_expanded_dims)
        predictions = model.predict(processed_image)
        return decode_predictions(predictions, top=3)[0]
    return ([0,0])


def scan_directory_for_images(directory_path):
    # Extended list of supported image file extensions including common RAW formats
    supported_extensions = [
        '.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif',  # Standard formats
        '.cr2', '.nef', '.arw', '.dng'  # Common RAW formats
    ]
    image_paths = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith(tuple(supported_extensions)):
                full_path = os.path.join(root, file)
                image_paths.append(full_path)
    return image_paths

if __name__ == "__main__":
    # Example usage
    image_paths = scan_directory_for_images(app.gui.self.output_dir_path.get())
    predict_images(models, image_paths)
    #convert_raw_to_jpeg(directory_path, output_path)
