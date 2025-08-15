FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    poppler-utils \
    tesseract-ocr \
    imagemagick \
    build-essential \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Fix ImageMagick PDF security policy
RUN sed -i 's/rights="none"/rights="read|write"/' /etc/ImageMagick-6/policy.xml || true

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install pdf2image pytesseract easyocr pillow opencv-python-headless fastapi uvicorn

# Create directories
RUN mkdir -p /app/input /app/output

# Copy scripts
COPY *.py /app/

# Set working directory
WORKDIR /app

# Start the FastAPI server
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]