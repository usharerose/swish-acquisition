"""
Utilities on S3 interaction
"""
import io
import logging
import json
from typing import Any, Dict, Optional

from minio import Minio, S3Error


logger = logging.getLogger(__name__)


def get_s3_client():
    endpoint = 'minio:9000'
    access_key = 'minioadmin'
    secret_key = 'minioadmin'
    return Minio(endpoint=endpoint, access_key=access_key, secret_key=secret_key, secure=False)


S3_CLIENT = get_s3_client()


def get_s3_object_data(bucket_name: str, object_name: str) -> Dict:
    """
    Commonly need the following keyword arguments,
    * bucket_name (str)
    * object_name (str)
    """
    response = None
    try:
        response = S3_CLIENT.get_object(bucket_name, object_name)
        data = json.loads(response.data.decode('utf-8'))
    finally:
        if response:
            response.close()
            response.release_conn()
    return data  # type: ignore[no-any-return]


class S3MixIn(object):

    BUCKET_NAME: Optional[str] = None
    OBJECT_NAME_PATTERN: str

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # NOQA
        self._validate_bucket_arguments()

    def _validate_bucket_arguments(self) -> None:
        for item in (self.BUCKET_NAME, self.OBJECT_NAME_PATTERN):
            if item is None:
                raise

    def upload_to_s3(self, data: Dict) -> None:
        content = json.dumps(data).encode('utf-8')
        b_data = io.BytesIO(content)
        data_length = len(content)

        try:
            S3_CLIENT.put_object(self.BUCKET_NAME, self.object_path, b_data,
                                 data_length, content_type='application/json')
        except S3Error:
            logger.exception('upload failed')
            raise

    @property
    def object_path(self) -> str:
        return self.OBJECT_NAME_PATTERN.format(**self.get_object_path_kwargs())

    def get_object_path_kwargs(self) -> Dict:
        raise NotImplementedError

    def get_object_data(self) -> Dict:
        if self.BUCKET_NAME is None:
            raise
        return get_s3_object_data(self.BUCKET_NAME, self.object_path)
