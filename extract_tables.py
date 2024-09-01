import fitz  # PyMuPDF
import cv2
import numpy as np
import os

# بارگذاری فایل PDF
pdf_document = "PDF/برق خودرو.pdf"
doc = fitz.open(pdf_document)

# ایجاد پوشه برای ذخیره تصاویر جداول (در صورت عدم وجود پوشه)
output_folder = 'extracted_tables'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

table_count = 0

# پیمایش صفحات PDF
for page_num in range(len(doc)):
    page = doc.load_page(page_num)
    pix = page.get_pixmap()

    # تبدیل کل صفحه به تصویر
    img_cv = np.array(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    img_cv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

    # اعمال Threshold برای باینری کردن تصویر
    _, img_bin = cv2.threshold(img_cv, 150, 255, cv2.THRESH_BINARY_INV)

    # تشخیص خطوط افقی و عمودی
    kernel_length = np.array(img_cv).shape[1]//100

    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length))
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

    # تشخیص خطوط عمودی
    img_temp1 = cv2.erode(img_bin, vertical_kernel, iterations=3)
    vertical_lines_img = cv2.dilate(img_temp1, vertical_kernel, iterations=3)

    # تشخیص خطوط افقی
    img_temp2 = cv2.erode(img_bin, horizontal_kernel, iterations=3)
    horizontal_lines_img = cv2.dilate(img_temp2, horizontal_kernel, iterations=3)

    # ترکیب خطوط افقی و عمودی
    table_mask = cv2.addWeighted(vertical_lines_img, 0.5, horizontal_lines_img, 0.5, 0.0)
    table_mask = cv2.erode(~table_mask, kernel, iterations=2)
    _, table_mask = cv2.threshold(table_mask, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # یافتن کانتورهای جداول
    contours, _ = cv2.findContours(table_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # استخراج و ذخیره جداول
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w > 50 and h > 50:  # فیلتر کردن جداول کوچک
            table_image = img_cv[y:y+h, x:x+w]
            output_path = os.path.join(output_folder, f'table_page_{page_num+1}_{table_count+1}.png')
            cv2.imwrite(output_path, table_image)
            table_count += 1

print(f"جداول با موفقیت استخراج شدند و {table_count} جدول در پوشه 'extracted_tables' ذخیره شدند.")
