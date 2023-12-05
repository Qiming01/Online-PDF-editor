from PyPDF2 import  PdfReader, PdfWriter 
import zipfile
import os
import shutil

# getNumPages() 获取总页数
def splitPDF(sor):
    obj = sor.split(".")
    n = obj[0].split('/')
    obj = 'static/download/files_to_zip/split_' + n[2]
    file_reader = PdfReader(sor)
    for page in range(len(file_reader.pages)):
        # 实例化对象len
        file_writer = PdfWriter()
        # 将遍历的每一页添加到实例化对象中
        file_writer.add_page(file_reader.pages[page])
        with open(obj + str(page + 1) + ".pdf", 'wb') as out:
            file_writer.write(out)
    generate_zip_file()
    empty_folder('static/download/files_to_zip/')

def empty_folder(folder_path):
    try:
        # 清空文件夹
        shutil.rmtree(folder_path)
        # 重新创建空文件夹
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' successfully emptied.")
    except Exception as e:
        print(f"Error: {e}")

def generate_zip_file():
    # 生成压缩包的函数
    folder_path = 'static/download/files_to_zip'
    zip_file_path = 'static/download/archive.zip'

    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname=arcname)