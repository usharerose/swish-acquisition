"""
Basis components which can collect and store raw data
"""
import json
import logging
from typing import Dict, Protocol

from minio import S3Error


logger = logging.getLogger(__name__)


class EndpointCollectorProtocol(Protocol):

    # refer to S3MixIn::upload_to_s3
    def upload_to_s3(self, data: Dict) -> None: ...

    # refer to Endpoint::get_dict
    def get_dict(self, overwritten: bool = False) -> Dict: ...

    # refer to Endpoint::_set_data_dict
    def _set_data_dict(self, data_dict: Dict) -> None: ...

    # refer to S3MixIn::get_object_data
    def get_object_data(self) -> Dict: ...

    # refer to Endpoint::get_params
    def get_params(self) -> Dict: ...


class EndpointCollectorMixIn(object):

    def run(self: EndpointCollectorProtocol, overwritten: bool = False) -> None:
        msg_template = (f'{self.__class__.__name__} | '
                        f'{json.dumps(self.get_params())} | '
                        f'from %(source)s | '
                        f'SUCCESS')
        src_tag = 'REMOTE'
        if not overwritten:
            try:
                src_tag = 'LOCAL'
                obj_data = self.get_object_data()
                self._set_data_dict(obj_data)
                logger.info(msg_template % {'source': src_tag})
                return
            except S3Error:
                pass

        data = self.get_dict(overwritten)
        self.upload_to_s3(data)
        logger.info(msg_template % {'source': src_tag})
