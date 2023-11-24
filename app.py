from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# 设置上传文件的保存目录
app.config['UPLOAD_FOLDER'] = 'static'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index_drag_drop.html')

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
        pdf_path = 'static/' + filename
        return render_template('viewer.html', pdf_path=pdf_path)
    else:
        return jsonify({'error': 'Invalid file format'})

@app.route('/pdf_viewer/<path>')
def pdf_viewer(path):
    pdf_path = 'static/' + path + '.pdf'
    return render_template('viewer.html', pdf_path=pdf_path)

if __name__ == '__main__':
    app.run(debug=True)
