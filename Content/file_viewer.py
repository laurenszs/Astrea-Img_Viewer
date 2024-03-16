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

        self.view_mode = "flat"  # Default view mode

        self.treeview = ttk.Treeview(self.root)
        self.treeview.pack(side="left", fill="both", expand=True)

        # Toggle view mode button
        toggle_text = "Switch to Tree View" if self.view_mode == "flat" else "Switch to Flat View"
        self.toggle_btn = ttk.Button(self.root, text=toggle_text, command=self.toggle_view_mode)
        self.toggle_btn.pack(side="top", fill="x")

        # Create GUI state object
        self.gui_state = gui_utils.GUIState("File Viewer")

        self.load_files("G:/IMG")

        self.treeview.bind("<<TreeviewSelect>>", self.on_select)

    def toggle_view_mode(self):
        self.view_mode = "tree" if self.view_mode == "flat" else "flat"
        self.toggle_text = "Switch to Tree View" if self.view_mode == "flat" else "Switch to Flat View"
        self.toggle_btn.config(text=self.toggle_text)
        self.load_files("G:/IMG")

    def load_files(self, directory):
        self.treeview.delete(*self.treeview.get_children())
        self.load_files_recursive(directory, "")

    def load_files_recursive(self, directory, parent):
        for entry in os.listdir(directory):
            path = os.path.join(directory, entry)
            if os.path.isdir(path):
                oid = self.treeview.insert(parent, "end", text=entry, open=False)
                self.load_files_recursive(path, oid)
            elif self.is_image_file(path):
                self.treeview.insert(parent, "end", text=entry)

    def on_select(self, event):
        selected_item = self.treeview.selection()
        if selected_item:
            current_path = self.get_full_path(selected_item[0])
            if os.path.isfile(current_path) and self.is_image_file(current_path):
                self.image_viewer.show_image(current_path)
                # Save the last image path using GUI state
                self.gui_state.set_last_image(current_path)

    def get_full_path(self, item_id):
        path_components = []
        while item_id:
            item = self.treeview.item(item_id)
            path_components.append(item["text"])
            item_id = self.treeview.parent(item_id)
        return os.path.join("G:/IMG", *reversed(path_components))

    def is_image_file(self, file_path):
        valid_extensions = ('.jpg', '.jpeg', '.png', '.gif')
        return os.path.splitext(file_path)[1].lower() in valid_extensions


