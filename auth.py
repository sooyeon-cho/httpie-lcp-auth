#!/usr/bin/env python
from httpie.plugins import AuthPlugin

import generators

__version__ = '1.0.2'
__author__ = 'Ferdinand Cardoso'
__licence__ = 'GNU General Public License'


class LcpHmacAuth:
    def __init__(self, secret_identifier, secret_key):
        self.secret_identifier = secret_identifier
        self.secret_key = secret_key

    def __call__(self, r):
        if not self.secret_identifier or not self.secret_key:
            raise ValueError('Loyalty Commerce Platform secret identifier or key cannot be empty.')

        content_type = r.headers.get('content-type')
        if r.method in ['POST', 'PUT', 'PATCH']:
            content_type = 'application/json'
        auth_hdr_value = generators.generate_authorization_header_value(
            r.method,
            r.url,
            self.secret_identifier,
            self.secret_key,
            content_type,
            r.body)

        if content_type:
            r.headers['Content-Type'] = content_type
        r.headers['Authorization'] = auth_hdr_value
        return r


class LcpHmacAuthPlugin(AuthPlugin):

    name = 'Loyalty Commerce Platform token auth'
    auth_type = 'lcp-hmac'
    description = 'Sign requests using a Loyalty Commerce Platform authentication method'

    def get_auth(self, username=None, password=None):
        return LcpHmacAuth(username, password)