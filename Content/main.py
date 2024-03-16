import tkinter as tk
import os
from tkinter import ttk  # Optional, import if needed

from image_viewer import ImageViewer  # Import from image_viewer.py
from file_viewer import FileViewer  # Import from file_viewer.py
import gui_utils  # Import GUIState for managing GUI state


def on_close(root, gui_state, image_viewer):
    # Fetch current window size and save it using set_scale
    width = root.winfo_width()
    height = root.winfo_height()
    gui_state.set_scale((width, height))

    # Save the path of the last image viewed
    if image_viewer.current_image_path:
        gui_state.set_last_image(image_viewer.current_image_path)

    root.destroy()


def main():
    # Create the main application window
    root = tk.Tk()

    # Instantiate GUIState
    gui_state = gui_utils.GUIState('AppGUI')

    # Load and apply saved window size, if available
    scale = gui_state.get_scale()
    if scale:
        root.geometry(f"{scale[0]}x{scale[1]}")

    # Create instances of FileViewer and ImageViewer
    image_viewer = ImageViewer(root)
    file_viewer = FileViewer(root, image_viewer)

    # Attempt to load and display the last viewed image
    last_image_path = gui_state.get_last_image()
    if last_image_path:
        # Ensure the path is valid and the file exists before attempting to display it
        if os.path.exists(last_image_path):
            image_viewer.show_image(last_image_path)

    # Bind the window close event to save the window size and last image viewed
    root.protocol("WM_DELETE_WINDOW", lambda: on_close(root, gui_state, image_viewer))

    # Start the main event loop
    root.mainloop()


if __name__ == "__main__":
    main()
