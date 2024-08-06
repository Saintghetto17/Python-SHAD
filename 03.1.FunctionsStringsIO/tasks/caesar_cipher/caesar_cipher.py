import string


def caesar_encrypt(message: str, n: int) -> str:
    """Encrypt message using caesar cipher

    :param message: message to encrypt
    :param n: shift
    :return: encrypted message
    """

    letters = list(string.ascii_lowercase)
    letters_upper = list(string.ascii_uppercase)
    order = list(range(26))

    dictionary_original: dict[int, str] = dict(zip(order, letters))
    dictionary_original_upper: dict[int, str] = dict(zip(order, letters_upper))

    dictionary_punctuation: dict[str, str] = dict(zip(string.punctuation, string.punctuation))

    dictionary_new: dict[str, str] = dict.fromkeys(letters, '')
    dictionary_new.update(dictionary_punctuation)

    dictionary_new_upper: dict[str, str] = dict.fromkeys(letters_upper, '')
    dictionary_new_upper.update(dictionary_punctuation)
    for i in range(26):
        new_order = (i + n) % 26
        dictionary_new[dictionary_original[i]] = dictionary_original[new_order]
        dictionary_new_upper[dictionary_original_upper[i]] = dictionary_original_upper[new_order]
    table = str.maketrans(dictionary_new)
    table_upper = str.maketrans(dictionary_new_upper)
    str_first = message.translate(table)
    str_res = str_first.translate(table_upper)
    return str_res
