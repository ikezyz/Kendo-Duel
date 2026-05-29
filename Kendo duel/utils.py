def get_menu_choice(prompt, valid_choices):
    """Keep asking until the player enters one of the valid choices."""
    while True:
        try:
            user_input = input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nInput ended. Exiting Kendo Duel safely.")
            raise SystemExit

        if user_input in valid_choices:
            return user_input

        print("Invalid input. Please choose:", ", ".join(valid_choices))


def print_line():
    print("=" * 50)


def pause():
    try:
        input("\nPress Enter to continue...")
    except (EOFError, KeyboardInterrupt):
        print("\nInput ended. Exiting Kendo Duel safely.")
        raise SystemExit
