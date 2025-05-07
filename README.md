# Adapter pattern example

## Background to the application of interest
This example depicts a real scenario with developed software to interface with cameras throughout manufacturing facilities. The role of this system is to have multiple connection points to the cameras for displaying, storage of the camera frames in databases, and tacking on image processing for defect detection. The following depicts the high level setup:
![CameraServerClient drawio](https://github.com/user-attachments/assets/f360ac3a-9d6d-4b0e-ab86-bd2d403fdbfc)

A typical facility has tens of cameras. Each camera can be accessed by multiple clients. Typically, there would be a central hub that displayed between 1 and 10 camera views in a control station room, but also each camera could be directly connected to one of many laptops that would be brought out to the manufacturing floor for close up, remote inspection.

In the ```./original/``` directory, you'll see a simplified depiction of the code. The ```ImageClient.py``` is the client code that connects to the CameraHandler.py, which is the code / class that interfaces with the camera on the server.
These systems almost always used one particular brand of camera, which is a Basler.

## Situation that required an Adapter
Some customers would ask for special cameras that suite particular needs (higher frame rate, larger sensors, non standard color schemes, etc). To custom tailor these requests, we would have to add these specialized cameras upon request.

If we were NOT using an adapter, we would have to implement the following workflow:
- Add new camera interfacing code module on the server.
- Update client such that the target has if/else statements or case/switch statements wherever the hardware interface code occurs.
- Roll out these changes to one location on the server, and update every single client (which could be up to 50) with the new client code. [BIG TASK WITH POTENTIAL ERROR IN MISSED DEVICES!!]

If we DID use an adapter, we would have to implement the following workflow:
- No changes needed to make on any client code.
- Add new camera interfacing code module on the server, as well as Adapter->Adaptee classes to keep client code consistent.

As one can see from reading above, utilizing the adapter pattern involves significant reduction of scope for the rollout of a new camera type if they're custom requests at various manufacturing facilities. All we need to do is update the server code in one location (the server rack) and we don't have to manage tens of client code updates running on the client machines.

## Adapter implementation explained
## Original Code
In the directory ./existing code/ , you can see what the original implemenation was with CameraHandler.py and ImageClient.py.

This class below manages the connection to the CameraHandler class and calls all of the methods which were written as an interfact to the Basler cameras. It calls methods to set the camera's width, start grabbing images, and return these images upon request.
### ImageClient.py
```
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
```

This class below handles the interface to the actual camera hardware. It handles the logic to initialize, set properties through firmware, start grabbing images upon request, and return images to the caller.
### CameraHandler.py
```
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
```
## Updated Adapter code
In the directory ./adapter update/ , you can see what the new adapter implemenation is with CameraHandler.py, CameraAdaptee.py, and ImageClient.py .


This class below is the adapter, and is named "CameraHandler" so that all of the client code stays exactly the same. It provides all of the same methods, but under each it calls the more specific functions for the new camera interface (in this case, Dalsa cameras). 
### CameraHandler.py
```
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
```

This class below is the adaptee for the new camera type. It manages all of the camera interface logic for the new hardware, and is called by the adapter which is the "CameraHandler" class. 
### CameraAdaptee.py
```
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
```

Nothing to show for this one, because it's the exact same as the ImageClient.py from the existing code. This was the whole purpose of this design pattern for this scenario!
### ImageClient.py
NOTE, THIS IS UNCHANGED!!!

## Conclusion
As one can see from reading the details above, this is a scenario where the adapter pattern is particularly useful. We only had to modify a few clases on the server and push the changes out to one location, and didn't have to update the client at all; which would have been a large effor in terms of operations and downtime for the customers. The adapter can be a useful tool in the right situation, such as this.

## Note
I don't have details on how to compile this and make it run, because one would need both a Basler and Dalsa camera to operate this code. This is more a visual and contextual example, but not one that's intent to be run.
