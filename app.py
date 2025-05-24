from flask import Flask, render_template, request, send_from_directory
from PIL import Image
import os

app = Flask(__name__)

# Folder to save output images
OUTPUT_FOLDER = os.path.join('static', 'output')
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Allowed image extensions
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def resize_image(input_image, target_width, target_height, max_file_size_kb, output_path):
    # Open the input image
    img = Image.open(input_image)
    
    # Resize the image to target size using LANCZOS resampling
    img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
    
    # Start with a reasonable quality and reduce it if the file size is too large
    quality = 95

    while True:
        # Save the resized image with the current quality
        img.save(output_path, format='JPEG', quality=quality)
        
        # Check the file size
        file_size_kb = os.path.getsize(output_path) / 1024  # File size in KB
        
        # If the file size is under the target size, we are done
        if file_size_kb <= max_file_size_kb:
            break
        
        # Otherwise, reduce the quality and try again
        quality -= 5
        if quality < 10:  # Prevent quality from going too low
            print("Could not meet the file size requirement without losing too much quality.")
            break

    return file_size_kb

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return 'No file part'
    file = request.files['image']
    if file.filename == '':
        return 'No selected file'

    if file and allowed_file(file.filename):
        # Get the width, height, and max size from the form
        try:
            target_width = int(request.form['width'])
            target_height = int(request.form['height'])
            max_file_size_kb = int(request.form['max_size'])
        except ValueError:
            return 'Invalid resize parameters. Please enter valid numbers.'

        # Path to save resized image
        output_filename = 'resized_image.jpg'
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)

        # Resize and save image
        file_size_kb = resize_image(file, target_width, target_height, max_file_size_kb, output_path)

        return render_template('index.html',
                               message=f"Image resized to {file_size_kb:.2f} KB",
                               output_image=output_filename)

    else:
        return 'Invalid file type. Please upload an image file (jpg, jpeg, png, gif).'

@app.route('/download_image/<filename>')
def download_image(filename):
    return send_from_directory(directory=OUTPUT_FOLDER, filename=filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

