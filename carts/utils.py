import random
import string


def random_string_generator(size=15,chars= string.ascii_uppercase + string.digits):

    l = ""
    for i in range(size):
        l += random.choice(chars)
    return l