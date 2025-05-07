import CameraAdaptee

#this is the adapter
class CameraHandler:
    def __init__(self):
        # Use the new camera handler
        self.new_camera_handler = CameraAdaptee()
        self.new_camera_handler.open_camera()

    def adjust_camera_width(self):
        # Adapt set_parameters method
        self.new_camera_handler.set_parameters(crop_factor=1.0)

    def start_grabbing(self, num_images):
        # Adapt start_transfer method
        self.new_camera_handler.start_transfer(num_images)

    def get_image(self):
        # Adapt get_image retrieval
        return self.new_camera_handler.get_image()

    def stop_and_close(self):
        # Adapt close_camera method
        self.new_camera_handler.close_camera()