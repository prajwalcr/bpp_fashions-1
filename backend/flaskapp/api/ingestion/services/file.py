import os
from typing import Union

from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage


class FileService:
    """Service layer for handling file operations."""
    @classmethod
    def get_file_extension(cls, filename: str) -> Union[str, None]:
        """
        Extract the extension of a file from its name.

        Parameters
        ----------
        filename: str
            Name of the input file.

        Returns
        -------
        str
            Extension of the file if filename is valid.

        """
        if '.' in filename:
            return filename.rsplit('.', 1)[1]

    @classmethod
    def save_file(cls, save_dir: str, file: FileStorage) -> Union[str, None]:
        """

        Parameters
        ----------
        save_dir: str
            The path to the directory where files are saved.
        file: FileStorage
            Werkzeug datastructure representing the file to be saved.

        Returns
        -------
        str
            The path of the saved file, if save is successful.

        """

        if file and file.filename == '':
            return None

        # Secure the filename to prevent file injection attacks
        filename = secure_filename(file.filename)

        filepath = os.path.join(save_dir, filename)
        file.save(filepath)
        return filepath
