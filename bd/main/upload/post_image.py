from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

__FILEPATH__ = os.path.dirname((os.path.dirname(os.path.abspath(__file__))))
DEDICACE_FOLDER = os.path.join(__FILEPATH__, 'static/main/images/dedicaces')
EXLIBRIS_FOLDER = os.path.join(__FILEPATH__, 'static/main/images/exlibris')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['DEDICACE_FOLDER'] = DEDICACE_FOLDER
app.config['EXLIBRIS_FOLDER'] = EXLIBRIS_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/dedicace', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['DEDICACE_FOLDER'], filename))
        return jsonify({'message': 'File uploaded successfully'})

    return jsonify({'error': 'File type not allowed'})


if __name__ == '__main__':
    app.run()
