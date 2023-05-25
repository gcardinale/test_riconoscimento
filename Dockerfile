FROM ghcr.io/opennmt/ctranslate2:latest-ubuntu20.04-cuda11.2


ARG DEBIAN_FRONTEND=noninteractive

# RUN apt update && apt upgrade -y
# RUN apt install software-properties-common -y
# RUN add-apt-repository ppa:deadsnakes/ppa

# Install system dependencies
RUN apt-get update && apt-get install -y \
    # python3.10 \
    # python3-pip \
    # python3.10-venv \
    # libsm6 \
    # libxext6 \
    # libxrender-dev \
    git \
    curl \
    ffmpeg \
    redis-server 


# Create app directory
WORKDIR /app

# # Create virtual environment
# RUN python3.10 -m venv /opt/venv
# ENV PATH="/opt/venv/bin:$PATH"
# Update pip
RUN pip install --upgrade pip
RUN pip install faster-whisper

# Install Gradio and Gradio Client
RUN pip install aioredis celery[redis] Redis fastapi[all]

# Copy source code to app directory
COPY . /app

EXPOSE 8005

ENTRYPOINT ["/usr/bin/env"]
RUN chmod +x start_all.sh
CMD ["/bin/bash", "start_all.sh"]