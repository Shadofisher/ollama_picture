import base64
from io import BytesIO
from PIL import Image
import argparse
import os

def image_to_base64(image_path):
    # Open the image file
    with Image.open(image_path) as image:
        # Create a BytesIO object to hold the image data
        buffered = BytesIO()
        # Save the image in buffer as PNG format
        image.save(buffered, format="PNG")
        # Get the byte data of the image
        img_byte = buffered.getvalue()
        # Convert the byte data to a base64 string
        img_base64 = base64.b64encode(img_byte).decode("utf-8")
    
    return img_base64

def save_base64_to_curl_file(base64_str, original_image_path):
    # Construct the cURL command
    curl_command = (
        "curl --location 'http://localhost:11434/api/chat' "
        "--header 'Content-Type: application/json' "
        "--data '{"
        "  \"model\": \"llava\","
        "  \"messages\": ["
        "    {"
        "      \"role\": \"user\","
        "      \"content\": \"Is there a person in the image?\","
        f"     \"images\":[ \"{base64_str}\"]"
        "    }"
        "  ],"
        " \"stream\": false"
        "}'"
    )

    # Make the output file path based on the original image path
    output_file_path = original_image_path + "_curl_command.txt"
    # Write the cURL command to the file
    with open(output_file_path, 'w') as outfile:
        outfile.write(curl_command)
    
    print(f"cURL command saved to: {output_file_path}")

def main(image_path):
    try:
        base64_str = image_to_base64(image_path)
        print(f"Base64 string generated for: {image_path}")
        save_base64_to_curl_file(base64_str, image_path)
    except Exception as e:
        print(f"Failed to convert image: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert an image to Base64 and generate a cURL command.")
    parser.add_argument('image_file', type=str, help='Path to the image file.')

    args = parser.parse_args()
    if not os.path.isfile(args.image_file):
        print("The provided image file path does not exist.")
    else:
        main(args.image_file)

