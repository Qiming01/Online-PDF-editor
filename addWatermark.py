from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from PyPDF2 import PdfReader, PdfWriter

def makeWatermark(text, fontFamily, fontSize):
    pdf = canvas.Canvas("static/upload/watermark.pdf", pagesize=A4)
    pdf.translate(inch, inch)
    pdf.setFillColor(colors.grey, alpha=0.6)
    pdf.setFont(fontFamily, fontSize)
    pdf.rotate(45)
    pdf.drawCentredString(400, 100, text)
    pdf.save()

def makepdf(pdf_file):
    watermark = 'static/upload/watermark.pdf'
    merged = "static/download/Watermarked.pdf"

    with open(pdf_file, "rb") as input_file, open(watermark, "rb") as watermark_file:
        input_pdf = PdfReader(input_file)
        watermark_pdf = PdfReader(watermark_file)
        watermark_page = watermark_pdf.pages[0]
        output = PdfWriter()

        for i in range(len(input_pdf.pages)):
            pdf_page = input_pdf.pages[i]
            pdf_page.merge_page(watermark_page)
            output.add_page(pdf_page)

        with open(merged, "wb") as merged_file:
            output.write(merged_file)


def addWatermark(text, pdf_file, fontFamily="Helvetica", fontSize=60):
    makeWatermark(text, fontFamily, fontSize)
    # print("watermark.pdf created")
    makepdf(pdf_file)