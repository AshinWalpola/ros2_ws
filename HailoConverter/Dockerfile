FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ="Europe/Berlin"
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

# Install system dependencies and dev tools
RUN apt-get update && apt-get install --no-install-recommends -y \
    python3 \
    python3-pip \
    python3.10-dev \
    python3.10-distutils \
    python3-tk \
    curl \
    git \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    libfuse2 \
    graphviz \
    graphviz-dev \
    libgraphviz-dev \
    locales \
    sudo && \
    sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure locales && \
    update-locale && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Upgrade pip, install pygraphviz + numpy (correct version for DFC)
RUN pip install --upgrade pip && \
    pip install pygraphviz numpy==1.23.3

# Create non-root user
ARG USERNAME=hailo
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME && \
    useradd --uid $USER_UID --gid $USER_GID -m $USERNAME && \
    echo "$USERNAME ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/$USERNAME && \
    chmod 0440 /etc/sudoers.d/$USERNAME

# Switch to non-root user
USER $USERNAME

# Add Hailo Dataflow Compiler wheel and install
ENV PATH="/home/$USERNAME/.local/bin:${PATH}"
COPY ./hailo_dataflow_compiler-3.30.0-py3-none-linux_x86_64.whl /home/$USERNAME/
RUN pip install /home/$USERNAME/hailo_dataflow_compiler-3.30.0-py3-none-linux_x86_64.whl && \
    rm /home/$USERNAME/hailo_dataflow_compiler-3.30.0-py3-none-linux_x86_64.whl

# Set workspace folder (you’ll mount your project here)
WORKDIR /workspace

# Optional shell by default
CMD ["/bin/bash"]
