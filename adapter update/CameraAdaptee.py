from pygigev import PyGigEV as gev

#this is the adaptee, implementing the new camera interface
class CameraAdaptee:
    def __init__(self):
        self.ctx = gev()
        self.width_max = 1936
        self.height_max = 1216

    def open_camera(self):
        # Open the first detected camera
        if self.ctx.GevOpenCamera() == "OK":
            print("Camera opened successfully.")

    def set_parameters(self, crop_factor=1.0):
        # Set image parameters based on crop factor
        width = int(self.width_max / crop_factor)
        height = int(self.height_max / crop_factor)
        x_offset = (self.width_max - width) // 2
        y_offset = (self.height_max - height) // 2
        self.ctx.GevSetImageParameters(width, height, x_offset, y_offset)

    def start_transfer(self, num_images=-1):
        # Initialize and start transferring images
        self.ctx.GevInitializeImageTransfer(1)
        self.ctx.GevStartImageTransfer(num_images)

    def get_image(self):
        # Dummy parameters to showcase functionality
        width, height = 1936, 1216
        return self.ctx.GevGetImageBuffer().reshape(height, width)

    def close_camera(self):
        self.ctx.GevCloseCamera()