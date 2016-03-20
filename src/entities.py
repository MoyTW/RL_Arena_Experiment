import math
from src.level_log import LevelLog


class GameObject(object):
    def __init__(self, oid, log: LevelLog, x, y, name, faction=None, blocks=False, inventory=None, fighter=None,
                 ai=None, item=None, equipment=None):
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

        self.equipment = equipment
        if self.equipment:
            self.equipment.owner = self
            if not self.item:
                raise ValueError('Cannot construct with an Item and Equipment! Use Equipment only!')

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


class Fighter:
    def __init__(self, hp, defense, power, xp, base_speed=100, death_function=None, inventory=None):
        self.base_max_hp = hp
        self.hp = hp
        self.base_defense = defense
        self.base_power = power
        self.xp = xp
        self.base_speed = base_speed
        self._time_until_turn = self.base_speed
        self.death_function = death_function
        self.inventory = inventory
        self._power_buffs = []
        self._speed_buffs = []

    @property
    def max_hp(self):
        return self.base_max_hp

    @property
    def defense(self):
        return self.base_defense

    @property
    def power(self):
        buffs = sum(buff[0] for buff in self._power_buffs)
        return self.base_power + buffs

    @property
    def speed(self):
        buffs = sum(buff[0] for buff in self._speed_buffs)
        return self.base_speed - buffs

    @property
    def time_until_turn(self):
        return self._time_until_turn

    def pass_time(self, time):
        self._time_until_turn -= time
        for buff in self._power_buffs:
            buff[1] -= time
            if buff[1] < 0:
                self._power_buffs.remove(buff)
        for buff in self._speed_buffs:
            buff[1] -= time
            if buff[1] < 0:
                self._speed_buffs.remove(buff)

    def end_turn(self):
        self._time_until_turn = self.speed

    def attack(self, target):
        self.owner.log.log_attack(self.owner.oid, target.oid)
        damage = self.power - target.fighter.defense
        if damage > 0:
            target.fighter.take_damage(damage)
        return damage

    def take_damage(self, damage):
        owner = self.owner

        if damage > 0:
            self.hp -= damage
            owner.log.log_take_damage(owner.oid, damage)

        if self.hp <= 0:
            owner.log.log_destruction(owner.oid, owner.x, owner.y)
            function = self.death_function
            if function is not None:
                function(owner)

    def heal(self, amount):
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def apply_power_buff(self, amount, time):
        self._power_buffs.append([amount, time])

    def apply_speed_buff(self, amount, time):
        self._speed_buffs.append([amount, time])
