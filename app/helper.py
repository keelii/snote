import os, glob
from flask import url_for
from flask.ext.login import current_user

# Helpers
def getNoteUrl(note):
    if note.public:
        return '/note/{0}'.format(note.id)
    else:
        return '/{0}/{1}'.format(current_user.nick_name, note.id)

def emptyDir(dir):
    files = glob.glob(os.path.join(dir, '*'))
    for f in files:
        print f
        os.remove(f)

class Helper():
    @staticmethod
    def init_app(app):
        @app.context_processor
        def utility_processor():
            return dict( getNoteUrl=getNoteUrl )
