import base64
from io import BytesIO
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox


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


def select_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        try:
            base64_str = image_to_base64(file_path)
            text_area.delete(1.0, tk.END)  # Clear the text area
            text_area.insert(tk.END, base64_str)  # Insert the base64 string
            save_base64_to_curl_file(base64_str, file_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert image: {str(e)}")


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
        "      \"content\": \"Can you tell me what the following image depicts?\","
        f"      \"images\":[ \"{base64_str}\"]"
        "    }"
        "  ],"
        " \"stream\": false"
        "}'"
    )

    # curl_command = (
       # f"curl --location 'http://localhost:11434/api/chat'\ \n"
       # f"--header 'Content-Type: application/json'\  \n"
       # f" --data '{ "
       # f"-d '{{\"image_data\": \"{base64_str}\"}}'"
   # )
    # Make the output file path based on the original image path
    output_file_path = original_image_path + "_curl_command.txt"
    # Write the cURL command to the file
    with open(output_file_path, 'w') as outfile:
        outfile.write(curl_command)
    messagebox.showinfo("Success", f"cURL command saved to: {output_file_path}")


# GUI setup
root = tk.Tk()
root.title("Image to Base64 Converter")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

select_button = tk.Button(frame, text="Select Image", command=select_file)
select_button.pack(side=tk.LEFT)

text_area = tk.Text(root, wrap=tk.WORD, height=20, width=60)
text_area.pack(padx=10, pady=10)

root.mainloop()