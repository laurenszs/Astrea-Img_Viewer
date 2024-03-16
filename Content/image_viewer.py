import tkinter as tk
from PIL import Image, ImageTk


class ImageViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Viewer")

        self.image_canvas = tk.Canvas(self.root)
        self.image_canvas.pack(side="right", fill="both", expand=True)

        self.current_image_path = None
        self.image_canvas.bind("<Configure>", self.on_canvas_resize)

    def show_image(self, image_path):
        self.current_image_path = image_path

        # Open the image
        image = Image.open(image_path)

        # Get the canvas's width and height
        canvas_width = self.image_canvas.winfo_width()
        canvas_height = self.image_canvas.winfo_height()

        # Ensure canvas dimensions are valid
        if canvas_width > 1 and canvas_height > 1:
            width_ratio, height_ratio = self.get_scale_ratios(image)
            scale_factor = min(width_ratio, height_ratio)
            self.resized_image = image.resize((int(image.width * scale_factor), int(image.height * scale_factor)))
            self.photo = ImageTk.PhotoImage(self.resized_image)
            self.center_and_display_image()
        else:
            # Optionally, you could log a message or set a flag to try redisplaying the image later
            pass

    def get_scale_ratios(self, image):
        # Calculate scaling factor to fit the image within the canvas while maintaining aspect ratio
        width_ratio = self.image_canvas.winfo_width() / image.width
        height_ratio = self.image_canvas.winfo_height() / image.height
        return width_ratio, height_ratio

    def center_and_display_image(self):
        x = (self.image_canvas.winfo_width() - self.resized_image.width) / 2
        y = (self.image_canvas.winfo_height() - self.resized_image.height) / 2
        self.image_canvas.create_image(x, y, anchor="nw", image=self.photo)
        self.image_canvas.image = self.photo

    def on_canvas_resize(self, event):
        if self.current_image_path:
            self.show_image(self.current_image_path)
