from pypylon import pylon

class CameraHandler:
    def __init__(self):
        # Initialize the camera
        self.camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        self.camera.Open()

    def adjust_camera_width(self):
        # Adjust the camera width
        new_width = self.camera.Width.Value - self.camera.Width.Inc
        if new_width >= self.camera.Width.Min:
            self.camera.Width.Value = new_width

    def start_grabbing(self, num_images):
        # Start grabbing images
        self.camera.StartGrabbingMax(num_images)

    def get_image(self):
        # Retrieve an image from the camera
        if self.camera.IsGrabbing():
            grab_result = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            if grab_result.GrabSucceeded():
                img = grab_result.Array
                grab_result.Release()
                return img
            grab_result.Release()

    def stop_and_close(self):
        # Close the camera
        self.camera.Close()