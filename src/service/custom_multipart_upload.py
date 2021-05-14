from pyexpat import ErrorString
from xml.etree.ElementTree import ParseError
from enum import Enum
from botocore.exceptions import ClientError
import logging
from botocore.response import StreamingBody


class Status(Enum):
    NOT_STARTED = 0
    ACTIVE = 1
    STOPPED = 2
    ALL_PARTS_UPLOADED = 3
    COMPLETED = 4
    ERROR = 5


class CustomMultipart:

    def __init__(self, client, bucket):
        self.__status = Status.NOT_STARTED
        self.__uploaded_parts = []
        self.__upload_id = None
        self.__key = None
        self.__iterator = 1
        self.__s3 = client
        self.__bucket = bucket

    def init_multipart_upload(self, key=None):
        self.__key = key

        try:
            response = self.__s3.create_multipart_upload(Bucket=self.__bucket, Key=self.__key)
            self.__upload_id = response.get('UploadId')
            self.__status = Status.ACTIVE
            logging.debug("multipart upload successfully initiated with id: %s" % self.__upload_id)
            return response
        except ClientError as e:
            self.__status = Status.ERROR
            logging.error("multipart upload initiation ended up with an error: %s" % e)
            return e

    def upload_next_chunk(self, chunk: StreamingBody):
        if self.__status == Status.ACTIVE:
            try:
                logging.debug("uploading part %s for %s" % (self.__iterator, self.__key))
                response = self.__s3.upload_part(Bucket=self.__bucket, Key=self.__key, PartNumber=self.__iterator,
                                          UploadId=self.__upload_id, Body=chunk.read())
                self.__uploaded_parts.append({
                    'PartNumber': self.__iterator,
                    'ETag': response.get('ETag')
                })
            except StopIteration as e:
                logging.debug("all parts were uploaded")
            except ClientError as e:
                self.__status = Status.ERROR
                logging.error("upload of a part of a file ended up with an error: %s" % e)
                return e
            else:
                logging.debug("part: %s was uploaded" % self.__iterator)
                self.__iterator = self.__iterator + 1
                return response

    def complete_upload(self):
        try:
            logging.debug("trying to complete multipart upload with id: %s" % self.__upload_id)
            parts_info = {'Parts': self.__uploaded_parts}
            response = self.__s3.complete_multipart_upload(Bucket=self.__bucket, Key=self.__key,
                                                           UploadId=self.__upload_id, MultipartUpload=parts_info)
            self.__status = Status.COMPLETED
            return response
        except ClientError as e:
            self.__status = Status.ERROR
            logging.error("an attempt to complete multipart upload ended up with an error: %s" % e)
            return e
        except ParseError as e:
            self.__status = Status.ERROR
            logging.error(": %s" % ErrorString(e.__dict__.get('code')))
            return e

    def stop_upload(self, **kwargs):
        kwargs.setdefault('Bucket', self.__bucket)
        kwargs.setdefault('Key', self.__key)
        kwargs.setdefault('UploadId', self.__upload_id)
        logging.debug("trying to stop multipart upload with id: %s" % self.__upload_id)
        try:
            response = self.__s3.abort_multipart_upload(**kwargs)
            self.__status = Status.STOPPED
            return response
        except ClientError as e:
            self.__status = Status.ERROR
            logging.error("an attempt to stop multipart upload ended up with an error: %s" % e)
            return e
        except Exception as e:
            return e

    def get_status(self):
        return self.__status