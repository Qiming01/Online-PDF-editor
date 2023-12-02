from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# 设置上传文件的保存目录
app.config['UPLOAD_FOLDER'] = 'static/upload'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index_compress.html')

@app.route('/upload', methods=['POST'])
def upload_file():
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
        return render_template('modern-viewer.html', pdf_path=pdf_path)
    else:
        return jsonify({'error': 'Invalid file format'})

@app.route('/<file_name>')
def pdf_viewer(file_name):
    return render_template('modern-viewer.html',pdf_path="static/upload/" + file_name)
    # return render_template('modern-viewer.html')

# @app.route('/viewer')
# def pdf_viewer():
#     return render_template('modern-viewer.html',pdf_path="static/upload/document.pdf")
#     # return render_template('modern-viewer.html')

if __name__ == '__main__':
    app.run(debug=True)
