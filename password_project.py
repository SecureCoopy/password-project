import string
import random
import nltk
from nltk.corpus import words
from zxcvbn import zxcvbn

# Ensure the words list is downloaded
nltk.download('words', quiet=True)

def get_random_word(min_length=4):
    english_words = [word for word in words.words() if len(word) >= min_length]
    return random.choice(english_words).lower()

def add_random_characters(word):
    special_chars = string.punctuation.replace('-', '')  # Exclude dash as it's used as a separator
    number = str(random.randint(0, 9))
    special_char = random.choice(special_chars)
    positions = random.sample(range(len(word) + 2), 2)  # +2 for number and special char
    new_word = list(word)
    for pos in sorted(positions, reverse=True):  # Insert number and special char in random positions
        new_word.insert(pos, number if pos % 2 == 0 else special_char)
    return ''.join(new_word)

def prompt_length(min_length, max_length):
    while True:
        try:
            length = int(input("Enter desired length: "))
            if length < min_length:
                print(f"The length must be at least {min_length} characters.")
            elif length > max_length:
                print(f"The length must be no more than {max_length} characters.")
            else:
                return length
        except ValueError:
            print("Please enter a valid number.")

def generate_random_password(min_length, max_length):
    length = prompt_length(min_length, max_length)
    password = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(length))
    return password

def generate_passphrase(min_parts, max_length):
    num_parts = max(int(input(f"Enter the number of words in the passphrase (minimum {min_parts}): ")), min_parts)
    passphrase_parts = [add_random_characters(get_random_word()) for _ in range(num_parts)]
    passphrase = '-'.join(passphrase_parts)
    return passphrase

def display_strength_bar(score):
    bar_levels = {
        0: "[----------]",  # weakest
        1: "[#---------]",
        2: "[###-------]",  # weak
        3: "[#####-----]",
        4: "[##########]",  # strongest
    }
    bar_color = {
        0: '\033[91m',  # Red
        1: '\033[91m',  # Red
        2: '\033[93m',  # Yellow
        3: '\033[93m',  # Yellow
        4: '\033[92m',  # Green
    }
    reset_color = '\033[0m'
    colored_bar = bar_color[score] + bar_levels[score] + reset_color
    print(f"Password Strength: {colored_bar}")

fun_facts = [
    "Did you know? The most common password is '123456'. It's also the most hacked!",
    "Fun Fact: Passwords created by humans often contain predictable patterns. Random generators are more secure.",
    "Remember: Strong passwords are like good friends - they protect you in times of need!",
    "Security Tip: The longer the password, the better. Each additional character increases its security.",
    "Cybersecurity Insight: Passwords should be like toothbrushes. Don't leave them out, change them regularly, and don't share them."
]

def display_strength_explanation(score):
    explanations = {
        0: "This password is very weak. Avoid common patterns and add more unique characters.",
        1: "This password is weak. Consider using a longer mix of characters and avoid guessable patterns.",
        2: "This password is okay, but adding more length and symbols would make it stronger.",
        3: "This password is strong. It has a good mix of letters, numbers, and symbols.",
        4: "This password is very strong! It's long and includes a complex variety of characters."
    }
    print(explanations[score])
    print(random.choice(fun_facts))  # Display a random fun fact

def get_feedback(password):
    results = zxcvbn(password)
    score = results['score']
    display_strength_bar(score)
    display_strength_explanation(score)
    print(random.choice(fun_facts))  # Display a random fun fact
    suggestions = results['feedback'].get('suggestions', [])
    return ' '.join(suggestions) if suggestions else "Password is strong."

def get_user_input():
    MAX_LENGTH = 64  # Define a practical maximum length for passwords and passphrases
    MIN_LENGTH = 12  # Minimum length for passwords

    while True:
        print("\nChoose an option:")
        print("1: Generate random password")
        print("2: Generate passphrase")
        print("3: Enter your own password")
        choice = input("Your choice (1, 2, 3, or 'switch' to change option): ").strip().lower()

        if choice == 'switch':
            continue
        elif choice not in ["1", "2", "3"]:
            print("Invalid choice")
            continue

        # Removed attempt_limit and attempt logic for simplicity
        if choice == "1":
            item_generated = generate_random_password(MIN_LENGTH, MAX_LENGTH)
            print(f"Generated Password: {item_generated}")
        elif choice == "2":
            item_generated = generate_passphrase(6, MAX_LENGTH)
            print(f"Generated Passphrase: {item_generated}")
        elif choice == "3":
            item_generated = input("Enter your password: ")
            print(get_feedback(item_generated))  # Display strength bar for user-entered password

        feedback = get_feedback(item_generated)
        print(feedback)

        satisfied = input("Are you satisfied with this password? (Y/N) or type 'switch' to change option: ").strip().lower()
        if satisfied == 'switch':
            continue
        elif satisfied == "y":
            print("Please remember your password!")
            break  # Exit the loop after confirming the password

def main():
    get_user_input()

if __name__ == "__main__":
    main()
