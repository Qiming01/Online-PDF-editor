import fitz
import os


def covert2pic(doc, zoom, totaling):
    
    if os.path.exists('.pdf'):       # 临时文件，需为空
         os.removedirs('.pdf')
    os.mkdir('.pdf')
    for pg in range(totaling):
        page = doc[pg]
        zoom = int(zoom)            #值越大，分辨率越高，文件越清晰
        rotate = int(0)
        print(page)
        trans = fitz.Matrix(zoom / 100.0, zoom / 100.0).prerotate(rotate)
        pm = page.get_pixmap(matrix=trans, alpha=False)
      
        lurl='.pdf/%s.jpg' % str(pg+1)
        pm.save(lurl)
    doc.close()

def pic2pdf(obj, totaling):
    doc = fitz.open()
    for pg in range(totaling):
        img = '.pdf/%s.jpg' % str(pg+1)
        imgdoc = fitz.open(img)                 # 打开图片
        pdfbytes = imgdoc.convert_to_pdf()        # 使用图片创建单页的 PDF
        os.remove(img)  
        imgpdf = fitz.open("pdf", pdfbytes)
        doc.insert_pdf(imgpdf)                   # 将当前页插入文档
    if os.path.exists(obj):         # 若文件存在先删除
        os.remove(obj)
    doc.save(obj)                   # 保存pdf文件
    doc.close()


def pdfz(sor, zoom): 
    doc = fitz.open(sor)
    totaling = doc.page_count
    covert2pic(doc, zoom, totaling)
    n = sor.split('/')
    obj = 'static/download/compress_' + n[2]
    pic2pdf(obj, totaling)
    os.removedirs('.pdf')
    return obj
