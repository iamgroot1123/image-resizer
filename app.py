from flask import Flask, render_template, request, send_file
from PIL import Image
import io

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def resize_image(input_image, target_width, target_height, max_file_size_kb):
    img = Image.open(input_image)
    img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)

    quality = 95
    output = io.BytesIO()

    while True:
        output.seek(0)
        output.truncate(0)

        img.save(output, format='JPEG', quality=quality)
        size_kb = len(output.getvalue()) / 1024

        if size_kb <= max_file_size_kb:
            break

        quality -= 5
        if quality < 10:
            print("Could not meet the file size requirement without losing too much quality.")
            break

    output.seek(0)
    return output, size_kb

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return "No file part", 400

    file = request.files['image']
    if file.filename == '':
        return "No selected file", 400

    if not (file and allowed_file(file.filename)):
        return "Invalid file type. Please upload an image file (jpg, jpeg, png, gif).", 400

    try:
        target_width = int(request.form['width'])
        target_height = int(request.form['height'])
        max_file_size_kb = int(request.form['max_size'])
    except (ValueError, KeyError):
        return "Invalid resize parameters. Please enter valid numbers.", 400

    output_image, file_size_kb = resize_image(
        file, target_width, target_height, max_file_size_kb
    )

    # We’ll use JS to read Content-Length and blob size on frontend
    resp = send_file(
        output_image,
        as_attachment=True,
        download_name="resized_image.jpg",
        mimetype="image/jpeg",
    )
    # Optional: add custom header with size
    resp.headers['X-File-Size-KB'] = f"{file_size_kb:.2f}"
    return resp

if __name__ == '__main__':
    app.run(debug=True)
