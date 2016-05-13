from flask import current_app
from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config

class Upload():
    access_key = current_app.config['QN_ACCESS_KEY']
    secret_key = current_app.config['QN_SECRET_KEY']
    bucket_name = current_app.config['QN_BUCKET_NAME']

    def __init__(self, filename, local_file):
        self.filename = filename
        self.local_file = local_file

        self.getToken()

    def getToken(self):
        q = Auth(Upload.access_key, Upload.secret_key)
        self.token = q.upload_token(Upload.bucket_name, self.filename, 3600)

        return self.token

    def send_file(self):
        ret, info = put_file(self.token, self.filename, self.local_file)

        if info.status_code == 200 and not info.exception:
            return ret
        else:
            return None
