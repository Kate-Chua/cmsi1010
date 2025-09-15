import random

words = {
    "noun": ["dog", "carrot", "chair", "toy", "rice cake"],
    "verb": ["ran", "barked", "squeaked", "flew", "fell", "whistled"],
    "adjective": ["small", "great", "fuzzy", "funny", "light"],
    "preposition": ["through", "over", "under", "beyond", "across"],
    "adverb": ["barely", "mostly", "easily", "already", "just"],
    "color": ["pink", "blue", "mauve", "red", "transparent", "baby pink," "yellow", "green"]
}

templates = ["""
    Yesterday the color noun
    verb preposition the coach’s
    adjective color noun that was
    adverb adjective before
    """,
    """
    The adjective noun
    verb quickly over the color noun
    while the adjective noun
    verb adverb nearby
    """]


def random_sentence():
    sentence = []

    for token in templates:
        if token in words:
            sentence.append(random.choice(words[token]))
        else:
            sentence.append(token)
    return " ".join(sentence) + "."

for _ in range(5):
    print(random_sentence())

#Unfinished, must add additional for loop for sentence templates to work