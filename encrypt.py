from PyPDF2 import  PdfReader, PdfWriter 
def encryptPDF(sor, password):
    file_reader = PdfReader(sor)
    file_writer = PdfWriter()
    for page in range(len(file_reader.pages)):
        file_writer.add_page(file_reader.pages[page])

    file_writer.encrypt(password) # 设置密码
    n = sor.split('/')
    obj = 'static/download/encrypt_' + n[2]
    with open(obj, 'wb') as out:
        file_writer.write(out)
    return obj
