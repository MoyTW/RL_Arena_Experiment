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

    def set_coordinates(self, x, y):
        self.x = x
        self.y = y

    def can_move(self, dx, dy, level_map):
        return not level_map.is_blocked(self.x + dx, self.y + dy)

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
        if self.can_move(dx, dy, level_map):
            self.x += dx
            self.y += dy
            self.log.log_movement(self.oid, old_x, old_y, self.x, self.y)
            return True
        else:
            return False

    def move_towards(self, target_x, target_y, game_map):
        (next_x, next_y) = game_map.a_star_path(self.x, self.y, target_x, target_y)[0]
        dx = next_x - self.x
        dy = next_y - self.y
        return self.move(dx, dy, game_map)

    def movable_squares(self, game_map):
        movables = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                if (not (x == 0 and y == 0)) and self.can_move(x, y, game_map):
                    movables.append([self.x + x, self.y + y])
        return movables

    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def is_adjacent(self, other):
        return self.distance_to(other) <= 1.5

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
    def __init__(self, max_hp, max_stamina, defense, power, xp, accuracy=0, dodge=0, speed=100, death_function=None,
                 skills=None, inventory=None, equipment_slots=None, hp=None, stamina=None):
        self.owner = None

        self.effect_list = []

        self._max_hp = ChangeableProperty(c.PROPERTY_MAX_HP, max_hp, self.effect_list)
        if hp is None:
            self._hp = max_hp
        else:
            self._hp = hp
        self._max_stamina = ChangeableProperty(c.PROPERTY_MAX_STAMINA, max_stamina, self.effect_list)
        if stamina is None:
            self._stamina = max_stamina
        else:
            self._stamina = max_stamina

        self._defense = ChangeableProperty(c.PROPERTY_DEFENSE, defense, self.effect_list)
        self._power = ChangeableProperty(c.PROPERTY_POWER, power, self.effect_list, min_value=0)
        self._speed = ChangeableProperty(c.PROPERTY_SPEED, speed, self.effect_list, min_value=1)
        self._accuracy = ChangeableProperty(c.PROPERTY_ACCURACY, accuracy, self.effect_list)
        self._dodge = ChangeableProperty(c.PROPERTY_DODGE, dodge, self.effect_list)

        self.xp = xp
        self._time_until_turn = self.speed
        self.death_function = death_function
        self.inventory = inventory
        if skills is None:
            self._skills = []
        else:
            self._skills = skills
        if equipment_slots is not None:
            self.equipment_slots = {slot: None for slot in equipment_slots}
        else:
            self.equipment_slots = []

        self.destroyed = False

    @property
    def max_hp(self):
        return self._max_hp.value

    @property
    def hp(self):
        return self._hp

    @property
    def max_stamina(self):
        return self._max_stamina

    @property
    def stamina(self):
        return self._stamina

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
        for e in self.effect_list:
            if e.is_temporary:
                e.pass_time(time)
        for e in [e for e in self.effect_list if e.is_expired]:
            self.effect_list.remove(e)

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

    def remove_stamina(self, stamina):
        # TODO: Log removal
        self._stamina -= stamina
        if self._stamina < 0:
            raise ValueError('Cannot remove stamina, would take below 0!')

    def restore_stamina(self, stamina):
        # TODO: Log addition
        self._stamina += stamina
        if self._stamina > self.max_stamina:
            self._stamina = self.max_stamina

    def _take_damage(self, damage):
        owner = self.owner

        if damage > 0:
            self._hp -= damage
            owner.log.log_take_damage(owner.oid, damage)

        if self.hp <= 0:
            self.destroyed = True
            owner.log.log_destruction(owner.oid, owner.x, owner.y)
            function = self.death_function
            if function is not None:
                function(owner)

    def heal(self, amount):
        self._hp += amount
        if self.hp > self.max_hp:
            self._hp = self.max_hp

    def add_effect(self, effect):
        self.effect_list.append(effect)
        self.owner.log.log_apply_effect(self.owner.oid, effect)

    def remove_effect(self, effect):
        self.effect_list.remove(effect)
        self.owner.log.log_remove_effect(self.owner.oid, effect)
