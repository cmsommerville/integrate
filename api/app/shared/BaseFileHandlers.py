import os
import datetime
import pandas as pd
from flask import request
from werkzeug.utils import secure_filename
from typing import Set, Tuple

__FILE_READERS = {
    'txt': pd.read_csv, 
    'csv': pd.read_csv, 
    'xlsx': pd.read_excel, 
    'xls': pd.read_excel
}

class NoFileProvidedException(Exception):
    pass


def _allowed_file(filename: str, allowed_extensions: Set, *args, **kwargs):
    extension = filename.rsplit('.', 1)[1].lower()
    return '.' in filename and extension in allowed_extensions, extension

def upload_file(
    req: request, 
    filepath: str, 
    allowed_extensions: Set = set(__FILE_READERS.keys()), 
    *args, **kwargs) -> Tuple[pd.DataFrame, str]:

    # check if the post request has the file part
    if 'file' not in req.files:
        raise NoFileProvidedException(f"No file provided in request")
    file = request.files['file']

    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        raise NoFileProvidedException(f"No file provided in request")
 
    if not file: 
        raise Exception("Improper file")
        
    allowed_extension, extension = _allowed_file(file.filename, allowed_extensions)
    if not allowed_extension:
        raise Exception(f"File is not of proper type. Please upload a file of the following types: {', '.join(allowed_extensions)}")
    
    # append timestamp to filename and secure it
    now = datetime.datetime.now() 
    filename = secure_filename(now.strftime("%Y%m%d-%H%M%S-") + file.filename)

    # read data into pandas dataframee
    df = __FILE_READERS.get(extension.lower())(file, **kwargs)

    # save file to local storage
    # must come after reading file
    try: 
        full_filename = os.path.join(filepath, filename)
        file.save(full_filename)
    except Exception as e: 
        raise Exception(f"Could not save file to path: {filepath}")
    
    return df, full_filename
