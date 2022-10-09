"""
Module with AbstractSocket class
"""
import json

from usefull_stuff.messanger.common.config_mixin import ConfigMixin


class AbstractSocket(ConfigMixin):
    """
    Abstract class containing common logic for SocketType objects
    """
    def __init__(self):
        self._config = self.get_config()

    def get_message(self, client) -> dict:
        """
        Receives and decodes messages

        Args:
            client: socket file descriptor representing the connection

        Raises:
            ValueError: if was mistake during conversion
        """

        encoding = self._config.get('encoding', 'utf-8')
        max_msg_length = self._config.get('max_bytes_for_msg', '1024')

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

    def send_message(self, sock, message: dict) -> None:
        """
        Encodes and sends a message

        Args:
            sock:
            message:
        Raises:
            TypeError: if got wrong message
        """
        encoding = self._config.get('encoding', 'utf-8')

        if not isinstance(message, dict):
            raise TypeError
        js_message = json.dumps(message)
        encoded_message = js_message.encode(encoding)
        sock.send(encoded_message)
