from flask import Flask, render_template, request, send_file
from PIL import Image
import io

app = Flask(__name__)

# Allowed image extensions
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def resize_image(input_image, target_width, target_height, max_file_size_kb):
    # Open the input image
    img = Image.open(input_image)

    # Resize the image to target size using LANCZOS resampling
    img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)

    # Start with a reasonable quality and reduce it if the file size is too large
    quality = 95

    while True:
        # Save to BytesIO buffer
        output_buffer = io.BytesIO()
        img.save(output_buffer, format='JPEG', quality=quality)
        output_buffer.seek(0)

        # Check the file size
        file_size_kb = len(output_buffer.getvalue()) / 1024  # File size in KB

        # If the file size is under the target size, we are done
        if file_size_kb <= max_file_size_kb:
            break

        # Otherwise, reduce the quality and try again
        quality -= 5
        if quality < 10:  # Prevent quality from going too low
            print("Could not meet the file size requirement without losing too much quality.")
            break

    return output_buffer, file_size_kb

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

        # Resize image in memory
        output_buffer, file_size_kb = resize_image(file, target_width, target_height, max_file_size_kb)

        # Send the resized image as a downloadable file
        output_buffer.seek(0)
        return send_file(output_buffer, as_attachment=True, download_name='resized_image.jpg', mimetype='image/jpeg')

    else:
        return 'Invalid file type. Please upload an image file (jpg, jpeg, png, gif).'

if __name__ == '__main__':
    app.run(debug=True)

