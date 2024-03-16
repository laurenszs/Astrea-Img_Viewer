import os
import json


class GUIState:
    """
    This class manages saving and loading GUI state information.
    """

    def __init__(self, app_name, data_dir="gui_data"):
        self.app_name = app_name
        self.data_dir = data_dir
        self.data_file = os.path.join(self.data_dir, f"{self.app_name}.json")

        # Ensure data directory exists
        os.makedirs(self.data_dir, exist_ok=True)

        self.state = {"scale": None, "last_image": None}
        self.load_state()

    def save_state(self):
        """
        Saves the current GUI state to a JSON file.
        """
        with open(self.data_file, "w") as f:
            json.dump(self.state, f)

    def load_state(self):
        """
        Loads the GUI state from a JSON file if it exists.
        """
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                try:
                    self.state = json.load(f)
                except json.JSONDecodeError:
                    # Handle potential errors while loading JSON
                    pass

    def get_scale(self):
        """
        Returns the saved scale value or None.
        """
        return self.state.get("scale")

    def set_scale(self, scale):
        """
        Sets the scale value in the state and saves it.
        """
        self.state["scale"] = scale
        self.save_state()

    def get_last_image(self):
        """
        Returns the saved last image path or None.
        """
        return self.state.get("last_image")

    def set_last_image(self, image_path):
        """
        Sets the last image path in the state and saves it.
        """
        self.state["last_image"] = image_path
        self.save_state()

