import json
import os

settings_file = "gui_settings.json"

def save_gui_size(width, height):
    settings = load_settings()
    settings['gui_size'] = {'width': width, 'height': height}
    save_settings(settings)

def get_saved_gui_size():
    settings = load_settings()
    return settings.get('gui_size', {'width': 800, 'height': 600})  # Default size

def save_last_image(image_path):
    settings = load_settings()
    settings['last_image'] = image_path
    save_settings(settings)

def load_last_image():
    settings = load_settings()
    return settings.get('last_image', None)

def load_settings():
    if os.path.exists(settings_file):
        with open(settings_file, 'r') as file:
            return json.load(file)
    return {}

def save_settings(settings):
    with open(settings_file, 'w') as file:
        json.dump(settings, file, indent=4)

# Example usage in other parts of your application
# To save GUI size: gui_utils.save_gui_size(1024, 768)
# To get saved GUI size: width, height = gui_utils.get_saved_gui_size().values()
# To save last viewed image path: gui_utils.save_last_image('path/to/image.png')
# To load last viewed image path: last_image_path = gui_utils.load_last_image()
