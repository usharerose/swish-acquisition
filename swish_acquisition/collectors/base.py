"""
Basis components which can collect and store raw data
"""
import logging
from typing import Dict, Optional, Protocol

from minio import S3Error


logger = logging.getLogger(__name__)


class EndpointCollectorProtocol(Protocol):

    # refer to S3MixIn::upload_to_s3
    def upload_to_s3(self, data: Dict) -> None: ...

    # refer to Endpoint::get_dict
    def get_dict(self, overwritten: bool = False) -> Optional[Dict]: ...

    # refer to Endpoint::data_dict
    @property
    def data_dict(self) -> Dict: ...

    @data_dict.setter
    def data_dict(self, data_dict: Dict) -> None: ...

    def get_object_data(self) -> Dict: ...


class EndpointCollectorMixIn(object):

    def run(self: EndpointCollectorProtocol, overwritten: bool = False) -> None:
        if not overwritten:
            try:
                data_dict = self.get_object_data()
                self.data_dict = data_dict
                logger.info('Endpoint.run | from local | success')
                return
            except S3Error:
                pass

        data = self.get_dict(overwritten)
        self.upload_to_s3(data)
        logger.info('Endpoint.run | from remote | success')
