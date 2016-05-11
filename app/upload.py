from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config

class Upload():
    access_key = 'QoaeymVy9SxXAUdHx3yu5SvPv8YpLo-fIscAUFYa'
    secret_key = 'LPGQZxANjAokEJ4vOAinLFy0EkPeU5pxinPUyr27'
    bucket_name = 'keelii'

    def __init__(self, filename, local_file):
        self.filename = filename
        self.local_file = local_file

    def getToken(self):
        q = Auth(Upload.access_key, Upload.secret_key)
        self.token = q.upload_token(Upload.bucket_name, self.filename, 3600)

        return self.token

    def set_file(self):
        ret, info = put_file(self.token, self.filename, self.local_file)

        if info.status_code == 200 and not info.exception:
            return ret
        else:
            return None
