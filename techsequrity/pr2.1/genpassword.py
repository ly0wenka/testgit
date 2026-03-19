import random

# список слів (можеш розширити)
words = [
    "apple", "river", "tiger", "coffee", "sunset",
    "mountain", "cloud", "forest", "ocean", "stone",
    "wind", "fire", "shadow", "light", "storm"
]

def generate_password(num_words=4):
    selected = random.sample(words, num_words)

    # випадкові варіації
    password = ""
    for word in selected:
        if random.choice([True, False]):
            word = word.capitalize()
        password += word

    # додаємо цифри і символ
    password += str(random.randint(10, 99))
    password += random.choice("!@#$%^&*")

    return password

# приклад
print(generate_password())
