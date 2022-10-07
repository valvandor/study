"""
Common functions
"""

import json
from common.variables import MAX_PACKAGE_LENGTH, ENCODING


def get_message(client) -> dict:
    """
    Receives and decodes messages

    Args:
        client:

    Raises:
        ValueError: if was mistake during conversion
    """

    encoded_response = client.recv(MAX_PACKAGE_LENGTH)
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode(ENCODING)
        if isinstance(json_response, str):
            response = json.loads(json_response)
            if isinstance(response, dict):
                return response
            raise ValueError
        raise ValueError
    raise ValueError


def send_message(sock, message: dict) -> None:
    """
    Encodes and sends a message

    Args:
         sock:
         message:
    Raises:
        TypeError: if got wrong message
    """
    if not isinstance(message, dict):
        raise TypeError
    js_message = json.dumps(message)
    encoded_message = js_message.encode(ENCODING)
    sock.send(encoded_message)
