# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_client import settings
from polyaxon_client.exceptions import PolyaxonException


class ApiConfig(object):
    PAGE_SIZE = 20
    BASE_URL = "{}/api/{}"
    BASE_WS_URL = "{}/ws/{}"

    def __init__(self,
                 host=None,
                 http_port=None,
                 ws_port=None,
                 token=None,
                 version=None,
                 authentication_type=None,
                 use_https=None,
                 in_cluster=None,
                 reraise=False):

        self.token = token or settings.SECRET_TOKEN
        self.host = host or settings.API_HOST
        self.in_cluster = self._get_bool(in_cluster, settings.IN_CLUSTER)
        self.use_https = self._get_bool(use_https, settings.USE_HTTPS)

        if not all([self.host, self.token]) and not self.in_cluster:
            raise PolyaxonException(
                'Api config requires at least a host and a token if not running in-cluster.')

        self.http_port = http_port or settings.HTTP_PORT or (settings.DEFAULT_HTTPS_PORT
                                                             if self.use_https
                                                             else settings.DEFAULT_HTTP_PORT)
        self.ws_port = ws_port or settings.WS_PORT or (settings.DEFAULT_HTTPS_PORT
                                                       if self.use_https
                                                       else settings.DEFAULT_HTTP_PORT)
        self.version = version or settings.API_VERSION

        if self.in_cluster:
            if not settings.API_HTTP_HOST:
                print('Could get api host info, '
                      'please make sure this is running inside a polyaxon job.')
            self.http_host = settings.API_HTTP_HOST
            self.ws_host = settings.API_WS_HOST
        else:
            http_protocol = 'https' if self.use_https else 'http'
            ws_protocol = 'wss' if self.use_https else 'ws'
            self.http_host = '{}://{}:{}'.format(http_protocol, self.host, self.http_port)
            self.ws_host = '{}://{}:{}'.format(ws_protocol, self.host, self.ws_port)
        self.base_url = self.BASE_URL.format(self.http_host, self.version)
        self.base_ws_url = self.BASE_WS_URL.format(self.ws_host, self.version)
        self.authentication_type = authentication_type or settings.AUTHENTICATION_TYPE
        self.reraise = reraise

    @staticmethod
    def _get_bool(value, default_value):
        if isinstance(value, bool):
            return value

        return default_value
