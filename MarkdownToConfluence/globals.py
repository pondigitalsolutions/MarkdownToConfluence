import json
import os

FILELOCATION = os.environ.get('INPUT_FILESLOCATION')


def init(settings_path=""):
    global attachments, settings
    _is_init = False
    if (not _is_init):
        attachments = []
        _is_init = True

    if (settings_path == ""):
        if (FILELOCATION != None):
            try:
                settings = json.load(
                    open(os.path.join(FILELOCATION, 'settings.json')))
            except FileNotFoundError:
                settings = None
    else:
        settings = json.load(open(settings_path))


def reset():
    global attachments
    attachments = []
