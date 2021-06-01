

# https://www.youtube.com/watch?v=WLYEsgYkEvY
class Health:

    def __init__(self, max_health):
        self.max_health = max_health
        self.health = max_health

    def get_max_health(self):
        return self.max_health

    def set_max_health(self, max_health):
        self.max_health = max_health

    def get_current_health(self):
        return self.health

    def set_current_health(self, health):
        self.health = health

    def get_damage(self, damage):
        if self.health > 0:
            self.health -= damage

    def get_health(self, health):
        if self.health < self.max_health:
            self.health += health

