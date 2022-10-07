"""
Common functions
"""

import json


def get_message(client, config: dict) -> dict:
    """
    Receives and decodes messages

    Args:
        client:
        config: socket config

    Raises:
        ValueError: if was mistake during conversion
    """
    max_msg_length = config.get('max_bytes_for_msg')
    encoding = config.get('encoding')

    encoded_response = client.recv(max_msg_length)
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode(encoding)
        if isinstance(json_response, str):
            response = json.loads(json_response)
            if isinstance(response, dict):
                return response
            raise ValueError
        raise ValueError
    raise ValueError


def send_message(sock, message: dict, config: dict) -> None:
    """
    Encodes and sends a message

    Args:
        sock:
        message:
        config: socket config
    Raises:
        TypeError: if got wrong message
    """
    encoding = config.get('encoding')

    if not isinstance(message, dict):
        raise TypeError
    js_message = json.dumps(message)
    encoded_message = js_message.encode(encoding)
    sock.send(encoded_message)
