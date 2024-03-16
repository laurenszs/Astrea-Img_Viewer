import os
import tkinter as tk
from tkinter import ttk
from image_viewer import ImageViewer
import gui_utils


class FileViewer:
    def __init__(self, root, image_viewer):
        self.root = root
        self.root.title("File Viewer")
        self.image_viewer = image_viewer

        # Set GUI size from saved settings
        saved_size = gui_utils.get_saved_gui_size()
        self.root.geometry(f"{saved_size['width']}x{saved_size['height']}")

        self.view_mode = "flat"  # Default view mode: 'flat' or 'tree'

        self.treeview = ttk.Treeview(self.root)
        self.treeview.pack(side="left", fill="both", expand=True)

        # Toggle view mode button
        self.toggle_btn = ttk.Button(self.root, text="Switch to Tree View", command=self.toggle_view_mode)
        self.toggle_btn.pack(side="top", fill="x")

        self.load_files("G:/IMG")

        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def toggle_view_mode(self):
        if self.view_mode == "flat":
            self.view_mode = "tree"
            self.toggle_btn.config(text="Switch to Flat View")
        else:
            self.view_mode = "flat"
            self.toggle_btn.config(text="Switch to Tree View")
        self.load_files("G:/IMG")

    def load_files(self, directory):
        self.treeview.delete(*self.treeview.get_children())
        if self.view_mode == "flat":
            self.load_files_flat(directory)
        else:
            self.load_files_tree(directory)

    def load_files_flat(self, directory):
        files = os.listdir(directory)
        files.sort()
        current_letter = None
        for file in files:
            file_path = os.path.join(directory, file)
            if os.path.isdir(file_path) or not self.is_image_file(file_path):
                continue
            if not current_letter or file[0].upper() != current_letter:
                current_letter = file[0].upper()
                self.treeview.insert("", "end", text=current_letter, tags=("dividing_line",))
            self.treeview.insert("", "end", text=file)

        self.treeview.tag_configure("dividing_line", background="gray")
        self.treeview.bind("<<TreeviewSelect>>", self.on_select)

    def load_files_tree(self, directory, parent=""):
        for entry in os.listdir(directory):
            path = os.path.join(directory, entry)
            is_dir = os.path.isdir(path)
            if is_dir:
                oid = self.treeview.insert(parent, "end", text=entry, open=False)
                self.load_files_tree(path, oid)
            else:
                if self.is_image_file(path):
                    self.treeview.insert(parent, "end", text=entry)

        self.treeview.bind("<<TreeviewSelect>>", self.on_select)

    def on_select(self, event):
        selected_item = self.treeview.selection()
        if selected_item:
            item = self.treeview.item(selected_item)
            if self.view_mode == "flat":
                current_path = os.path.join("G:/IMG", item["text"])
            else:
                current_path = self.get_full_path(selected_item[0])
            if os.path.isfile(current_path) and self.is_image_file(current_path):
                self.image_viewer.show_image(current_path)

    def get_full_path(self, item_id):
        path_components = []
        while item_id:
            item = self.treeview.item(item_id)
            path_components.append(item["text"])
            item_id = self.treeview.parent(item_id)
        return os.path.join("G:/IMG", *reversed(path_components))

    def is_image_file(self, file_path):
        valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
        file_extension = os.path.splitext(file_path)[1].lower()
        return file_extension in valid_extensions

    def on_close(self):
        # Save GUI size and last viewed image path on app closure
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        gui_utils.save_gui_size(width, height)
        if self.image_viewer.current_image_path:  # Make sure this attribute exists in ImageViewer
            gui_utils.save_last_image(self.image_viewer.current_image_path)
        self.root.destroy()


def main():
    root = tk.Tk()
    image_viewer = ImageViewer(root)
    file_viewer = FileViewer(root, image_viewer)

    # Set minimum GUI size
    #  gui_utils.set_minimum_gui_size(root)
    last_image_path = gui_utils.load_last_image()
    if last_image_path:
        image_viewer.show_image(last_image_path)

    gui_utils.save_gui_size(root.winfo_width(), root.winfo_height())
    width, height = gui_utils.get_saved_gui_size().values()

    if width | height:
        root.geometry(f"{width}x{height}")

    root.protocol("WM_DELETE_WINDOW", file_viewer)  # Correct placement
    root.mainloop()


if __name__ == "__main__":
    main()
