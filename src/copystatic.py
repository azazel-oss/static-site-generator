import os
import shutil


def copy_folder(source_path, destination_path):
    if not os.path.exists(source_path):
        return
    if os.path.exists(destination_path):
        shutil.rmtree(destination_path)
    os.mkdir(destination_path)
    for item in os.listdir(path=source_path):
        if os.path.isfile(os.path.join(source_path, item)):
            shutil.copy(os.path.join(source_path, item), destination_path)
        else:
            copy_folder(
                os.path.join(source_path, item), os.path.join(destination_path, item)
            )
