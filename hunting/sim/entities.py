import math

from hunting.level.log import LevelLog
import hunting.constants as c
import hunting.utils as utils


class GameObject(object):
    def __init__(self, oid, log: LevelLog, x, y, name, faction=None, blocks=False, inventory=None, fighter=None,
                 ai=None, item=None):
        self.oid = oid
        self.log = log
        self.x = x
        self.y = y
        self.name = name
        self.faction = faction
        self.blocks = blocks
        self.inventory = inventory

        self.fighter = fighter
        if self.fighter:
            self.fighter.owner = self

        self.ai = ai
        if self.ai:
            self.ai.owner = self

        self.item = item
        if self.item:
            self.item.owner = self

    def move(self, dx, dy, level_map):
        """
        Port to [x+dx][y+dy].
        :param dx: difference in x
        :param dy: difference in y
        :param level_map: the level
        :return: True if movement was successful, False if not
        """
        old_x = self.x
        old_y = self.y
        new_x = self.x + dx
        new_y = self.y + dy
        if not level_map.is_blocked(new_x, new_y):
            self.x += dx
            self.y += dy
            self.log.log_movement(self.oid, old_x, old_y, new_x, new_y)
            return True
        else:
            return False

    def move_towards(self, target_x, target_y, game_map):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        return self.move(dx, dy, game_map)

#    def path_towards(self, target_x, target_y, game_map, objects, fov_map):
#        path = libtcod.path_new_using_map(fov_map)
#        libtcod.path_compute(path, self.x, self.y, target_x, target_y)
#        (x, y) = libtcod.path_walk(path, False)
#        if x is not None:
#            self.move_towards(x, y, game_map, objects)

    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def distance(self, x, y):
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)


class ChangeableProperty:
    """ Represents a property which can be changed by temporary means. """
    def __init__(self, property_type, base, effect_list, min_value=None, max_value=None):
        self.property_type = property_type
        self.base = base
        self.effect_list = effect_list
        self.min_value = min_value
        self.max_value = max_value

    @property
    def value(self):
        bonus = sum([e.value for e in self.effect_list if e.property_type == self.property_type])
        val = self.base + bonus
        if self.min_value is not None and val < self.min_value:
            return self.min_value
        elif self.max_value is not None and val > self.max_value:
            return self.max_value
        else:
            return val


class Fighter:
    def __init__(self, hp, defense, power, xp, accuracy=0, dodge=0, base_speed=100, death_function=None, inventory=None,
                 equipment_slots=None):
        self.owner = None

        self.effect_list = []
        self.base_max_hp = hp
        self.hp = hp

        self._defense = ChangeableProperty(c.PROPERTY_DEFENSE, defense, self.effect_list)
        self._power = ChangeableProperty(c.PROPERTY_POWER, power, self.effect_list, min_value=0)
        self._speed = ChangeableProperty(c.PROPERTY_SPEED, base_speed, self.effect_list, min_value=1)
        self._accuracy = ChangeableProperty(c.PROPERTY_ACCURACY, accuracy, self.effect_list)
        self._dodge = ChangeableProperty(c.PROPERTY_DODGE, dodge, self.effect_list)

        self.xp = xp
        self._time_until_turn = self.speed
        self.death_function = death_function
        self.inventory = inventory
        if equipment_slots is not None:
            self.equipment_slots = {slot: None for slot in equipment_slots}
        else:
            self.equipment_slots = []

        self.destroyed = False

    @property
    def max_hp(self):
        return self.base_max_hp

    @property
    def defense(self):
        return self._defense.value

    @property
    def power(self):
        return self._power.value

    @property
    def accuracy(self):
        return self._accuracy.value

    @property
    def dodge(self):
        return self._dodge.value

    @property
    def speed(self):
        return self._speed.value

    @property
    def time_until_turn(self):
        return self._time_until_turn

    def pass_time(self, time):
        self._time_until_turn -= time

    def end_turn(self):
        self._time_until_turn = self.speed

    def attack(self, target: GameObject):
        return target.fighter.receive_attack(self.owner.oid, self.accuracy, self.power)

    def receive_attack(self, attacker_oid, accuracy, damage):
        roll = utils.d100()
        final_accuracy = roll + accuracy - self.dodge
        if final_accuracy <= c.HIT_MISS_MAX:
            final_attack_damage = 0
        elif final_accuracy <= c.HIT_GRAZE_MAX:
            final_attack_damage = int(damage / 2)
        elif final_accuracy <= c.HIT_HIT_MAX:
            final_attack_damage = damage
        else:
            final_attack_damage = int(damage * 1.5)

        received_damage = final_attack_damage - self.defense
        self.owner.log.log_attack(attacker_oid, self.owner.oid, base_accuracy=accuracy, accuracy_roll=roll,
                                  dodge=self.dodge, base_damage=damage)

        return self._take_damage(received_damage)

    def _take_damage(self, damage):
        owner = self.owner

        if damage > 0:
            self.hp -= damage
            owner.log.log_take_damage(owner.oid, damage)

        if self.hp <= 0:
            self.destroyed = True
            owner.log.log_destruction(owner.oid, owner.x, owner.y)
            function = self.death_function
            if function is not None:
                function(owner)

    def heal(self, amount):
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def add_effect(self, effect):
        self.effect_list.append(effect)
        self.owner.log.log_apply_effect(self.owner.oid, effect)

    def remove_effect(self, effect):
        self.effect_list.remove(effect)
        self.owner.log.log_remove_effect(self.owner.oid, effect)
