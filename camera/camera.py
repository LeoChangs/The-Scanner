from picamera2 import Picamera2
from libcamera import controls
import time
from abc import ABC, abstractmethod

class CameraSource(ABC):
    @abstractmethod
    def capture(self):
        """Return a raw image (numpy array) from the source."""
        ...

def capture_document(output_path="scan.jpg"):
    picam2 = Picamera2()

    # Use the sensor's full resolution for OCR-quality detail
    config = picam2.create_still_configuration(
        main={"size": (4608, 2592)}  # Camera Module 3 max still res
    )
    picam2.configure(config)

    # Module 3 has autofocus — use it, and give it time to lock
    picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})
    picam2.start()
    time.sleep(2)  # let autofocus settle before capturing

    picam2.capture_file(output_path)
    picam2.stop()
    return output_path

if __name__ == "__main__":
    path = capture_document()
    print(f"Saved to {path}")