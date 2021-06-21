import importlib
import os
from itertools import chain


# Search for model files in api/<[app_name]>/models directory
MODEL_DIRECTORIES = [
    os.path.join(model_directory, "models")
    for model_directory in os.listdir(".")
    if os.path.isdir(os.path.join(model_directory, "models"))
]
EXCLUDE_FILES = ["__init__.py"]

# import all the models, so that alembic knows what to migrate
def import_models():
    model_directories = chain.from_iterable(os.walk(model_directory) for model_directory in MODEL_DIRECTORIES)
    for dir_path, dir_names, file_names in model_directories:
        for file_name in file_names:
            if file_name.endswith("py") and not file_name in EXCLUDE_FILES:
                file_path_wo_ext, _ = os.path.splitext((os.path.join(dir_path, file_name)))
                module_name = file_path_wo_ext.replace(os.sep, ".")
                importlib.import_module(module_name)
