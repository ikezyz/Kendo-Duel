Kendo Duel
==========

Kendo Duel is a terminal-based turn-based kendo strategy game. The player fights
through three stages against increasingly difficult bots: Rookie, Veteran, and
Dojo Master.

How to Run
----------
Run the project from the folder containing the Python files:

python main.py

main.py is the file to run. All .py files must remain in the same folder so the
simple imports can work correctly.

Required Files
--------------
main.py
game.py
fighter.py
bot.py
rules.py
records.py
utils.py
README.txt

battle_records.json is created automatically if it does not already exist.

Libraries
---------
No external libraries are required.

The program only uses Python built-in libraries:
- random
- json
- os
- datetime

Game Controls
-------------
Use number input to choose menu options and battle actions.

Main menu:
1. Start Game
2. View Rules
3. View Battle Records
4. Reset Battle Records
5. Exit

Battle actions:
1. Tsuki
2. Men Strike
3. Do Strike
4. Guard
5. Parry

Brief Rules
-----------
Each battle starts with fresh HP and 100 stamina. The player has 100 HP. The
three bots have increasing HP and difficulty.

Attacks cost 25 stamina and have 20 base damage.

Kendo-style attack meanings:
- Tsuki means thrust.
- Men Strike means an overhead/head strike.
- Do Strike means a side/body strike.

Attack counters:
- Tsuki beats Men Strike
- Men Strike beats Do Strike
- Do Strike beats Tsuki

The countering attack deals full damage. The countered attack still deals 10
damage. Both fighters can deal damage in the same round.

Repeating the same attack creates a combo:
- 1st use: x1.0 damage
- 2-hit combo: x1.2 damage
- 3-hit combo: x1.5 damage
- 4-hit combo or higher: x2.0 damage

Guard restores 25 stamina and reduces incoming non-combo attack damage by 80%.
Combo attacks break Guard.

Parry only succeeds against combo attacks. A successful Parry cancels incoming
combo damage, restores 25 stamina to the parrying fighter, reduces the attacker's
stamina by 30, and resets the attacker's combo.

Battle Records
--------------
Completed game results are saved in battle_records.json. If this file is missing
or corrupted, the program handles the problem safely and continues.

Advanced Python Concepts Demonstrated
-------------------------------------
1. Object-oriented programming with Fighter, Bot, and Game classes
2. File I/O with JSON for battle records
3. Exception handling and input validation
4. Randomised bot behaviour
