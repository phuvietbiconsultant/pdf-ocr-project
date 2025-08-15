# PDF OCR Docker Container

This repository contains a Dockerfile and script to build a container for OCR processing of PDF files using Tesseract.

## Usage
- Build the image.
- Run the container with mounted input/output volumes.
- Execute `python ocr_pdf.py /app/input/yourfile.pdf` inside the container.