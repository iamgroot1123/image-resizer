# QuickResize – Online Image Resizer

**Live Website:** https://quickresizeapp.vercel.app/

QuickResize is a fast, browser-based image resizer that allows users to upload an image, specify a target width, height, and maximum file size, and instantly download a resized JPEG — all processed safely in-memory on the server.

No storage.  
No clutter.  
Just **upload → resize → download.**

---

## 🚀 Features

- Upload any image (JPG, JPEG, PNG, GIF)
- Drag & drop or file picker
- Live preview of the uploaded image
- Custom resize options:
  - Target width
  - Target height
  - Max output file size (KB)
- Automatic JPEG compression loop
- Fully in-memory (files are **never saved on the server**)
- Auto-download + “Download Again” button
- Responsive, modern UI
- Dark theme
- Hosted on Vercel

---

## 🌐 Live Website

👉 **https://quickresizeapp.vercel.app/**  
Accessible to anyone. No login or installation required.

---

## 📁 Project Structure

.
├── app.py
├── requirements.txt
├── vercel.json
├── templates
│ └── index.html
└── static
└── style.css

---

## 🧠 How It Works

1. User uploads an image.
2. Flask + Pillow resize it to the exact width & height.
3. A dynamic loop reduces JPEG quality until file size ≤ max KB.
4. Processed image is returned as a downloadable blob.
5. Nothing is written to disk on the server — fully memory-based.

---

## 💻 Tech Stack

### **Frontend**

- HTML
- CSS
- Vanilla JavaScript
- Drag & drop file handling
- Blob-based downloads

### **Backend**

- Python
- Flask
- Pillow (PIL)

### **Deployment**

- Vercel
- Python Serverless Functions
- `@vercel/python` runtime

---

📦 Future Improvements
Batch image resizing

Preserve EXIF metadata (optional)

Support output formats (PNG, WEBP)

Compress without changing resolution

Multi-language UI

Light/dark theme toggle

---
