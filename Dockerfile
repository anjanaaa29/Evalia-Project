# Use official Python 3.11 slim image
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libasound2-dev \
    portaudio19-dev \
    ffmpeg \
    libssl-dev \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy only requirements and install first (for cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download spacy model (if used)
RUN python -m spacy download en_core_web_sm

# Copy everything else
COPY . .

# Let Streamlit run on GCP
ENV STREAMLIT_SERVER_PORT=8080
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Expose port
EXPOSE 8080

# Run app
CMD ["streamlit", "run", "main.py", "--server.port=8080", "--server.address=0.0.0.0"]
