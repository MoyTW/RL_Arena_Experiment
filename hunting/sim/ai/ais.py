from hunting.sim.ai.core import MonsterAI, ObjectiveEliminate, ObjectiveKite
import hunting.constants as c
import hunting.sim.ai.behaviours as behaviours


class DummyAI(MonsterAI):
    def __init__(self):
        super().__init__(level=None, objectives_to_behaviours=None)

    def assess_objective(self):
        pass


class RunnerMonster(MonsterAI):
    def __init__(self, level, max_dist=5):
        objectives_to_behaviours = {
            c.OBJECTIVE_KITE: [behaviours.OpenDistance(self, max_dist=max_dist), behaviours.BasicMelee(self)]
        }
        super().__init__(level, objectives_to_behaviours)

    def assess_objective(self):
        enemies = self.level.get_objects_outside_faction(self.owner.faction)

        if len(enemies) > 0:
            distances = {self.owner.distance_to(e): e for e in enemies}
            closest_distance = min(distances)
            closest_enemy = distances[closest_distance]
            self.objective = ObjectiveKite(closest_enemy)


class TestMonster(MonsterAI):
    def __init__(self, level):
        objectives_to_behaviours = {
            c.OBJECTIVE_ELIMINATE: [behaviours.BasicMelee(self), behaviours.UseAnyThrowingItem(self),
                                    behaviours.CloseDistance(self)]
        }
        super().__init__(level, objectives_to_behaviours)

    def assess_objective(self):
        enemies = self.level.get_objects_outside_faction(self.owner.faction)

        if len(enemies) > 0:
            distances = {self.owner.distance_to(e): e for e in enemies}
            closest_distance = min(distances)
            closest_enemy = distances[closest_distance]
            self.objective = ObjectiveEliminate(target=closest_enemy)
