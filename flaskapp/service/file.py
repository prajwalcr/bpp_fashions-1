import os

from werkzeug.utils import secure_filename


class FileService:
    @classmethod
    def get_file_extension(cls, filename):
        if '.' in filename:
            return filename.rsplit('.', 1)[1]

    @classmethod
    def save_file(cls, save_dir, file):
        if file and file.filename == '':
            return None

        filename = secure_filename(file.filename)
        filepath = os.path.join(save_dir, filename)
        file.save(filepath)
        return filepath
