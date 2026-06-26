import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
import threading


# Import our vision modules
import vision.filters as vf
import vision.detectors as vd
import vision.utils as vu


class VisionStudioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vision Studio - Ultimate CV Project")
        self.root.geometry("900x700")

        # Sate variables
        self.original_image = None
        self.processed_image = None
        self.camera_cap = None
        self.is_camera_active = False
        self.motion_prev_frame = None
        self.tracking_mode = None  # Red , Blue , or None
        self.motion_mode = False

        self.setup_ui()

    def setup_ui(self):
        # --- Top Menu Bar ---
        menubar = tk.Frame(self.root, bg="#333", height=30)
        menubar.pack(side="top", fill="x")

        btn_open = tk.Button(
            menubar, text="Open Image", command=self.open_image, bg="#444", fg="white"
        )
        btn_open.pack(side="left", padx=10, pady=5)

        btn_save = tk.Button(
            menubar,
            text="Save Current",
            command=self.save_current,
            bg="#444",
            fg="white",
        )
        btn_save.pack(side="left", padx=10, pady=5)

        btn_webcam = tk.Button(
            menubar,
            text="Toggle Webcam",
            command=self.toggle_webcam,
            bg="#444",
            fg="white",
        )
        btn_webcam.pack(side="left", padx=10, pady=5)

        btn_exit = tk.Button(
            menubar, text="Exit", command=self.root.quit, bg="#800000", fg="white"
        )
        btn_exit.pack(side="right", padx=10, pady=5)

        # --- Main Display Area ---
        self.canvas_frame = tk.Frame(self.root, bg="black")
        self.canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.canvas_label = tk.Label(self.canvas_frame, bg="black")
        self.canvas_label.pack()

        # Info Label
        self.info_label = tk.Label(
            self.root, text="No image loaded", fg="gray", bg="white"
        )
        self.info_label.pack(fill="x", padx=10, pady=5)

        # --- Controls Area ---
        controls_frame = tk.Frame(self.root, bg="#f0f0f0", height=150)
        controls_frame.pack(fill="x", side="bottom")

        # Filters Section
        filters_label = tk.Label(
            controls_frame, text="Filters:", font=("Arial", 10, "bold"), bg="#f0f0f0"
        )
        filters_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        btn_gray = tk.Button(
            controls_frame,
            text="Grayscale",
            command=lambda: self.apply_filter(vf.apply_grayscale),
        )
        btn_gray.grid(row=1, column=0, padx=5, pady=2)

        btn_blur = tk.Button(
            controls_frame,
            text="Blur",
            command=lambda: self.apply_filter(vf.apply_blur),
        )
        btn_blur.grid(row=1, column=1, padx=5, pady=2)

        btn_sharp = tk.Button(
            controls_frame,
            text="Sharpen",
            command=lambda: self.apply_filter(vf.apply_sharpen),
        )
        btn_sharp.grid(row=1, column=2, padx=5, pady=2)

        btn_sepia = tk.Button(
            controls_frame,
            text="Sepia",
            command=lambda: self.apply_filter(vf.apply_sepia),
        )
        btn_sepia.grid(row=1, column=3, padx=5, pady=2)

        btn_edge = tk.Button(
            controls_frame,
            text="Edge Detect",
            command=lambda: self.apply_filter(vf.apply_edge_detection),
        )
        btn_edge.grid(row=1, column=4, padx=5, pady=2)

        # Real-Time Features Section
        rt_label = tk.Label(
            controls_frame,
            text="Real-Time Features:",
            font=("Arial", 10, "bold"),
            bg="#f0f0f0",
        )
        rt_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)

        btn_red = tk.Button(
            controls_frame,
            text="Track Red",
            command=lambda: self.toggle_tracking("Red"),
        )
        btn_red.grid(row=3, column=0, padx=5, pady=2)

        btn_blue = tk.Button(
            controls_frame,
            text="Track Blue",
            command=lambda: self.toggle_tracking("Blue"),
        )
        btn_blue.grid(row=3, column=1, padx=5, pady=2)

        btn_motion = tk.Button(
            controls_frame, text="Motion Detect", command=self.toggle_motion
        )
        btn_motion.grid(row=3, column=2, padx=5, pady=2)

        self.status_label = tk.Label(
            controls_frame, text="Status: Idle", fg="red", bg="#f0f0f0"
        )
        self.status_label.grid(row=4, column=0, columnspan=5, pady=5)

    def open_image(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            self.original_image = cv2.imread(filepath)
            self.processed_image = self.original_image.copy()
            self.tracking_mode = None
            self.motion_mode = False
            self.motion_prev_frame = None
            self.update_info()
            self.show_image()

    def show_image(self):
        if self.processed_image is None:
            return

        # Convert BGR (OpenCV) to RGB (PIL)
        img_rgb = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)

        # Resize to fit canvas while maintaining aspect ratio
        max_w, max_h = 800, 550
        img_pil.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)

        self.photo = ImageTk.PhotoImage(img_pil)
        self.canvas_label.config(image=self.photo)

        # Update status if needed
        if self.is_camera_active:
            self.root.after(10, self.camera_loop)

    def apply_filter(self, filter_func):
        if self.original_image is None:
            return
        # Apply filter to the current processed image
        self.processed_image = filter_func(self.processed_image)
        self.show_image()

    def toggle_tracking(self, color):
        # ALLOW tracking if EITHER an image is loaded OR the webcam is active
        if self.original_image is None and not self.is_camera_active:
            messagebox.showwarning(
                "Warning", "Please open an image first or turn on the Webcam."
            )
            return

        # If webcam is active, we handle tracking in the camera_loop
        # If image is active, we handle it here
        self.tracking_mode = color if self.tracking_mode != color else None

        if self.is_camera_active:
            self.status_label.config(
                text=f"Status: Tracking {self.tracking_mode}"
                if self.tracking_mode
                else "Status: Idle"
            )
            # The camera_loop will handle the actual drawing
        else:
            # If we are on a static image, apply it immediately
            if self.tracking_mode:
                res, _ = vd.track_color(self.original_image, self.tracking_mode)
                self.processed_image = res
                self.show_image()
                self.status_label.config(text=f"Status: Tracking {self.tracking_mode}")
            else:
                self.processed_image = self.original_image.copy()
                self.show_image()
                self.status_label.config(text="Status: Idle")

    def toggle_motion(self):
        # ALLOW motion detection if EITHER an image is loaded OR the webcam is active
        if self.original_image is None and not self.is_camera_active:
            messagebox.showwarning(
                "Warning", "Please open an image first or turn on the Webcam."
            )
            return

        self.motion_mode = not self.motion_mode
        self.tracking_mode = None  # Disable color tracking if motion is on

        if self.is_camera_active:
            self.motion_prev_frame = None  # Reset previous frame for camera
            self.status_label.config(
                text="Status: Motion Detection ON"
                if self.motion_mode
                else "Status: Idle"
            )
        else:
            if self.motion_mode:
                messagebox.showinfo(
                    "Note",
                    "Motion Detection works best with the Webcam active. "
                    "On a static image, it will show the initial state.",
                )
                self.status_label.config(
                    text="Status: Motion Detection ON (Static Image)"
                )
            else:
                self.status_label.config(text="Status: Idle")

    def process_image_stream(self):
        """Processes the static image if tracking/motion is active."""
        if not self.is_camera_active and (self.tracking_mode or self.motion_mode):
            if self.tracking_mode:
                res, _ = vd.track_color(self.original_image, self.tracking_mode)
                self.processed_image = res
            elif self.motion_mode:
                pass
            self.show_image()

    def toggle_webcam(self):
        if self.is_camera_active:
            if self.camera_cap:
                self.camera_cap.release()
            self.is_camera_active = False
            self.tracking_mode = None
            self.motion_mode = False
            self.motion_prev_frame = None
            self.status_label.config(text="Status: Webcam OFF")
            self.canvas_label.config(image="")  # Clear image
        else:
            self.camera_cap = cv2.VideoCapture(0)

            if not self.camera_cap.isOpened():
                messagebox.showerror("Error", "Could not open webcam.")
                return

            # FORCE RESOLUTION TO 640x480 FOR SPEED (Optional)
            # Uncomment these lines if you want to force 640x480
            self.camera_cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.camera_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

            # Try to set FPS to 30
            self.camera_cap.set(cv2.CAP_PROP_FPS, 30)

            self.is_camera_active = True
            self.original_image = None
            self.status_label.config(text="Status: Webcam ON")
            self.camera_loop()

    def camera_loop(self):
        if not self.is_camera_active:
            return

        ret, frame = self.camera_cap.read()
        if not ret:
            self.root.after(10, self.camera_loop)
            return

        # OPTIMIZATION: Resize to a manageable size if the camera is too high res
        # This drastically improves speed on slower CPUs
        target_width = 640
        h, w = frame.shape[:2]
        if w > target_width:
            scale = target_width / w
            new_h = int(h * scale)
            frame = cv2.resize(frame, (target_width, new_h))

        self.processed_image = frame.copy()

        # Apply Real-time features
        if self.tracking_mode:
            # Optimized: track_color handles its own conversion
            self.processed_image, _ = vd.track_color(
                self.processed_image, self.tracking_mode
            )
        elif self.motion_mode:
            self.processed_image, motion_detected = vd.detect_motion(
                self.processed_image, self.motion_prev_frame
            )
            self.motion_prev_frame = frame.copy()

            if motion_detected:
                self.status_label.config(text="Status: MOTION DETECTED!", fg="red")
            else:
                self.status_label.config(text="Status: Monitoring...", fg="green")

        # Show the image
        self.show_image()

        # Schedule next frame immediately (10ms = ~100 FPS max, but limited by CPU)
        self.root.after(10, self.camera_loop)

    def show_image(self):
        if self.processed_image is None:
            return

        # OPTIMIZATION: Convert only once and resize for display
        # Check dimensions to avoid unnecessary conversion
        if len(self.processed_image.shape) == 2:
            # Grayscale -> RGB
            img_cv = cv2.cvtColor(self.processed_image, cv2.COLOR_GRAY2RGB)
        else:
            # BGR -> RGB
            img_cv = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2RGB)

        # Resize for the canvas (e.g., 800x600 max) to reduce memory usage
        max_w, max_h = 800, 600
        h, w = img_cv.shape[:2]

        # Calculate aspect ratio
        if w > max_w or h > max_h:
            ratio = min(max_w / w, max_h / h)
            new_w = int(w * ratio)
            new_h = int(h * ratio)
            img_cv = cv2.resize(img_cv, (new_w, new_h))

        img_pil = Image.fromarray(img_cv)

        self.photo = ImageTk.PhotoImage(img_pil)
        self.canvas_label.config(image=self.photo)

    def save_current(self):
        """Saves the currently displayed image."""
        if self.processed_image is None:
            messagebox.showwarning("Warning", "No image to save.")
            return

        filepath = vu.save_image(self.processed_image)
        messagebox.showinfo("Success", f"Image saved to:\n{filepath}")

    def update_info(self):
        """Updates the info label with image dimensions and size."""
        if self.processed_image is None:
            self.info_label.config(text="No image loaded")
            return

        info = vu.get_image_info(self.processed_image)
        text = (
            f"Size: {info['width']}x{info['height']} | "
            f"Channels: {info['channels']} | "
            f"Est. Size: {info['size_kb']} KB"
        )
        self.info_label.config(text=text)

    def on_closing(self):
        """Cleanup before closing."""
        if self.is_camera_active and self.camera_cap:
            self.camera_cap.release()
        self.root.destroy()
