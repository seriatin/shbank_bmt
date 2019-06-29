import os
import time

def create_export_dir(export_dir, model_name):

    def create_dir(path):
        if not os.path.exists(path):
            os.mkdir(path)

    _export_dir = os.path.join(export_dir, model_name)
    _path = ''

    for path in [export_dir, model_name]:
        _path = os.path.join(_path, path)
        create_dir(_path)
 
    return _export_dir

def concat_timestamp(export_dir):
    return os.path.join(export_dir, str(int(time.time())))


    
