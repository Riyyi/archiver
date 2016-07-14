def convert_str_to_int(string):

    integer = ''
    for character in string:
        integer += str(ord(character))

    return int(integer) % 8925
