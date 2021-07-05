from uuid import uuid4

from app.models.configurations import Configurations
from app.wireguard.exc import RealmFullException

import app.context as ctx


def delete_first_expired():
    configurations = ctx.db.session.query(Configurations).all()
    expired = next((c for c in configurations if c.is_expired()), None)

    if not expired:
        raise RealmFullException

    ctx.db.session.query(Configurations).filter_by(username=expired.username).delete()


def assign_new_peer(username):
    new_peer = ""
    configs = ctx.db.session.query(Configurations).all()
    peers_names = [c.peer_name for c in configs]

    if not configs:
        new_peer = "peer1"
    else:
        for i in range(1, 254):
            peer_name = f"peer{i}"
            print(peer_name)
            if peer_name not in peers_names:
                new_peer = peer_name
                break

    config = Configurations(id=str(uuid4()), username=username, peer_name=new_peer)
    ctx.db.session.add(config)
    ctx.db.session.commit()

    return new_peer
