# def upload(self, file_data, key):
#     """通过二进制流上传文件 :param file_data: 二进制数据 :param key: key :return: """
#     try:
#         token = self.auth.upload_token(QINIU_DEFAULT_BUCKET)
#         ret, info = put_data(token, key, file_data)
#     except Exception as e:
#         logging.error("upload error, key: {0}, exception: {1}" .format(key, e))
#     if info.status_code == 200:
#         logging.info("upload data to qiniu ok, key: {0}".format(key))
#         return True
#     else:
#         logging.error("upload data to qiniu error, key: {0}".format(key))
#         return False
#
#
