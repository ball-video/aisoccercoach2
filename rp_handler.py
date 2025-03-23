import runpod
import cv2
import json
import base64
import os


#docker build --platform linux/amd64 --tag 883054/aisoccercoach1:test3 .
#docker push 883054/aisoccercoach1:test3


def handler(event):
    # Get the base64-encoded video from the request
    video_data = event.get("input", {}).get("video_data", "")
    if not video_data:
        return {"error": "No video data provided"}

    # Decode the video from base64 and save it temporarily
    video_path = "/tmp/input_video.mp4"
    with open(video_path, "wb") as f:
        f.write(base64.b64decode(video_data))

    # Process the video (e.g., count frames)
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        os.remove(video_path)
        return {"error": "Failed to open video"}

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    os.remove(video_path)  # Clean up

    return {"status": "Video processed", "frame_count": frame_count}

if __name__ == '__main__':
    runpod.serverless.start({'handler': handler})


