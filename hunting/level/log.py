import json

from hunting.constants import *


class LevelLog:
    def __init__(self):
        self._log = []

    @property
    def events(self):
        return self._log

    def log_begin_item_use(self, oid, user_oid, target):
        self._log.append({
            EVENT_TYPE: BEGIN_ITEM_USE,
            OBJ_ID: oid,
            USER_ID: user_oid,
            TARGET: target
        })

    def log_end_item_use(self, oid):
        self._log.append({
            EVENT_TYPE: END_ITEM_USE,
            OBJ_ID: oid
        })

    def log_begin_turn(self, oid):
        self._log.append({
            EVENT_TYPE: BEGIN_TURN_EVENT,
            OBJ_ID: oid
        })

    def log_end_turn(self, oid):
        self._log.append({
            EVENT_TYPE: END_TURN_EVENT,
            OBJ_ID: oid
        })

    def log_movement(self, oid, x0, y0, x1, y1):
        self._log.append({
            EVENT_TYPE: MOVEMENT_EVENT,
            OBJ_ID: oid,
            MOVEMENT_PREV_X: x0,
            MOVEMENT_PREV_Y: y0,
            OBJ_X: x1,
            OBJ_Y: y1
        })

    def log_attack(self, attacker_oid, defender_oid, base_accuracy, accuracy_roll, dodge, base_damage):
        self._log.append({
            EVENT_TYPE: ATTACK_EVENT,
            ATTACK_ATTACKER_ID: attacker_oid,
            ATTACK_DEFENDER_ID: defender_oid,
            ATTACK_BASE_ACCURACY: base_accuracy,
            D100_RESULT: accuracy_roll,
            ATTACK_DODGE: dodge,
            ATTACK_BASE_DAMAGE: base_damage
        })

    def log_take_damage(self, oid, damage):
        self._log.append({
            EVENT_TYPE: TAKE_DAMAGE_EVENT,
            "object_id": oid,
            "damage": damage
        })

    def log_change_effect(self, event_type, oid, effect):
        msg = {
            EVENT_TYPE: event_type,
            OBJ_ID: oid,
            EFFECT_TYPE: effect.effect_type
        }
        if effect.effect_type == EFFECT_TYPE_PROPERTY:
            msg.update({
                PROPERTY_TYPE: effect.property_type,
                VALUE: effect.value
            })
            self._log.append(msg)
        else:
            raise ValueError("Don't know how to log non-property effects!")

    def log_apply_effect(self, oid, effect):
        self.log_change_effect(APPLY_EFFECT_EVENT, oid, effect)

    def log_remove_effect(self, oid, effect):
        self.log_change_effect(REMOVE_EFFECT_EVENT, oid, effect)

    def log_destruction(self, oid, x, y):
        self._log.append({
            EVENT_TYPE: OBJECT_DESTRUCTION_EVENT,
            OBJ_ID: oid,
            OBJ_X: x,
            OBJ_Y: y
        })

    def to_json_string(self):
        return json.dumps(self._log)