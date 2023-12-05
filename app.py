from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
import compress
import encrypt
import split
import addWatermark
import merge

app = Flask(__name__)

# 设置上传文件的保存目录
app.config['UPLOAD_FOLDER'] = 'static/upload'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

# 允许上传的文件格式
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# home page
@app.route('/')
def index():
    return render_template('index.html')

# 压缩pdf
@app.route('/compress')
def op_compress():
    return render_template('index_compress.html')

# 分割pdf
@app.route('/split')
def op_split():
    return render_template('index_split.html')

# 添加水印
@app.route('/watermark')
def op_watermark():
    return render_template('index_watermark.html')

# 合并pdf
@app.route('/merge')
def op_merge():
    return render_template('index_merge.html')

# 加密pdf
@app.route('/encrypt')
def op_encrypt():
    return render_template('index_encrypt.html')

# 批注pdf
@app.route('/view')
def op_view():
    return render_template('index_view.html')


# 上传文件
@app.route('/upload', methods=['POST'])
def upload_file():
    previous_page = request.referrer

    page = previous_page.split('/')
    operation = page[3]

    # 检查是否有文件
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']

    # 检查是否选择了文件
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # 检查文件格式通过
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        pdf_path = 'static/upload/' + filename
        if operation == 'compress':
            pdf_path = compress.pdfz(pdf_path, 100)
            obj = 'compress_' + filename
            return render_template('compress.html', pdf_path=pdf_path, obj=obj)
        elif operation == 'split':
            split.splitPDF(pdf_path)
            obj = 'archive.zip'
            return render_template('split.html', pdf_path=pdf_path, obj=obj)
        # elif operation == 'watermark':
        #     addWatermark.addWatermark("qiming", pdf_path, fontFamily="Helvetica", fontSize=60)
        #     obj = 'Watermarked.pdf'
        #     return render_template('watermark.html', pdf_path="static/download/Watermarked.pdf", obj=obj)
        elif operation == 'view':
            return render_template('view.html', pdf_path=pdf_path)
    else:
        return jsonify({'error': 'Invalid file format'})

@app.route('/upload-encrypt', methods=['POST'])
def encrypt_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    password = request.form['password']
    

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'encrypt' + filename))
        pdf_path = 'static/upload/encrypt' + filename
        encrypt.encryptPDF(pdf_path, password)
        obj = 'encrypt' + filename
        return render_template('encrypt.html', pdf_path=pdf_path, obj=obj)

    else:
        return jsonify({'error': 'Invalid file format'})
    
@app.route('/upload-watermark', methods=['POST'])
def addwatermark():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    text = request.form['textInput']
    fontFamily = request.form['fontFamily']
    fontSize = int(request.form['fontSize'])
    print(text)
    print(fontFamily)
    print(fontSize)
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        pdf_path = 'static/upload/' + filename
        addWatermark.addWatermark(text, pdf_path, fontFamily, fontSize)
        obj = 'Watermarked.pdf'
        return render_template('watermark.html', pdf_path="static/download/Watermarked.pdf", obj=obj)

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
    return render_template('merge.html', pdf_path='static/download/merge.pdf', obj=obj)

if __name__ == '__main__':
    app.run(debug=True)
