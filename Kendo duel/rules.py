ATTACKS = ["Tsuki", "Men Strike", "Do Strike"]
DEFENSIVE_ACTIONS = ["Guard", "Parry"]

BASE_DAMAGE = 20
ATTACK_COST = 25
PLAYER_HP = 100
MAX_STAMINA = 100

COUNTER_RULES = {
    "Tsuki": "Men Strike",
    "Men Strike": "Do Strike",
    "Do Strike": "Tsuki",
}

COMBO_MULTIPLIERS = {
    1: 1.0,
    2: 1.2,
    3: 1.5,
    4: 2.0,
}


def get_combo_multiplier(combo_count):
    """Return the correct damage multiplier for a combo count."""
    if combo_count >= 4:
        return COMBO_MULTIPLIERS[4]
    return COMBO_MULTIPLIERS.get(combo_count, 1.0)


def attack_beats(attack_a, attack_b):
    """Return True if attack_a counters attack_b."""
    return COUNTER_RULES.get(attack_a) == attack_b


def is_attack(action):
    """Return True if the action is one of the three attack actions."""
    return action in ATTACKS


def is_combo(fighter):
    """Return True if the fighter is currently using a combo attack."""
    return fighter.combo_count >= 2


def clamp(value, minimum, maximum):
    """Keep a number within a minimum and maximum range."""
    return max(minimum, min(value, maximum))
