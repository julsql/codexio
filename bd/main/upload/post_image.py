from flask import Flask, request, jsonify
import os

app = Flask(__name__)

__FILEPATH__ = os.path.dirname((os.path.dirname(os.path.abspath(__file__))))
DEDICACE_FOLDER = os.path.join(__FILEPATH__, 'static/main/images/dedicaces')
EXLIBRIS_FOLDER = os.path.join(__FILEPATH__, 'static/main/images/exlibris')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['DEDICACE_FOLDER'] = DEDICACE_FOLDER
app.config['EXLIBRIS_FOLDER'] = EXLIBRIS_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/dedicace/<isbn>', methods=['POST'])
def upload_dedicace(isbn):
    return upload(isbn, app.config['DEDICACE_FOLDER'])


@app.route('/exlibris/<isbn>', methods=['POST'])
def upload_exlibris(isbn):
    return upload(isbn, app.config['EXLIBRIS_FOLDER'])


def upload(isbn, origin_folder):
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and allowed_file(file.filename):
        # filename = secure_filename(file.filename)
        extension = file.filename.rsplit('.', 1)[1]
        path_folder = os.path.join(origin_folder, isbn)
        if not os.path.exists(path_folder):
            print(path_folder)
            os.makedirs(path_folder)
            number = 1
        else:
            number = count_files_in_directory(path_folder) + 1

        filename = f"{number}.{extension}"
        file.save(os.path.join(path_folder, filename))
        return jsonify({'message': 'File uploaded successfully'})

    return jsonify({'error': 'File type not allowed'})


def count_files_in_directory(directory_path):
    if not os.path.isdir(directory_path):
        return 0
    file_count = 0
    for root, dirs, files in os.walk(directory_path):
        file_count += len(files)

    return file_count


if __name__ == '__main__':
    app.run()
