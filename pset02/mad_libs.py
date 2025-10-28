import random

# I chatGPTed the templates for the mad libs game
templates = [
    {"text": "The :adjective :animal :verb over the :color :object.", "author": "Kate"},
    {"text": "A :profession always carries a :item while :verb-ing.", "author": "Sam"},
    {"text": "Never trust a :adjective :creature who loves :food too much.", "author": "Luis"},
    {"text": "My :relative told me that :place has :number hidden treasures.", "author": "Ava"},
    {"text": "The :color spaceship landed on a :adjective planet full of :animal.", "author": "Milo"},
    {"text": "Every morning, a :adjective :animal drinks :drink before sunrise.",
        "author": "Raya"},
    {"text": "Legend says the :object will grant :number wishes to a :person.",
        "author": "Toby"},
    {"text": "I once saw a :animal wearing a :clothing while :verb-ing loudly.",
        "author": "Nico"},
    {"text": "A :person and a :animal started a band called ':adjective Beats'.",
        "author": "June"},
    {"text": "Beware of the :adjective :monster that eats only :food and :drink.", "author": "Lena"}
]

yes_answers = {"yes", "y", "yeah", "sure", "si", "sí", "oui", "ok", "okay"}


def fill_template(template):
    words = template.split()
    replacements = {}
    for i, word in enumerate(words):
        if word.startswith(":"):
            label = word.strip(".,!?")
            if label not in replacements:
                while True:
                    user_input = input(f"Enter a {label[1:]}: ")
                    if 1 <= len(user_input) <= 30:
                        break
                    print("Please enter between 1 and 30 characters.")
                replacements[label] = user_input
    for label, replacement in replacements.items():
        template = template.replace(label, replacement)
    return template


def play():
    while True:
        chosen = random.choice(templates)
        final_story = fill_template(chosen["text"])
        print("\n" + final_story)
        print(f"\nAuthor: {chosen['author']}\n")
        again = input("Play again? ").strip().lower()
        if again not in yes_answers:
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    play()
