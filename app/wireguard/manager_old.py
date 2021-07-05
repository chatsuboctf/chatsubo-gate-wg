import os

import jinja2
import wgconfig
from wgconfig import wgexec

from app.models.configurations import Configurations


class WireguardManager_old:
    def __init__(self, home, config_file, pubkey, server_addr, server_port, dns_server, allowed_ips):
        self.home = home
        self.config_file = config_file
        self.config = os.path.abspath(os.path.join(home, config_file))
        self.pubkey = pubkey
        self.server_port = server_port
        self.server_addr = server_addr
        self.dns_server = dns_server
        self.allowed_ips = allowed_ips
        self.wgconfig = wgconfig.WGConfig(self.home)

    @classmethod
    def from_config(cls, config):
        return cls(config["home"], config["config_file"], config["public_key"], config["server"]["address"], config["server"]["port"], config["dns_server"], config["allowed_ips"])

    def add_peer(self, username):
        print(username)
        params = {
            "private_key": "",
            "dns_server": self.dns_server,
            "public_key": self.pubkey,
            "server_url": self.server_addr,
            "server_port": self.server_port,
            "allowed_ips": self.allowed_ips,
        }

        pkey = wgexec.generate_privatekey()
        self.wgconfig.add_peer(pkey)
        self.wgconfig.write_file()
        self.wgconfig.read_file()
        print(self.wgconfig.peers)
        return None

        tpl_env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="/"))

        template = tpl_env.get_template("app/templates/peer.j2")

        params["private_key"] = pkey
        config_content = template.render(params)
        config = Configurations(username=username, config=config_content)

        return config
