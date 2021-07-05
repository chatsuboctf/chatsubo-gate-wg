from datetime import datetime, timedelta

from flask import current_app
from flask_restx import Resource

from app.api import vpn_api
from app.helpers.api_response import VpnAccessApiResponse

import app.context as ctx
from app.helpers.auth import require_auth
from app.helpers.configurations import delete_first_expired, assign_new_peer
from app.models.configurations import Configurations
from app.wireguard.exc import RealmFullException
from app.wireguard.manager import WireguardManager


@vpn_api.route('/get/<string:username>')
class List(Resource):

    @require_auth
    def get(self, username):
        res = VpnAccessApiResponse()
        wg = WireguardManager(current_app.config.get("clients", "./clients"))

        cached = ctx.db.session.query(Configurations).filter_by(username=username).first()
        if cached:
            res.config = wg.read(cached.peer_name)
            return res.make()

        peers_qty = ctx.db.session.query(Configurations).count()
        if peers_qty == 254:
            try:
                delete_first_expired()
            except RealmFullException:
                res.add_error("Realm is full")
                return res.make()

        # wg = WireguardManager.from_config(current_app.config["wg"])

        new_peer_name = assign_new_peer(username)
        res.config = wg.read(new_peer_name)

        return res.make()
