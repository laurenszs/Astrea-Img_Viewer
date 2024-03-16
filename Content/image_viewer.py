import tkinter as tk
from PIL import Image, ImageTk
import atexit
import gui_utils


class ImageViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Viewer")

        self.image_canvas = tk.Canvas(self.root)
        self.image_canvas.pack(side="right", fill="both", expand=True)

        # Delayed call to show the last image
        last_image_path = gui_utils.load_last_image()
        if last_image_path:
            root.after(100, self.show_image, last_image_path)  # Delay the call

        # Bind the configure event to handle resizing
        self.image_canvas.bind("<Configure>", self.on_canvas_resize)

    def show_image(self, image_path):
        # Open the image
        image = Image.open(image_path)

        # Calculate scaling factor to fit the image within the image canvas while maintaining aspect ratio
        width_ratio = self.image_canvas.winfo_width() / image.width
        height_ratio = self.image_canvas.winfo_height() / image.height
        scale_factor = min(width_ratio, height_ratio)

        # Resize the image
        new_width = int(image.width * scale_factor)
        new_height = int(image.height * scale_factor)
        image = image.resize((new_width, new_height))

        # Convert to PhotoImage
        photo = ImageTk.PhotoImage(image)

        # Calculate coordinates to center the image
        x = (self.image_canvas.winfo_width() - new_width) / 2
        y = (self.image_canvas.winfo_height() - new_height) / 2

        # Display the image
        self.image_canvas.delete("all")  # Clear previous image
        self.image_canvas.create_image(x, y, anchor="nw", image=photo)

        # Keep reference to avoid garbage collection
        self.image_canvas.image = photo
        self.current_image_path = image_path

    def on_canvas_resize(self, event):
        # Resize the image when the canvas is resized
        if self.current_image_path:
            self.show_image(self.current_image_path)
