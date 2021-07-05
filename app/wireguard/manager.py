import os

from app.models.configurations import Configurations


class WireguardManager:
    def __init__(self, clients_dir):
        self.clients_dir = os.path.abspath(clients_dir)

    def read(self, peer_name):
        with open(f"{self.clients_dir}/{peer_name}/{peer_name}.conf") as f:
            return f.read()

    def add_peer(self, username):
        config = Configurations(username=username)
        # find unused peer_name
        # register it

        return config
