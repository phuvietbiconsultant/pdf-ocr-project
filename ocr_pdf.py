import sys
import os
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
if len(sys.argv) < 2:
    print("❌ Usage: python ocr_pdf.py /path/to/file.pdf")
    sys.exit(1)
pdf_path = sys.argv[1]
if not os.path.exists(pdf_path):
    print(f"❌ File not found: {pdf_path}")
    sys.exit(1)
output_dir = "/app/output"
os.makedirs(output_dir, exist_ok=True)
try:
    pages = convert_from_path(pdf_path, dpi=300)
    print(f"✅ Converted {len(pages)} pages")
    
    for i, page in enumerate(pages):
        img_path = os.path.join(output_dir, f"page_{i+1}.jpg")
        txt_path = os.path.join(output_dir, f"page_{i+1}.txt")
        
        page.save(img_path, "JPEG", quality=95)
        
        # Enhanced OCR config for receipts/documents
        config = '--oem 3 --psm 6'
        text = pytesseract.image_to_string(Image.open(img_path), config=config)
        
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(text)
        
        print(f"✅ Page {i+1} complete: {len(text.strip())} characters")
        
        # Preview
        preview = text.strip()[:100]
        if preview:
            print(f"   Preview: {preview}...")
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
print("🎉 Done! Check /app/output for results")