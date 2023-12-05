from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
import reportlab.pdfbase.ttfonts
 
 
# 创建水印信息
def create_watermark(content):
    """水印信息"""
    # 默认大小为21cm*29.7cm
    file_name = "mark.pdf"
    # 水印PDF页面大小
    c = canvas.Canvas(file_name, pagesize=(30 * cm, 30 * cm))
    # 移动坐标原点(坐标系左下为(0,0))
    c.translate(4 * cm, 0 * cm)
    # 设置字体格式与大小,中文需要加载能够显示中文的字体，否则就会乱码，注意字体路径
    
    c.setFont("Helvetica", 30)
    content = "watermark"
 
    # 旋转角度度,坐标系被旋转
    c.rotate(30)
    # 指定填充颜色
    c.setFillColorRGB(0, 0, 0)
    # 设置透明度,1为不透明
    c.setFillAlpha(0.05)
    # 画几个文本,注意坐标系旋转的影响
    c.drawString(0 * cm, 3 * cm, content)
    # 关闭并保存pdf文件
    c.save()
    return file_name
 
 
# 插入水印
def add_watermark(sor, pdf_file_mark):
    n = sor.split('/')
    obj = 'static/download/sy_' + n[2]
    pdf_output = PdfWriter()
    input_stream = open(sor, 'rb')
    pdf_input = PdfReader(input_stream, strict=False)
 
    # 获取PDF文件的页数
    pageNum = len(pdf_input.pages)
 
    # 读入水印pdf文件
    pdf_watermark = PdfReader(open(pdf_file_mark, 'rb'), strict=False)
    # 给每一页打水印
    for i in range(pageNum):
        page = pdf_input.pages[i]
        page.merge_page(pdf_watermark.pages[0])
        page.compress_content_streams()  # 压缩内容
        pdf_output.add_page(page)
    pdf_output.write(open(obj, 'wb'))
    return obj
 
