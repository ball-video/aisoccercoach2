FROM python:3.10-slim

WORKDIR /

# Install system dependencies required for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies, including OpenCV
RUN pip install --no-cache-dir runpod opencv-python-headless

COPY rp_handler.py /

# Start the container
CMD ["python3", "-u", "rp_handler.py"]
