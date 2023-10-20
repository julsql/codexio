from flask import Flask, request, jsonify
import os
import re

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
            os.makedirs(path_folder)
            number = 1
        else:
            number = get_next_number(path_folder)

        filename = f"{number}.{extension}"
        file.save(os.path.join(path_folder, filename))
        return jsonify({'message': 'File uploaded successfully'})

    return jsonify({'error': 'File type not allowed'})


def get_next_number(directory_path):
    if not os.path.isdir(directory_path):
        return []

    image_paths = []
    allowed_image_extensions = ".jpeg"

    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_extension = os.path.splitext(file)[1].lower()
            if file_extension == allowed_image_extensions:
                image_path = os.path.join(root, file)
                image_paths.append(image_path)

    integers = [int(re.search(r'\d+', s).group()) for s in image_paths if re.search(r'\d+', s)]
    integers.sort()

    missing_integer = 1
    for num in integers:
        if num == missing_integer:
            missing_integer += 1
        elif num > missing_integer:
            break

    return missing_integer


if __name__ == '__main__':
    app.run()
