from bot import Bot
from fighter import Fighter
import records
import rules
from utils import get_menu_choice, pause, print_line


GUARD_RESTORE = 25
PARRY_RESTORE = 25
PARRY_STAMINA_PENALTY = 30


class Game:
    """Controls menus, battles, round resolution, and stage progression."""

    def __init__(self):
        self.player = Fighter("Player", rules.PLAYER_HP)
        self.stages = [
            Bot("Rookie", 80, 1, "rookie"),
            Bot("Veteran", 100, 2, "veteran"),
            Bot("Dojo Master", 120, 3, "master"),
        ]

    def main_menu(self):
        while True:
            print()
            print_line()
            print("KENDO DUEL")
            print_line()
            print("1. Start Game")
            print("2. View Rules")
            print("3. View Battle Records")
            print("4. Reset Battle Records")
            print("5. Exit")

            choice = get_menu_choice("Choose an option: ", ["1", "2", "3", "4", "5"])

            if choice == "1":
                self.start_game()
            elif choice == "2":
                self.show_rules()
            elif choice == "3":
                self.view_records()
            elif choice == "4":
                self.reset_records()
            elif choice == "5":
                print("Thank you for playing Kendo Duel.")
                break

    def show_rules(self):
        print()
        print_line()
        print("RULES AND TUTORIAL")
        print_line()
        print("You are a kendo fighter trying to defeat three opponents:")
        print("Stage 1: Rookie")
        print("Stage 2: Veteran")
        print("Stage 3: Dojo Master")
        print()
        print("Each battle starts with fresh HP and 100 stamina.")
        print("Player HP is 100. Bot HP increases by stage.")
        print()
        print("Actions:")
        print("1. Tsuki - thrust attack, costs 25 stamina, base damage 20")
        print("2. Men Strike - overhead/head strike, costs 25 stamina, base damage 20")
        print("3. Do Strike - side/body strike, costs 25 stamina, base damage 20")
        print("4. Guard - reduces non-combo attack damage by 80% and restores 25 stamina")
        print("5. Parry - only works against combo attacks")
        print()
        print("Kendo-style attack meanings:")
        print("- Tsuki means thrust.")
        print("- Men Strike means an overhead/head strike.")
        print("- Do Strike means a side/body strike.")
        print()
        print("Attack counters:")
        print("- Tsuki beats Men Strike")
        print("- Men Strike beats Do Strike")
        print("- Do Strike beats Tsuki")
        print("The winning attack deals full damage. The countered attack still deals 10 damage.")
        print()
        print("Combos:")
        print("- Repeat the same attack in consecutive rounds to create a combo.")
        print("- 2-hit combo: x1.2 damage")
        print("- 3-hit combo: x1.5 damage")
        print("- 4-hit combo or higher: x2.0 damage")
        print("- Combo attacks break Guard.")
        print("- A countered combo attack still deals at least 20 damage.")
        print()
        print("Parry:")
        print("- Parry succeeds only if the opponent uses a combo attack.")
        print("- Successful Parry cancels all incoming combo damage.")
        print("- The attacker loses 30 stamina and their combo is reset.")
        print("- The parrying fighter restores 25 stamina.")
        print("- Failed Parry does not restore stamina.")
        pause()

    def start_game(self):
        self.show_rules()
        defeated_bots = []

        for stage_number, bot in enumerate(self.stages, start=1):
            player_won = self.run_battle(bot, stage_number)
            if player_won:
                defeated_bots.append(bot.name)
                print("\nYou defeated", bot.name + "!")
            else:
                print("\nYou were defeated by", bot.name + ".")
                records.add_record({
                    "result": "Loss",
                    "stage_reached": stage_number,
                    "defeated_bots": defeated_bots,
                    "final_player_hp": self.player.hp,
                })
                print("Battle record saved.")
                return

        print("\nCongratulations! You defeated all three opponents and won Kendo Duel!")
        records.add_record({
            "result": "Win",
            "stage_reached": 3,
            "defeated_bots": defeated_bots,
            "final_player_hp": self.player.hp,
        })
        print("Battle record saved.")

    def run_battle(self, bot, stage_number):
        self.player.reset_for_battle()
        bot.reset_for_battle()
        round_number = 1
        previous_player_action = None
        previous_bot_action = None

        print()
        print_line()
        print("STAGE", stage_number, "-", bot.name)
        print_line()

        while self.player.hp > 0 and bot.hp > 0:
            self.show_battle_status(
                bot,
                stage_number,
                round_number,
                previous_player_action,
                previous_bot_action
            )
            player_action = self.get_player_action()
            bot_action = bot.choose_action(self.player)
            summary = self.resolve_round(player_action, bot_action, bot)

            print("\nROUND", round_number, "SUMMARY")
            print("-" * 50)
            for line in summary:
                print(line)
            print("Player: " + str(self.player.hp) + " HP, " + str(self.player.stamina) + " stamina")
            print(bot.name + ": " + str(bot.hp) + " HP, " + str(bot.stamina) + " stamina")

            previous_player_action = player_action
            previous_bot_action = bot_action
            round_number += 1
            pause()

        return self.player.hp > 0

    def show_battle_status(self, bot, stage_number, round_number,
                           previous_player_action, previous_bot_action):
        print()
        print_line()
        print("Stage", stage_number, "-", bot.name, "| Round", round_number)
        print_line()
        print("Player HP:", self.player.hp, "| Stamina:", self.player.stamina)
        print(bot.name + " HP:", bot.hp, "| Stamina:", bot.stamina)
        print("Previous round:")
        print("Player used:", previous_player_action if previous_player_action is not None else "None")
        print(bot.name + " used:", previous_bot_action if previous_bot_action is not None else "None")
        print("\nAvailable actions:")

        all_actions = rules.ATTACKS + rules.DEFENSIVE_ACTIONS
        for index, action in enumerate(all_actions, start=1):
            print(str(index) + ".", action)

    def get_player_action(self):
        all_actions = rules.ATTACKS + rules.DEFENSIVE_ACTIONS
        valid_choices = ["1", "2", "3", "4", "5"]

        while True:
            choice = get_menu_choice("Choose your action: ", valid_choices)
            action = all_actions[int(choice) - 1]

            if rules.is_attack(action) and not self.player.can_attack():
                print("You do not have enough stamina to attack. Choose Guard or Parry.")
            else:
                return action

    def resolve_round(self, player_action, bot_action, bot):
        summary = []
        summary.append("Player action: " + player_action)
        summary.append(bot.name + " action: " + bot_action)

        # First, apply stamina costs for attacks.
        if rules.is_attack(player_action):
            self.player.spend_stamina(rules.ATTACK_COST)
        if rules.is_attack(bot_action):
            bot.spend_stamina(rules.ATTACK_COST)

        # Then update combo tracking. Defensive actions reset the user's combo.
        self.player.update_combo(player_action)
        bot.update_combo(bot_action)

        self.add_combo_summary(self.player, player_action, summary)
        self.add_combo_summary(bot, bot_action, summary)

        if player_action == "Guard":
            self.player.restore_stamina(GUARD_RESTORE)
            summary.append("Player used Guard and restored 25 stamina.")
        if bot_action == "Guard":
            bot.restore_stamina(GUARD_RESTORE)
            summary.append(bot.name + " used Guard and restored 25 stamina.")

        self.add_counter_summary(player_action, bot_action, bot, summary)

        player_damage = 0
        bot_damage = 0

        player_parry_success = self.is_successful_parry(self.player, player_action, bot, bot_action)
        bot_parry_success = self.is_successful_parry(bot, bot_action, self.player, player_action)

        if player_parry_success:
            self.handle_successful_parry(self.player, bot)
            summary.append("Player Parry succeeded. " + bot.name + "'s combo was interrupted.")
        elif player_action == "Parry":
            summary.append("Player Parry failed.")

        if bot_parry_success:
            self.handle_successful_parry(bot, self.player)
            summary.append(bot.name + " Parry succeeded. Player combo was interrupted.")
        elif bot_action == "Parry":
            summary.append(bot.name + " Parry failed.")

        if rules.is_attack(player_action) and not bot_parry_success:
            player_damage = self.calculate_damage(self.player, bot, player_action, bot_action, summary)

        if rules.is_attack(bot_action) and not player_parry_success:
            bot_damage = self.calculate_damage(bot, self.player, bot_action, player_action, summary)

        bot.take_damage(player_damage)
        self.player.take_damage(bot_damage)

        summary.append("Player dealt " + str(player_damage) + " damage.")
        summary.append(bot.name + " dealt " + str(bot_damage) + " damage.")
        return summary

    def add_combo_summary(self, fighter, action, summary):
        """Add a clear summary line about whether combo damage can apply."""
        if not rules.is_attack(action):
            return

        if rules.is_combo(fighter):
            multiplier = fighter.get_combo_multiplier()
            summary.append(fighter.name + " used a combo attack: "
                           + action + " x" + str(multiplier) + ".")
        else:
            summary.append(fighter.name + " used a normal attack with no combo multiplier.")

    def add_counter_summary(self, player_action, bot_action, bot, summary):
        """Add a clear summary line about the attack counter result."""
        if not rules.is_attack(player_action) or not rules.is_attack(bot_action):
            summary.append("Counter result: no attack counter this round.")
            return

        if rules.attack_beats(player_action, bot_action):
            summary.append("Counter result: Player's " + player_action
                           + " countered " + bot.name + "'s " + bot_action + ".")
        elif rules.attack_beats(bot_action, player_action):
            summary.append("Counter result: " + bot.name + "'s " + bot_action
                           + " countered Player's " + player_action + ".")
        else:
            summary.append("Counter result: both fighters used the same attack, so no counter applied.")

    def is_successful_parry(self, defender, defender_action, attacker, attacker_action):
        """A parry only succeeds against an opponent's combo attack."""
        return (
            defender_action == "Parry"
            and rules.is_attack(attacker_action)
            and rules.is_combo(attacker)
        )

    def handle_successful_parry(self, defender, attacker):
        defender.restore_stamina(PARRY_RESTORE)
        attacker.spend_stamina(PARRY_STAMINA_PENALTY)
        attacker.reset_combo()

    def calculate_damage(self, attacker, defender, attacker_action, defender_action, summary):
        damage = rules.BASE_DAMAGE
        attacker_has_combo = rules.is_combo(attacker)

        if attacker_has_combo:
            multiplier = attacker.get_combo_multiplier()
            damage = int(rules.BASE_DAMAGE * multiplier)
            summary.append(attacker.name + " combo damage applied: x" + str(multiplier) + ".")

        if rules.is_attack(defender_action) and rules.attack_beats(defender_action, attacker_action):
            if attacker_has_combo:
                damage = max(20, int(damage * 0.5))
                summary.append(defender.name + "'s " + defender_action + " countered "
                               + attacker.name + "'s combo attack, but combo damage stayed at least 20.")
            else:
                damage = int(rules.BASE_DAMAGE * 0.5)
                summary.append(defender.name + "'s " + defender_action + " countered "
                               + attacker.name + "'s " + attacker_action + ".")

        if defender_action == "Guard":
            if attacker_has_combo:
                summary.append(defender.name + "'s Guard was broken by a combo attack.")
            else:
                damage = int(damage * 0.2)
                summary.append(defender.name + "'s Guard reduced incoming damage.")

        return int(damage)

    def view_records(self):
        battle_records = records.load_records()
        print()
        print_line()
        print("BATTLE RECORDS")
        print_line()

        if len(battle_records) == 0:
            print("No battle records yet.")
            pause()
            return

        for index, record in enumerate(battle_records, start=1):
            print("\nRecord", index)
            print("Date/Time:", record.get("date_time", "Unknown"))
            print("Result:", record.get("result", "Unknown"))
            print("Stage reached:", record.get("stage_reached", "Unknown"))
            defeated = record.get("defeated_bots", [])
            if defeated:
                print("Defeated bots:", ", ".join(defeated))
            else:
                print("Defeated bots: None")
            print("Final player HP:", record.get("final_player_hp", "Unknown"))

        pause()

    def reset_records(self):
        print("\nResetting battle records will delete all saved records.")
        choice = get_menu_choice("Type YES to confirm, or N to cancel: ", ["YES", "N"])
        if choice == "YES":
            records.reset_records()
            print("Battle records have been reset.")
        else:
            print("Reset cancelled.")
        pause()
