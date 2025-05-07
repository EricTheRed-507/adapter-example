import cv2
import CameraHandler

class ImageClient:
    def __init__(self, num_images=100):
        self.camera_handler = CameraHandler()
        self.num_images = num_images

    def acquire_and_display_images(self):
        # Start capturing images
        self.camera_handler.adjust_camera_width()
        self.camera_handler.start_grabbing(self.num_images)

        while True:
            # Retrieve each image
            image = self.camera_handler.get_image()

            if image is not None:
                # Display the image (or process accordingly)
                cv2.imshow('Camera', image)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        # Once done, stop and close the camera
        self.camera_handler.stop_and_close()