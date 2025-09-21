import random

def guessing_game():
    while True:
        rand_num = random.randint(1, 1000)
        attempts = 0

        while True:
            user_input = input("Guess a random number between 1 and 1000. Type 'bye' or 'exit' to quit: ").strip()

            if user_input.lower() == "bye" or user_input.lower() == "exit":
                print("Goodbye!")
                return

            if not user_input.isdigit():
                print("Please enter a valid number")
                continue

            guess = int(user_input)
            attempts += 1

            if guess < rand_num:
                print("Too low!")
            elif guess > rand_num:
                print("Too high!")
            else:
                print(f"Congratulations! You guessed the number in {attempts} attempts!")
                break

guessing_game()
