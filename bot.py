import random

import rules
from fighter import Fighter


class Bot(Fighter):
    """A computer-controlled fighter with difficulty-based behaviour."""

    def __init__(self, name, max_hp, difficulty_level, behaviour_type):
        super().__init__(name, max_hp)
        self.difficulty_level = difficulty_level
        self.behaviour_type = behaviour_type

    def choose_action(self, player):
        """Choose an action based on the bot's behaviour type."""
        if not self.can_attack():
            return "Guard"

        if not player.can_attack():
            return random.choice(rules.ATTACKS)

        if self.behaviour_type == "rookie":
            return self.choose_rookie_action(player)
        if self.behaviour_type == "veteran":
            return self.choose_veteran_action(player)
        return self.choose_master_action(player)

    def choose_rookie_action(self, player):
        # Rookie often repeats attacks, making it predictable.
        if self.last_attack in rules.ATTACKS and random.random() < 0.60:
            return self.last_attack

        roll = random.random()
        if roll < 0.08:
            return "Guard"
        if roll < 0.12 and rules.is_combo(player):
            return "Parry"
        return random.choice(rules.ATTACKS)

    def choose_veteran_action(self, player):
        # Veteran is balanced and uses defence more intelligently.
        if rules.is_combo(player) and random.random() < 0.18:
            return "Parry"
        if self.stamina <= 45 and random.random() < 0.35:
            return "Guard"

        roll = random.random()
        if roll < 0.15:
            return "Guard"
        if roll < 0.20 and rules.is_combo(player):
            return "Parry"
        return random.choice(rules.ATTACKS)

    def choose_master_action(self, player):
        # Dojo Master reacts strongly to player combos and low stamina.
        if rules.is_combo(player) and random.random() < 0.45:
            return "Parry"
        if self.stamina <= 55 and random.random() < 0.55:
            return "Guard"

        roll = random.random()
        if roll < 0.18:
            return "Guard"
        if roll < 0.25 and rules.is_combo(player):
            return "Parry"
        return random.choice(rules.ATTACKS)
