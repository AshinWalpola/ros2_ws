import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib
import argparse
import hailo
from hailo_apps_infra.hailo_rpi_common import app_callback_class
from hailo_apps_infra.detection_pipeline import GStreamerDetectionApp

# -----------------------------------------------------------------------------------------------
# Callback Function
# -----------------------------------------------------------------------------------------------
def app_callback(pad, info, user_data):
    """Callback function to extract object detections from the buffer."""
    buffer = info.get_buffer()
    if buffer is None:
        return Gst.PadProbeReturn.OK

    # Extract detections
    roi = hailo.get_roi_from_buffer(buffer)
    detections = roi.get_objects_typed(hailo.HAILO_DETECTION)

    # Print detected objects
    print("\nDetected Objects:")
    if not detections:
        print("No objects detected.")
    for detection in detections:
        label = detection.get_label()
        confidence = detection.get_confidence()
        print(f"Label: {label}, Confidence: {confidence:.2f}")

    return Gst.PadProbeReturn.OK

# -----------------------------------------------------------------------------------------------
# Main Execution
# -----------------------------------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run inference with Hailo.")
    parser.add_argument("--input", type=str, required=True, help="Path to input image")
    args = parser.parse_args()

    # Create an instance of the user app callback class
    user_data = app_callback_class()

    # Run GStreamerDetectionApp with the image input
    app = GStreamerDetectionApp(app_callback, user_data)
    app.options_menu.input = args.input  # Pass image path to the pipeline
    app.run()
