import pymupdf
import os

pdf_path = "docs/DrD_Project_Report.pdf"
out_dir = "docs/pdf_previews"
os.makedirs(out_dir, exist_ok=True)

doc = pymupdf.open(pdf_path)
print(f"Total PDF pages: {len(doc)}")

for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=150)
    img_name = f"{out_dir}/page_{i+1:02d}.png"
    pix.save(img_name)
    print(f"Rendered Page {i+1} -> {img_name}")

print("Visual verification render complete!")
