import base64
import hashlib
import hmac
import logging
import os
import time
import urllib.parse
from builtins import str, object
from http.client import HTTP_PORT, HTTPS_PORT

logger = logging.getLogger(__name__)
DEFAULT_HASH_FUNCTION = hashlib.sha256


def generate_ext(content_type, body, hash_function=None):
    """Returns an `ext` value as described in
    `<http://tools.ietf.org/html/draft-ietf-oauth-v2-http-mac-02#section-3.1>`_.

    :param content_type: The content type of the request e.g. application/json.'
    :param body: The request body as a byte or Unicode string.
    :param hash_function: The hash function used on the content type & body.
    """
    hash_function = hash_function or DEFAULT_HASH_FUNCTION
    if content_type and body:
        # Hashing requires a bytestring, so we need to encode back to utf-8
        # in case the body/header have already been decoded to unicode (by the
        # python json module for instance)
        if isinstance(body, str):
            body = body.encode('utf-8')
        if isinstance(content_type, str):
            content_type = content_type.encode('utf-8')
        content_type_plus_body = content_type + body
        content_type_plus_body_hash = hash_function(content_type_plus_body)
        return content_type_plus_body_hash.hexdigest()
    return ""


def build_normalized_request_string(
        ts, nonce, http_method, host, port, request_path, ext):
    """Returns a normalized request string as described in
    `<http://tools.ietf.org/html/draft-ietf-oauth-v2-http-mac-02#section-3.2.1>`_.

    :param ts: The integer portion of a Unix epoch timestamp.
    :param nonce: A cryptographic nonce value.
    :param http_method: The HTTP method of the request e.g. `POST`.
    :param host: The host name of the server.
    :param port: The port of the server.
    :param request_path: The path portion of the request URL i.e. everything after the host and port.
    :param ext: An ext value computed from the request content type and body.
    """

    return '\n'.join(
        (ts, nonce, http_method, request_path, host, str(port), ext, '')).encode('utf-8')


def generate_nonce():
    """Returns a random string intend for use as a nonce when computing an
    HMAC.
    """
    return base64.b64encode(os.urandom(8)).decode()


def generate_signature(mac_key, normalized_request_string, hash_function=None):
    """Returns a request's signature given a normalized request string (a.k.a.
    a summary of the key elements of the request) and the MAC key (shared
    secret).

    The `mac_key` must match the key ID used to create the normalized request string.
    The `normalized_request_string` should be generated using
    :py:func:`build_normalized_request_string <pylcp.mac.build_normalized_request_string>`.

    :param mac_key: The MAC key to use to sign the request.
    :param normalized_request_string: Key elements of the request in a normalized form.
    :param hash_function: Hash function to be used in the signature. E.g. hashlib.sha1, hashlib.sha256
    """
    hash_function = hash_function or DEFAULT_HASH_FUNCTION
    key = base64.b64decode(mac_key.replace('-', '+').replace('_', '/') + '=')
    signature = hmac.new(key, normalized_request_string, hash_function)
    return base64.b64encode(signature.digest()).decode()


def generate_authorization_header_value(
        http_method,
        url,
        mac_key_identifier,
        mac_key,
        content_type,
        body,
        hash_function=None):
    """Returns a suitable value for the HTTP `Authorization` header that
    contains a valid signature for the request.

    :param http_method: The HTTP method of the request e.g. `POST`.
    :param url: The full URL of the request.
    :param mac_key_identifier: The ID of the MAC key to be used to sign the request
    :param mac_key: The MAC key to be used to sign the request
    :param content_type: The request content type.
    :param body: The request body as a byte or Unicde string.
    :param hash_function: Hash function passed to generate_ext & generate_signature, E.g. hashlib.sha1, hashlib.sha256
    """
    url_parts = urllib.parse.urlparse(url)
    port = url_parts.port
    if not port:
        port = str(HTTPS_PORT if url_parts.scheme == 'https' else HTTP_PORT)
    ts = str(int(time.time()))
    nonce = generate_nonce()
    ext = generate_ext(content_type, body, hash_function)
    normalized_request_string = build_normalized_request_string(
        ts,
        nonce,
        http_method,
        url_parts.hostname,
        port,
        url_parts.path,
        ext)

    signature = generate_signature(mac_key, normalized_request_string, hash_function)

    return 'MAC id="%s", ts="%s", nonce="%s", ext="%s", mac="%s"' % (
        mac_key_identifier,
        ts,
        nonce,
        ext,
        signature)


class AuthHeaderValue(object):
    """As per http://tools.ietf.org/html/draft-ietf-oauth-v2-http-mac-02 create
    the value for the HTTP Authorization header using an existing HMAC.
    """

    def __init__(self, mac_key_identifier, ts, nonce, ext, mac):
        self.mac_key_identifier = mac_key_identifier
        self.ts = ts
        self.nonce = nonce
        self.ext = ext
        self.mac = mac

    def __str__(self):
        return (
            'MAC id="{self.mac_key_identifier}", ts="{self.ts}", '
            'nonce="{self.nonce}", ext="{self.ext}", mac="{self.mac}"'
        ).format(self=self)
