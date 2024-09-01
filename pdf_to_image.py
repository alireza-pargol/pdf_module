import fitz  # PyMuPDF
import os


def pdf_to_images(pdf_path, output_folder):
    # بررسی وجود پوشه خروجی و ایجاد آن در صورت عدم وجود
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # باز کردن فایل PDF
    pdf_document = fitz.open(pdf_path)

    # پیمایش در صفحات PDF
    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)

        # تبدیل صفحه به تصویر
        pix = page.get_pixmap()

        # تعیین نام فایل تصویر
        image_filename = os.path.join(output_folder, f'page_{page_number + 1}.png')

        # ذخیره تصویر
        pix.save(image_filename)
        print(f'Saved: {image_filename}')

    # بستن فایل PDF
    pdf_document.close()


# تنظیم مسیر فایل PDF و پوشه خروجی
pdf_path = 'PDF/سیستم سوخت رسانی.pdf'
output_folder = 'سیستم سوخت رسانی'

# اجرای تابع تبدیل PDF به تصاویر
pdf_to_images(pdf_path, output_folder)
