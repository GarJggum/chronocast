import random
import string

def generate_random_string(length=32):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Example usage
if __name__ == "__main__":
    print(generate_random_string())
