import gi
import argparse
import cv2
import numpy as np
import os
import hailo

gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib
from hailo_apps_infra.hailo_rpi_common import (
    get_caps_from_pad,
    get_numpy_from_buffer,
    app_callback_class,
)
from hailo_apps_infra.detection_pipeline import GStreamerDetectionApp

# -----------------------------------------------------------------------------------------------
# User-defined class for handling frame processing
# -----------------------------------------------------------------------------------------------
class user_app_callback_class(app_callback_class):
    def __init__(self):
        super().__init__()
        self.frame_saved = False  # Ensures only one frame is saved

# -----------------------------------------------------------------------------------------------
# Callback Function: Process Each Frame
# -----------------------------------------------------------------------------------------------
def app_callback(pad, info, user_data):
    if user_data.frame_saved:  # Stop after one frame
        return Gst.PadProbeReturn.OK

    buffer = info.get_buffer()
    if buffer is None:
        return Gst.PadProbeReturn.OK

    format, width, height = get_caps_from_pad(pad)

    if format is not None and width is not None and height is not None:
        frame = get_numpy_from_buffer(buffer, format, width, height)
        if frame is not None:
            # Convert RGB to BGR for OpenCV
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            # Save the captured frame
            save_path = "/home/uml/captured_frame.jpg"
            cv2.imwrite(save_path, frame)
            print(f"Doneee!! Frame captured and saved to {save_path}")

            user_data.frame_saved = True  # Ensure only one frame is saved
            return Gst.PadProbeReturn.REMOVE  # Stop after first frame

    return Gst.PadProbeReturn.OK

# -----------------------------------------------------------------------------------------------
# Main Function
# -----------------------------------------------------------------------------------------------
if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(description="Hailo Detection with Dynamic Input")
    parser.add_argument("--input", type=str, required=True, help="Input source: 'rpi' for camera or file path for video/image")
    args = parser.parse_args()

    # Determine input source (Modify pipeline instead of passing input_src)
    if args.input.lower() == "rpi":
        os.environ["GSTREAMER_INPUT_SRC"] = "v4l2src device=/dev/video0 ! video/x-raw,framerate=30/1 ! videoconvert"
        print("Using Raspberry Pi Camera as input.")
    else:
        if not os.path.exists(args.input):
            print(f"Nope Error: File '{args.input}' not found.")
            exit(1)
        os.environ["GSTREAMER_INPUT_SRC"] = f"filesrc location={args.input} ! decodebin ! videoconvert"
        print(f"Using video file: {args.input}")

    # Run the detection pipeline
    user_data = user_app_callback_class()
    app = GStreamerDetectionApp(app_callback, user_data)  # Remove 'input_src'
    app.run()