import os
import sys
from fastapi import FastAPI, File, UploadFile, HTTPException
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import shutil
from pathlib import Path

app = FastAPI()

# Ensure directories exist
INPUT_DIR = "/app/input"
OUTPUT_DIR = "/app/output"
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/ocr/")
async def ocr_pdf(file: UploadFile = File(...)):
    # Validate file is a PDF
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="File must be a PDF")

    # Save uploaded file
    pdf_path = Path(INPUT_DIR) / file.filename
    with open(pdf_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Convert PDF to images
        pages = convert_from_path(pdf_path, dpi=300)
        results = []

        for i, page in enumerate(pages):
            img_path = Path(OUTPUT_DIR) / f"page_{i+1}.jpg"
            txt_path = Path(OUTPUT_DIR) / f"page_{i+1}.txt"

            # Save image
            page.save(img_path, "JPEG", quality=95)

            # Perform OCR
            config = '--oem 3 --psm 6'
            text = pytesseract.image_to_string(Image.open(img_path), config=config)

            # Save text to file
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(text)

            # Collect results
            results.append({
                "page": i + 1,
                "text": text.strip()[:100] + "..." if text.strip() else "",
                "text_file": str(txt_path),
                "image_file": str(img_path)
            })

        # Clean up input file
        pdf_path.unlink()

        return {"status": "success", "pages": len(pages), "results": results}

    except Exception as e:
        # Clean up on error
        if pdf_path.exists():
            pdf_path.unlink()
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")