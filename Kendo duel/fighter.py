import rules


class Fighter:
    """Stores shared information and actions for the player and bots."""

    def __init__(self, name, max_hp):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.max_stamina = rules.MAX_STAMINA
        self.stamina = rules.MAX_STAMINA
        self.last_attack = None
        self.combo_count = 0

    def reset_for_battle(self):
        """Reset HP, stamina, and combo state at the start of a battle."""
        self.hp = self.max_hp
        self.stamina = self.max_stamina
        self.last_attack = None
        self.combo_count = 0

    def can_attack(self):
        return self.stamina >= rules.ATTACK_COST

    def spend_stamina(self, amount):
        self.stamina = rules.clamp(self.stamina - amount, 0, self.max_stamina)

    def restore_stamina(self, amount):
        self.stamina = rules.clamp(self.stamina + amount, 0, self.max_stamina)

    def take_damage(self, amount):
        self.hp = rules.clamp(self.hp - amount, 0, self.max_hp)

    def update_combo(self, action):
        """Update combo count when the same attack is repeated."""
        if rules.is_attack(action):
            if self.last_attack == action:
                self.combo_count += 1
            else:
                self.last_attack = action
                self.combo_count = 1
        else:
            self.reset_combo()

    def reset_combo(self):
        self.last_attack = None
        self.combo_count = 0

    def get_combo_multiplier(self):
        return rules.get_combo_multiplier(self.combo_count)

    def get_combo_text(self):
        if rules.is_combo(self) and self.last_attack is not None:
            multiplier = self.get_combo_multiplier()
            return self.last_attack + " combo x" + str(multiplier)
        return "No active combo"
