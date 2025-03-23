import runpod
import cv2
import json
import base64
import os


#docker build --platform linux/amd64 --tag 883054/aisoccercoach1:test4 .
#docker push 883054/aisoccercoach1:test4


def handler(event):
    try:
        # Get the base64-encoded video from the request
        video_data = event.get("input", {}).get("video_data", "")
        if not video_data:
            return {"error": "No video data provided"}

        # Decode the video from base64 and save it temporarily
        input_path = "/tmp/input_video.mp4"
        with open(input_path, "wb") as f:
            f.write(base64.b64decode(video_data))

        # Open the input video
        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            os.remove(input_path)
            return {"error": "Failed to open input video"}

        # Get video properties
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Define the output video path and codec
        output_path = "/tmp/output_video.mp4"
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Codec for .mp4
        out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height), isColor=False)

        # Process each frame
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            # Convert frame to grayscale
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Write grayscale frame to output video
            out.write(gray_frame)

        # Release resources
        cap.release()
        out.release()
        os.remove(input_path)  # Clean up input

        # Read the output video and encode it to base64
        with open(output_path, "rb") as f:
            output_video_data = base64.b64encode(f.read()).decode("utf-8")

        os.remove(output_path)  # Clean up output

        return {
            "status": "Video processed",
            "frame_count": frame_count,
            "output_video": output_video_data
        }

    except Exception as e:
        return {"error": f"Processing failed: {str(e)}"}

if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})

