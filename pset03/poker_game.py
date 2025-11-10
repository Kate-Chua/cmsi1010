from cards import deal, poker_classification


def main():
    while True:
        user_input = input(
            "Enter the number of players(2-10): ").strip().lower()
        if user_input in ("bye", "exit"):
            break
        try:
            num_players = int(user_input)
            if not 2 <= num_players <= 10:
                print("Error: number of players must be between 2 and 10.")
                continue
        except ValueError:
            print("Error: please enter a valid number.")
            continue

        hands = deal(num_players, 5)
        for hand in hands:
            hand_str = " ".join(str(card) for card in sorted(
                hand, key=lambda c: (c.suit, c.rank)))
            classification = poker_classification(hand)
            print(f"{hand_str} is a {classification}")


if __name__ == "__main__":
    main()
