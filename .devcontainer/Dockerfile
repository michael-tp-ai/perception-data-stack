# Start with a lightweight, official Python 3.10 Linux image
FROM python:3.10-slim-bookworm

# Install necessary system tools (like git for version control and build-essential for compiling)
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install 'uv' directly from the official astral-sh image (the fastest way)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Tell 'uv' to create the virtual environment inside /opt/.venv instead of the local folder.
# This completely prevents conflicts between your host laptop and the Linux container.
ENV UV_PROJECT_ENVIRONMENT="/opt/.venv"
ENV PATH="/opt/.venv/bin:$PATH"

# Set the default directory when you open the terminal
WORKDIR /workspaces/perception-stack
