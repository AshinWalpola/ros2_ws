import gi
import asyncio
import json
import websockets
import argparse
import hailo

gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib
from hailo_apps_infra.hailo_rpi_common import app_callback_class
from hailo_apps_infra.detection_pipeline import GStreamerDetectionApp

# WebSocket server URL (Modify this to match your ROS2 node)
WS_SERVER_URL = "ws://192.168.1.100:9090"  # Update with ROS2 container IP

async def send_detection_data(data):
    async with websockets.connect(WS_SERVER_URL) as websocket:
        await websocket.send(json.dumps(data))

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

    # Prepare detections for WebSocket message
    detection_list = []
    for detection in detections:
        detection_data = {
            "label": detection.get_label(),
            "confidence": round(detection.get_confidence(), 2)
        }
        detection_list.append(detection_data)

    # Send data via WebSocket
    if detection_list:
        asyncio.run(send_detection_data({"detections": detection_list}))
    
    return Gst.PadProbeReturn.OK

# -----------------------------------------------------------------------------------------------
# Main Execution
# -----------------------------------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run inference with Hailo and send data to ROS2.")
    parser.add_argument("--input", type=str, required=True, help="Path to input image")
    args = parser.parse_args()

    # Create an instance of the user app callback class
    user_data = app_callback_class()

    # Run GStreamerDetectionApp with the image input
    app = GStreamerDetectionApp(app_callback, user_data)
    app.options_menu.input = args.input  # Pass image path to the pipeline
    app.run()
