import fitz  # PyMuPDF
import os
from PIL import Image
import io

def is_image_black(image):
    """
    بررسی می‌کند که آیا تمام پیکسل‌های یک تصویر سیاه هستند یا خیر.
    """
    # تبدیل تصویر به حالت RGB یا L (Grayscale)
    image = image.convert("RGB")  # اگر مطمئن هستید تصویر grayscale است، از "L" استفاده کنید
    # دسترسی به داده‌های تصویر به صورت لیست پیکسل‌ها
    pixels = list(image.getdata())
    # بررسی می‌کند که آیا تمام پیکسل‌ها سیاه هستند
    black_pixel = (0, 0, 0)
    return all(pixel == black_pixel for pixel in pixels)

def extract_images_from_pdf(pdf_path, output_dir):
    # Open the PDF file
    doc = fitz.open(pdf_path)
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]

    # Iterate through each page
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        image_list = page.get_images()

        if not image_list:
            continue

        # Skip the first image on each page
        for img_index, img in enumerate(image_list, start=1):
            if img_index == 1:
                continue

            xref = img[0]
            base_image = doc.extract_image(xref)
            img_data = base_image["image"]
            img_ext = base_image["ext"]

            # Create an image object
            image = Image.open(io.BytesIO(img_data))

            # Check if the image is completely black
            if is_image_black(image):
                # print(f"Image {img_index - 1} on page {page_num + 1} is completely black. Skipping...")

                continue


            # Define image filename
            img_filename = f"{base_name}-{page_num + 1}-{img_index - 1}.{img_ext}"
            img_path = os.path.join(output_dir, img_filename)

            # Save the image
            image.save(img_path, format=img_ext)

def main():
    pdf_files = ["PDF/موتور.pdf"]
    output_dir = "images/موتور"

    os.makedirs(output_dir, exist_ok=True)

    for pdf_file in pdf_files:
        extract_images_from_pdf(pdf_file, output_dir)

if __name__ == "__main__":
    main()
