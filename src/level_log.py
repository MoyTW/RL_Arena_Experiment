import json

EVENT_TYPE = 'event_type'

BEGIN_TURN = 'begin turn'
MOVEMENT_EVENT = 'movement'
ATTACK_EVENT = 'attack'
TAKE_DAMAGE_EVENT = 'take damage'


class LevelLog:
    def __init__(self):
        self._log = []

    def log_begin_turn(self, oid):
        self._log.append({BEGIN_TURN: oid})

    def log_movement(self, oid, x, y):
        self._log.append({
            "event_type": MOVEMENT_EVENT,
            "object_id": oid,
            "x": x,
            "y": y
        })

    def log_attack(self, attacker_oid, defender_oid):
        self._log.append({
            EVENT_TYPE: ATTACK_EVENT,
            "attacker_object_id": attacker_oid,
            "defender_object_id": defender_oid
        })

    def log_take_damage(self, oid, damage):
        self._log.append({
            EVENT_TYPE: TAKE_DAMAGE_EVENT,
            "object_id": oid,
            "damage": damage
        })

    def to_json_string(self):
        return json.dumps(self._log)