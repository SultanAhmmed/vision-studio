# Vision Studio 

> A high-performance, modular desktop application for real-time Computer Vision built with **Python**, **OpenCV**, and **Tkinter**.

Vision Studio is a feature-rich desktop application that demonstrates practical computer vision techniques through an intuitive graphical interface. It combines image processing, real-time webcam analysis, and modern software architecture into a single project suitable for learning, portfolios, and future robotics applications.

---

## Preview

> Add screenshots or GIFs of your application here.

```
screenshots/
├── home.png
├── filters.png
├── color_tracking.png
└── motion_detection.png
```

---

## Features

### Image Processing

* Open and display images
* Save processed images
* Grayscale conversion
* Gaussian Blur
* Sharpen filter (Convolution)
* Sepia filter
* Image resizing
* Image rotation

---

### Edge Detection

* Canny Edge Detection
* Noise reduction before edge extraction
* Real-time preview

---

### Real-Time Computer Vision

* Live webcam feed
* HSV-based Red object tracking
* HSV-based Blue object tracking
* Motion detection using frame differencing
* Automatic bounding boxes around detected objects

---

### Performance

* High-FPS webcam processing
* Frame resizing for faster computation
* Efficient memory management
* Non-blocking GUI updates using Tkinter's `after()` method

---

### Software Engineering

* Modular project structure
* Separation of GUI and vision logic
* Clean state management
* Error handling
* Easily extendable architecture

---

## Technology Stack

| Layer               | Technology   | Purpose                              |
| ------------------- | ------------ | ------------------------------------ |
| Language            | Python 3.10+ | Core programming language            |
| Computer Vision     | OpenCV       | Image processing and computer vision |
| GUI                 | Tkinter      | Desktop application interface        |
| Image Rendering     | Pillow       | Display OpenCV images in Tkinter     |
| Numerical Computing | NumPy        | Image and matrix operations          |

---

## 📂 Project Structure

```text
vision_studio/
│
├── main.py                 # Application entry point
│
├── gui/
│   ├── __init__.py
│   ├── app.py              # Main application window
│   └── controls.py         # Buttons, menus and sliders
│
├── vision/
│   ├── __init__.py
│   ├── filters.py          # Grayscale, Blur, Sharpen, Sepia
│   ├── detectors.py        # Edge, Motion, Color Tracking
│   └── utils.py            # Helper functions
│
├── assets/
│   ├── icons/
│   └── images/
│
├── screenshots/
│
├── recordings/
│
├── requirements.txt
├── README.md
└── LICENSE
```

---

## ⚙️ Installation

### Clone the Repository

```bash
git clone https://github.com/SultanAhmmed/vision-studio.git

cd vision-studio
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install opencv-python pillow numpy
```

---

## ▶️ Run the Application

```bash
python main.py
```

---

## 🖥️ How to Use

### Image Processing

* Open an image
* Apply filters
* Detect edges
* Save processed image

### Webcam Mode

* Start webcam
* Track red objects
* Track blue objects
* Detect motion
* Capture screenshots

---

## 🧠 Skills Demonstrated

### Computer Vision

* Image filtering
* Convolution kernels
* Color space conversion (BGR ↔ HSV)
* Edge Detection (Canny)
* HSV Thresholding
* Motion Detection
* Contour Detection
* Bounding Box Detection

---

### Software Engineering

* Modular architecture
* Object-Oriented Programming
* GUI development
* State management
* Error handling
* Resource management
* Real-time event loops

---

### Performance Optimization

* Frame resizing
* Efficient image processing
* Non-blocking GUI updates
* Memory-efficient webcam streaming

---


## Future Improvements

* Brightness and Contrast controls
* Face Detection
* YOLO Object Detection
* QR Code Scanner
* Barcode Detection
* Image Histogram
* Video Recording
* Screenshot Gallery
* Camera Settings
* Dark Mode UI
* Multi-language Support
* Unit Testing
* Packaging with PyInstaller

---

## Screenshots

| Home           | Filters        |
| -------------- | -------------- |
| Add Screenshot | Add Screenshot |

| Color Tracking | Motion Detection |
| -------------- | ---------------- |
| Add Screenshot | Add Screenshot   |

---

## Contributing

Contributions are welcome.

1. Fork the repository
2. Create a new feature branch
3. Commit your changes
4. Push your branch
5. Open a Pull Request

---

## Author

**Sultan Ahmmed**

* GitHub: https://github.com/SultanAhmmed

---

## 📄 License

This project is licensed under the GPL License.

See the `LICENSE` file for more information.
