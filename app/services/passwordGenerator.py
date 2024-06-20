import random


async def generate_password(length: int, char_set: str) -> str:
    # Convert char_set to a list to shuffle characters
    password_list = list(char_set)
    # Shuffle the characters in place
    random.shuffle(password_list)
    # Join the first `length` characters to form the password
    return ''.join(password_list[:length])
