from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
import compress
import encrypt
import split
import sy
import merge

app = Flask(__name__)

# 设置上传文件的保存目录
app.config['UPLOAD_FOLDER'] = 'static/upload'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# @app.route('/')
# def index():
#     return render_template('index_drag_drop.html')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compress')
def op_compress():
    return render_template('index_compress.html')

@app.route('/split')
def op_split():
    return render_template('index_split.html')

@app.route('/sy')
def op_sy():
    return render_template('index_sy.html')

@app.route('/merge')
def op_merge():
    return render_template('index_merge.html')

@app.route('/encrypt')
def op_encrypt():
    return render_template('index_encrypt.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    previous_page = request.referrer
    page = previous_page.split('/')
    operation = page[3]

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # return jsonify({'message': 'File successfully uploaded'})
        pdf_path = 'static/upload/' + filename
        if operation == 'compress':
            pdf_path = compress.pdfz(pdf_path, 100)
            obj = 'compress_source.pdf'
        elif operation == 'encrypt':
            encrypt.encryptPDF(pdf_path, '123456')
            obj = 'encrypt_source.pdf'
        elif operation == 'split':
            split.splitPDF(pdf_path)
            obj = 'archive.zip'
        elif operation == 'sy':
            pdf_path = sy.add_watermark(pdf_path, 'static/sy.pdf')
            obj = 'sy_source.pdf'
        return render_template('modern-viewer.html', pdf_path=pdf_path, obj=obj)
    else:
        return jsonify({'error': 'Invalid file format'})


@app.route('/uploadmerge', methods=['POST'])
def uploadmerge_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'merge/' + filename))
        # return jsonify({'message': 'File successfully uploaded'})
        
        return render_template('index_merge.html')

    else:
        return jsonify({'error': 'Invalid file format'})

@app.route('/mergeall')
def op_mergeall():
    merge.mergePDF()
    obj = 'merge.pdf'
    return render_template('modern-viewer.html', pdf_path='static/download/merge.pdf', obj=obj)
# @app.route('/pdf_viewer/<file_name>')
# def pdf_viewer(file_name):
#     return render_template('modern-viewer.html',pdf_path="static/upload/" + file_name)
#     # return render_template('modern-viewer.html')

if __name__ == '__main__':
    app.run(debug=True)
