import PyPDF2
import os
import shutil

def list_files(folder_path):
    file_list = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_list.append(file_path)

    return file_list

def mergePDF():
    filenames = list_files('static/upload/merge')
    merger=PyPDF2.PdfMerger()
    for filename in filenames:
        merger.append(PyPDF2.PdfReader(filename))
    merger.write('static/download/merge.pdf')
    empty_folder('static/upload/merge')
    

def empty_folder(folder_path):
    try:
        # 清空文件夹
        shutil.rmtree(folder_path)
        # 重新创建空文件夹
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' successfully emptied.")
    except Exception as e:
        print(f"Error: {e}")


