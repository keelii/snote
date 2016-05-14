from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config

class Upload():

    def __init__(self, access_key, secret_key, bucket_name):
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket_name = bucket_name

        self.auth = Auth(access_key, secret_key)

    def send_file(self, filename, local_file):
        self.token = self.auth.upload_token(self.bucket_name, filename, 3600)
        ret, info = put_file(self.token, filename, local_file)

        if info.status_code == 200 and not info.exception:
            return ret
        else:
            return None
